"""
dayong.tasks.medium
~~~~~~~~~~~~~~~~~~~

Module in charge of retrieving email messages from Medium Daily Digest.
"""
import os
import re

from dotenv import load_dotenv
from pragmail import Client, utils

load_dotenv()


def extract_mime_url(msg: bytes) -> list[str]:
    """Extract URLs from message."""
    uri = [""]
    msg = msg.replace(b"\r\n", b"")
    body = utils.read_message(msg, as_string=True)

    if not isinstance(body, str):
        body = str(body)

    # Extract URLs. Only include link to articles written by Medium users. Path to user
    # profiles includes an "@" symbol and have greater than three slashes.
    for href in re.findall(r'href=3D[\'"]?([^\'">?]+)', body):
        if href.count("/") > 3 and "@" in href:
            uri.append(href.replace("=", ""))

    return uri


def get_medium_daily_digest():
    """Retrieve relevant content URLs from the latest Medium Daily Digest message."""
    client = Client("imap.gmail.com")
    client.login(os.environ["EMAIL"], os.environ["EMAIL_PASSWORD"])
    client.select("INBOX")
    response, message = client.latest_message("Medium Daily Digest")

    if response == "OK" and isinstance(message, tuple):
        message_body: bytes = message[0][1]
        articles = extract_mime_url(message_body)
    else:
        articles = []

    if articles:
        for url in articles:
            print(url)

    client.logout()


if __name__ == "__main__":
    get_medium_daily_digest()
