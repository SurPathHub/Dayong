"""
dayong.tasks.emails
~~~~~~~~~~~~~~~~~~~

Module in charge of retrieving content on email subscription.
"""
import re
from typing import Any, Optional, Union

from pragmail import Client, utils

from dayong.utils import run_in_executor


class EmailClient:
    """Represents a client for retrieving email subscriptions."""

    def __init__(
        self,
        host: str,
        email: str,
        password: str,
        max_retries: Optional[int] = None,
    ) -> None:
        self.host = host
        self.email = email
        self.password = password
        self.max_retries = max_retries if max_retries is not None else 5
        self._client = Client(self.host)
        self._client.login(self.email, self.password)

    @staticmethod
    def extract_mime_url(msg: bytes) -> Any:
        """Extract URLs from message.

        Args:
            msg (bytes): Message retrieved from email server.

        Returns:
            Any: List of url strings.
        """
        uris: list[str] = []
        msg = msg.replace(b"\r\n", b"")
        body = utils.read_message(msg, as_string=True)

        if not isinstance(body, str):
            body = str(body)

        # Extract URLs. Only include link to articles written by Medium users.
        # Path to user profiles includes an "@" symbol and have greater than three
        # slashes.
        for href in re.findall(r'href=3D[\'"]?([^\'">?]+)', body):
            if href.count("/") > 3 and "@" in href:
                uri = href.replace("=", "")
            else:
                uri = ""

            # Add url and avoid duplicates.
            if uri and uri not in uris:
                uris.append(uri)

        return uris

    @staticmethod
    def parse_message_data(
        message: Union[list[Any], list[Union[bytes, tuple[bytes, bytes]]]]
    ) -> Any:
        """Parse the message data and extract message body.

        Args:
            message (Union[list[Any], list[Union[bytes, tuple[bytes, bytes]]]]): The
                message object retrieved from the email server.

        Raises:
            TypeError: Raised if message data is not a tuple.

        Returns:
            Any: The message body.
        """
        message_data = message[0]

        if isinstance(message_data, tuple):
            message_body = message_data[1]
        else:
            raise TypeError(f"{type(message_data)}, {message_data=}")

        return message_body

    def reconnect(self) -> None:
        """Reconnect to the server."""
        self._client.logout()
        self._client = Client(self.host)
        self._client.login(self.email, self.password)

    @run_in_executor
    def get_medium_daily_digest(self) -> list[str]:
        """Retrieve relevant content URLs from the latest Medium Daily Digest message.

        Raises:
            ValueError: Raised if the email server returned an error response.

        Returns:
            list[str]: List of url strings.
        """
        response, _ = self._client.select("INBOX")

        if not response == "OK" and self.max_retries:
            self.max_retries -= 1
            self.reconnect()
            self.get_medium_daily_digest()

        response, message = self._client.latest_message("Medium Daily Digest")

        if not response == "OK":
            raise ValueError(f"{repr(self._client)} returned {response=}")

        message_body = EmailClient.parse_message_data(message)
        return EmailClient.extract_mime_url(message_body)

    @classmethod
    def client(
        cls,
        host: str,
        email: str,
        password: str,
        max_retries: Optional[int] = None,
    ) -> "EmailClient":
        """Return an instance of `dayong.exts.email.Client`.

        Args:
            host (str): The IMAP server URL.
            email (str): The subscriber's email address.
            password (str): The email account's password.
            max_retries (Optional[int], optional): The number of reconnection attempts.
                Defaults to None.

        Returns:
            EmailClient: A `dayong.exts.EmailClient` instance.
        """
        return cls(
            host=host,
            email=email,
            password=password,
            max_retries=max_retries,
        )


if __name__ == "__main__":
    pass
