# pylint: disable=W0231
"""
dayong.tasks.emails
~~~~~~~~~~~~~~~~~~~

Module in charge of retrieving content on email subscription.
"""
import asyncio
import re
from dataclasses import dataclass
from typing import Any, Optional, Union

from pragmail import Client, utils
from pragmail.exceptions import IMAP4Error

from dayong.exts.contents import ThirdPartyContent


@dataclass
class EmailClient:
    """Represents a client for retrieving email subscriptions."""

    host: str
    email: str
    password: str
    max_retries: int = 5

    def __post_init__(self) -> None:
        self._client: Optional[Client] = None
        self.connect_to_server()

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
    async def parse_message_data(
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

    @staticmethod
    async def get_content(data: Any) -> ThirdPartyContent:
        """Parse and return fetched content.

        Args:
            data (Any): Response data from mail server.

        Returns:
            ThirdPartyContent: Representation of content from third-party
                service/content provider.
        """
        message_body = await EmailClient.parse_message_data(data)
        return await ThirdPartyContent.parse(EmailClient.extract_mime_url(message_body))

    def connect_to_server(self) -> None:
        """Connect to the mail server."""
        try:
            if self._client:
                self._client.logout()

            self._client = Client(self.host)
            self._client.login(self.email, self.password)
            self._client.select("INBOX")
        except IMAP4Error as emap_err:
            raise ValueError from emap_err

    async def get_medium_daily_digest(self) -> ThirdPartyContent:
        """Retrieve relevant content URLs from the latest Medium Daily Digest message.

        Raises:
            ValueError: Raised if the email server returned an error response.

        Returns:
            list[str]: List of url strings.
        """
        assert self._client
        loop = asyncio.get_running_loop()
        response, message = await loop.run_in_executor(
            None, self._client.latest_message, "Medium Daily Digest"
        )

        if response != "OK":
            if self.max_retries > 0:
                self.max_retries -= 1
                await loop.run_in_executor(None, self.connect_to_server)
                await loop.run_in_executor(None, self.get_medium_daily_digest)
            else:
                raise ValueError(f"{repr(self._client)} returned {response=}")

        return await self.get_content(message)
