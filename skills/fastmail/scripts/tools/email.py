"""Email operations via JMAP."""

from __future__ import annotations

from ..jmap_client import JMAPClient
from ..errors import NotFoundError


_EMAIL_LIST_PROPERTIES = [
    "id", "blobId", "threadId", "mailboxIds", "subject",
    "from", "to", "cc", "receivedAt", "preview",
    "hasAttachment", "keywords",
]


class EmailTools:
    def __init__(self, client: JMAPClient):
        self._client = client

    def get_mailboxes(self) -> list[dict]:
        account_id = self._client.get_account_id()
        resp = self._client.call([
            ("Mailbox/get", {"accountId": account_id, "properties": ["id", "name", "role", "totalEmails", "unreadEmails"]}, "a"),
        ])
        return resp["methodResponses"][0][1]["list"]

    def _get_inbox_id(self) -> str:
        mailboxes = self.get_mailboxes()
        inbox = next((m for m in mailboxes if m.get("role") == "inbox"), None)
        if not inbox:
            raise RuntimeError("Inbox not found")
        return inbox["id"]

    def list_emails(self, mailbox_id: str | None = None, limit: int = 20) -> list[dict]:
        account_id = self._client.get_account_id()
        target_mailbox = mailbox_id or self._get_inbox_id()

        resp = self._client.call([
            ("Email/query", {
                "accountId": account_id,
                "filter": {"inMailbox": target_mailbox},
                "sort": [{"property": "receivedAt", "isAscending": False}],
                "limit": limit,
            }, "a"),
            ("Email/get", {
                "accountId": account_id,
                "#ids": {"resultOf": "a", "name": "Email/query", "path": "/ids"},
                "properties": _EMAIL_LIST_PROPERTIES,
            }, "b"),
        ])
        return resp["methodResponses"][1][1]["list"]

    def get_email(self, email_id: str) -> dict:
        account_id = self._client.get_account_id()
        resp = self._client.call([
            ("Email/get", {
                "accountId": account_id,
                "ids": [email_id],
                "properties": [
                    "id", "blobId", "threadId", "mailboxIds", "subject",
                    "from", "to", "cc", "receivedAt", "preview",
                    "hasAttachment", "keywords", "textBody", "htmlBody", "bodyValues",
                ],
                "fetchTextBodyValues": True,
                "fetchHTMLBodyValues": True,
            }, "a"),
        ])
        result_list = resp["methodResponses"][0][1]["list"]
        if not result_list:
            raise NotFoundError("email", email_id)
        return result_list[0]

    def search_emails(self, query: str, limit: int = 20) -> list[dict]:
        account_id = self._client.get_account_id()
        resp = self._client.call([
            ("Email/query", {
                "accountId": account_id,
                "filter": {"text": query},
                "sort": [{"property": "receivedAt", "isAscending": False}],
                "limit": limit,
            }, "a"),
            ("Email/get", {
                "accountId": account_id,
                "#ids": {"resultOf": "a", "name": "Email/query", "path": "/ids"},
                "properties": _EMAIL_LIST_PROPERTIES,
            }, "b"),
        ])
        return resp["methodResponses"][1][1]["list"]

    def send_email(
        self,
        to: list[dict],
        subject: str,
        text_body: str,
        html_body: str | None = None,
        cc: list[dict] | None = None,
        bcc: list[dict] | None = None,
        in_reply_to: str | None = None,
        references: list[str] | None = None,
    ) -> dict:
        account_id = self._client.get_account_id()

        # Get identity for sending
        identity_resp = self._client.call([
            ("Identity/get", {"accountId": account_id}, "a"),
        ])
        identities = identity_resp["methodResponses"][0][1]["list"]
        if not identities:
            raise RuntimeError("No identity found")
        identity_id = identities[0]["id"]

        email_create: dict = {
            "mailboxIds": {},
            "to": to,
            "subject": subject,
            "bodyValues": {
                "body": {"value": text_body, "isEncodingProblem": False, "isTruncated": False},
            },
            "textBody": [{"partId": "body", "type": "text/plain"}],
        }

        if cc:
            email_create["cc"] = cc
        if bcc:
            email_create["bcc"] = bcc
        if in_reply_to:
            email_create["inReplyTo"] = [in_reply_to]
        if references:
            email_create["references"] = references

        if html_body:
            email_create["bodyValues"] = {
                "textBody": {"value": text_body, "isEncodingProblem": False, "isTruncated": False},
                "htmlBody": {"value": html_body, "isEncodingProblem": False, "isTruncated": False},
            }
            email_create["textBody"] = [{"partId": "textBody", "type": "text/plain"}]
            email_create["htmlBody"] = [{"partId": "htmlBody", "type": "text/html"}]

        resp = self._client.call([
            ("Email/set", {
                "accountId": account_id,
                "create": {"draft": email_create},
            }, "a"),
            ("EmailSubmission/set", {
                "accountId": account_id,
                "create": {
                    "send": {
                        "identityId": identity_id,
                        "emailId": "#draft",
                    },
                },
                "onSuccessUpdateEmail": {
                    "#send": {
                        "mailboxIds/drafts": None,
                        "mailboxIds/sent": True,
                        "keywords/$draft": None,
                    },
                },
            }, "b"),
        ])

        email_result = resp["methodResponses"][0][1]
        submission_result = resp["methodResponses"][1][1]

        return {
            "emailId": (email_result.get("created") or {}).get("draft", {}).get("id", ""),
            "submissionId": (submission_result.get("created") or {}).get("send", {}).get("id", ""),
        }

    def move_to_folder(self, email_id: str, target_mailbox_id: str, source_mailbox_id: str | None = None) -> None:
        account_id = self._client.get_account_id()

        patch: dict = {f"mailboxIds/{target_mailbox_id}": True}

        mailboxes_to_remove: set[str] = set()
        if source_mailbox_id:
            mailboxes_to_remove.add(source_mailbox_id)
        else:
            current_email = self.get_email(email_id)
            for mailbox_id in (current_email.get("mailboxIds") or {}).keys():
                if mailbox_id != target_mailbox_id:
                    mailboxes_to_remove.add(mailbox_id)

        for mailbox_id in mailboxes_to_remove:
            patch[f"mailboxIds/{mailbox_id}"] = None

        self._client.call([
            ("Email/set", {
                "accountId": account_id,
                "update": {email_id: patch},
            }, "a"),
        ])

    def set_keywords(self, email_id: str, keywords: dict[str, bool]) -> None:
        account_id = self._client.get_account_id()

        patch: dict = {}
        for keyword, value in keywords.items():
            patch[f"keywords/{keyword}"] = value if value else None

        self._client.call([
            ("Email/set", {
                "accountId": account_id,
                "update": {email_id: patch},
            }, "a"),
        ])

    def delete_email(self, email_id: str) -> None:
        mailboxes = self.get_mailboxes()
        trash = next((m for m in mailboxes if m.get("role") == "trash"), None)
        if not trash:
            raise RuntimeError("Trash folder not found")
        self.move_to_folder(email_id, trash["id"])

    def get_thread(self, email_id: str) -> dict:
        account_id = self._client.get_account_id()

        # Get threadId from email
        resp = self._client.call([
            ("Email/get", {
                "accountId": account_id,
                "ids": [email_id],
                "properties": ["id", "threadId"],
            }, "a"),
        ])
        email_result = resp["methodResponses"][0][1]["list"]
        if not email_result:
            raise NotFoundError("email", email_id)

        thread_id = email_result[0]["threadId"]

        # Get all emails in thread
        thread_resp = self._client.call([
            ("Email/query", {
                "accountId": account_id,
                "filter": {"inThread": thread_id},
                "sort": [{"property": "receivedAt", "isAscending": True}],
            }, "a"),
            ("Email/get", {
                "accountId": account_id,
                "#ids": {"resultOf": "a", "name": "Email/query", "path": "/ids"},
                "properties": _EMAIL_LIST_PROPERTIES,
            }, "b"),
        ])

        emails = thread_resp["methodResponses"][1][1]["list"]
        if not emails:
            raise NotFoundError("thread", thread_id)

        # Extract unique participants
        participants: dict[str, dict] = {}
        for email in emails:
            for field in ("from", "to", "cc"):
                for p in (email.get(field) or []):
                    if p.get("email") and p["email"] not in participants:
                        participants[p["email"]] = p

        return {
            "id": thread_id,
            "emails": emails,
            "subject": emails[0].get("subject", ""),
            "participants": list(participants.values()),
            "latestDate": emails[-1].get("receivedAt", ""),
            "emailCount": len(emails),
        }

    @staticmethod
    def _extract_bulk_result(result: dict) -> dict:
        succeeded = list((result.get("updated") or {}).keys())
        failed = [
            {"id": eid, "error": err.get("description", err.get("type", "unknown"))}
            for eid, err in (result.get("notUpdated") or {}).items()
        ]
        return {"succeeded": succeeded, "failed": failed}

    def bulk_move_to_folder(
        self,
        email_ids: list[str],
        target_mailbox_id: str,
        source_mailbox_id: str | None = None,
    ) -> dict:
        account_id = self._client.get_account_id()

        update: dict = {}
        for eid in email_ids:
            patch: dict = {f"mailboxIds/{target_mailbox_id}": True}
            if source_mailbox_id:
                patch[f"mailboxIds/{source_mailbox_id}"] = None
            update[eid] = patch

        resp = self._client.call([
            ("Email/set", {"accountId": account_id, "update": update}, "a"),
        ])
        return self._extract_bulk_result(resp["methodResponses"][0][1])

    def bulk_set_keywords(self, email_ids: list[str], keywords: dict[str, bool]) -> dict:
        account_id = self._client.get_account_id()

        patch: dict = {}
        for keyword, value in keywords.items():
            patch[f"keywords/{keyword}"] = value if value else None

        update = {eid: dict(patch) for eid in email_ids}

        resp = self._client.call([
            ("Email/set", {"accountId": account_id, "update": update}, "a"),
        ])
        return self._extract_bulk_result(resp["methodResponses"][0][1])

    def bulk_delete_emails(self, email_ids: list[str]) -> dict:
        mailboxes = self.get_mailboxes()
        trash = next((m for m in mailboxes if m.get("role") == "trash"), None)
        if not trash:
            raise NotFoundError("mailbox", "Trash")
        return self.bulk_move_to_folder(email_ids, trash["id"])
