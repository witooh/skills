"""JMAP client for Fastmail email operations."""

import requests


class JMAPClient:
    SESSION_URL = "https://api.fastmail.com/jmap/session"

    def __init__(self, token: str):
        self._token = token
        self._session: dict | None = None

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

    def get_session(self) -> dict:
        if self._session:
            return self._session

        resp = requests.get(self.SESSION_URL, headers=self._headers())
        resp.raise_for_status()
        self._session = resp.json()
        return self._session

    def call(self, method_calls: list[tuple[str, dict, str]]) -> dict:
        session = self.get_session()

        request_body = {
            "using": [
                "urn:ietf:params:jmap:core",
                "urn:ietf:params:jmap:mail",
                "urn:ietf:params:jmap:submission",
            ],
            "methodCalls": method_calls,
        }

        resp = requests.post(
            session["apiUrl"],
            json=request_body,
            headers={**self._headers(), "Content-Type": "application/json"},
        )
        resp.raise_for_status()
        return resp.json()

    def get_account_id(self) -> str:
        session = self.get_session()
        return session["primaryAccounts"]["urn:ietf:params:jmap:mail"]
