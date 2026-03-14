"""Custom error classes with user-friendly messages and suggestions."""


class FastmailError(Exception):
    def __init__(self, message: str, code: str, suggestion: str | None = None, details: object = None):
        super().__init__(message)
        self.code = code
        self.suggestion = suggestion
        self.details = details

    def to_dict(self) -> dict:
        result: dict = {
            "error": str(self),
            "code": self.code,
        }
        if self.suggestion:
            result["suggestion"] = self.suggestion
        if self.details:
            result["details"] = self.details
        return result


class AuthenticationError(FastmailError):
    _MESSAGES = {
        "email": {
            "message": "Failed to authenticate with Fastmail email API",
            "suggestion": (
                "Check your FASTMAIL_API_TOKEN environment variable. "
                "Generate a new token at Fastmail Settings → Privacy & Security → Integrations → API tokens"
            ),
        },
        "calendar": {
            "message": "Failed to authenticate with Fastmail calendar",
            "suggestion": (
                "Check your FASTMAIL_USERNAME and FASTMAIL_PASSWORD environment variables. "
                "Use an app password, not your main password. "
                "Generate at Fastmail Settings → Privacy & Security → Integrations → App passwords"
            ),
        },
    }

    def __init__(self, auth_type: str, original_error: str | None = None):
        msg = self._MESSAGES[auth_type]
        super().__init__(
            msg["message"],
            "AUTH_ERROR",
            msg["suggestion"],
            {"originalError": original_error} if original_error else None,
        )


class ConfigurationError(FastmailError):
    def __init__(self, missing_vars: list[str]):
        var_list = ", ".join(missing_vars)
        suggestion = (
            "Set FASTMAIL_API_TOKEN for email operations. "
            "Get your token from Fastmail Settings → Privacy & Security → Integrations"
            if "FASTMAIL_API_TOKEN" in missing_vars
            else "Set FASTMAIL_USERNAME and FASTMAIL_PASSWORD for calendar operations. "
            "Create an app password at Fastmail Settings → Privacy & Security → Integrations"
        )
        super().__init__(
            f"Missing required environment variable(s): {var_list}",
            "CONFIG_ERROR",
            suggestion,
        )


class NotFoundError(FastmailError):
    _SUGGESTIONS = {
        "email": "Use list_emails to see available emails, or search_emails to find specific ones",
        "mailbox": "Use list_mailboxes to see available folders/mailboxes",
        "calendar": "Use list_calendars to see available calendars",
        "event": "Use list_events with a date range to find events, or search_events to search by text",
        "thread": "The email thread may have been deleted or the email_id is incorrect. Use list_emails to verify",
        "reminder": "Use list_event_reminders to see reminders for an event",
    }

    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            f"{resource_type.capitalize()} not found: {resource_id}",
            "NOT_FOUND",
            self._SUGGESTIONS.get(resource_type),
        )


class ValidationError(FastmailError):
    def __init__(self, field: str, reason: str, expected_format: str | None = None):
        super().__init__(
            f"Invalid {field}: {reason}",
            "VALIDATION_ERROR",
            f"Expected format: {expected_format}" if expected_format else None,
        )


class APIError(FastmailError):
    def __init__(self, operation: str, status_code: int, status_text: str, response_body: str | None = None):
        if status_code == 401:
            suggestion = "Your authentication token may have expired. Generate a new one at Fastmail Settings"
        elif status_code == 403:
            suggestion = "Your API token may not have sufficient permissions. Create a new token with full access"
        elif status_code == 404:
            suggestion = "The requested resource does not exist or has been deleted"
        elif status_code == 429:
            suggestion = "Rate limit exceeded. Wait a few seconds and try again"
        elif status_code >= 500:
            suggestion = "Fastmail server error. Check https://fastmailstatus.com/ for service status"
        else:
            suggestion = "Check the API documentation or try the operation again"

        super().__init__(
            f"{operation} failed: {status_code} {status_text}",
            "API_ERROR",
            suggestion,
            {"statusCode": status_code, "responseBody": response_body},
        )


class BulkOperationError(FastmailError):
    def __init__(self, operation: str, succeeded: list[str], failed: list[dict]):
        self.succeeded = succeeded
        self.failed = failed
        super().__init__(
            f"{operation} partially completed: {len(succeeded)} succeeded, {len(failed)} failed",
            "BULK_PARTIAL",
            "Review the failed items and retry them individually if needed",
            {"succeeded": succeeded, "failed": failed},
        )


def format_error(error: Exception) -> dict:
    if isinstance(error, FastmailError):
        return {"success": False, **error.to_dict()}

    message = str(error)

    if "401" in message or "Unauthorized" in message:
        return format_error(AuthenticationError("email", message))

    if "FASTMAIL_API_TOKEN" in message:
        return format_error(ConfigurationError(["FASTMAIL_API_TOKEN"]))

    if "FASTMAIL_USERNAME" in message or "FASTMAIL_PASSWORD" in message:
        return format_error(ConfigurationError(["FASTMAIL_USERNAME", "FASTMAIL_PASSWORD"]))

    result: dict = {"success": False, "error": message}
    result["suggestion"] = "If this error persists, check your environment variables and network connection"
    return result
