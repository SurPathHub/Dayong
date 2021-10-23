"""
dayong.exts.apis
~~~~~~~~~~~~~~~~

Module in charge of retrieving content from API endpoints.
"""
import asyncio
import json
import urllib.request
from typing import Any

from dayong.abc import Client
from dayong.exts.contents import ThirdPartyContent
from dayong.settings import CONTENT_PROVIDER


class RESTClient(Client):
    """Represents a client for interacting with REST APIs."""

    _headers = {"User-Agent": "Mozilla/5.0"}
    _request = urllib.request.Request("http://127.0.0.1", headers=_headers)

    @staticmethod
    async def get_content(data: Any, *args: Any, **kwargs: Any) -> ThirdPartyContent:
        loop = asyncio.get_running_loop()
        resp = await loop.run_in_executor(None, urllib.request.urlopen, data)
        data = await loop.run_in_executor(None, json.loads, resp.read())
        return await ThirdPartyContent.parse(data, list(kwargs.values())[0])

    async def get_devto_article(self, sort_by_date: bool = False) -> ThirdPartyContent:
        """Retrieve URLs of dev.to articles.

        Args:
            sort_by_date (bool, optional): Whether to order articles by descending
                publish date. Defaults to False.

        Returns:
            list[str]: List of article URLs.
        """
        request = self._request

        if sort_by_date:
            request.full_url = f"""{CONTENT_PROVIDER["dev"]}/api/articles/latest/"""
        else:
            request.full_url = f"""{CONTENT_PROVIDER["dev"]}/api/articles/"""

        return await RESTClient.get_content(request, "canonical_url")
