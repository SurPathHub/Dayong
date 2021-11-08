"""
dayong.exts.apis
~~~~~~~~~~~~~~~~

Module in charge of retrieving content from API endpoints.
"""
import json
import urllib.request
from typing import Any, Optional

import aiohttp

from dayong.core.settings import CONTENT_PROVIDER
from dayong.exts.contents import ThirdPartyContent


class RESTClient:
    """Represents a client for interacting with REST APIs."""

    _headers = {"User-Agent": "Mozilla/5.0"}
    _request = urllib.request.Request("http://127.0.0.1", headers=_headers)
    _session: Optional[aiohttp.ClientSession] = None

    async def create_session(self):
        """Create client session."""
        if not self._session:
            self._session = aiohttp.ClientSession()

    async def get_content(self, data: Any, *args: Any) -> "ThirdPartyContent":
        """Parse and return fetched content.

        Args:
            data (Any): Response data from mail server.

        Returns:
            ThirdPartyContent: Representation of content from third-party
                service/content provider.
        """
        await self.create_session()
        assert isinstance(self._session, aiohttp.ClientSession)
        resp = await self._session.get(data)
        data = await resp.text()
        return await ThirdPartyContent.parse(json.loads(data), args[0])

    async def get_devto_article(self, sort_by_date: bool = False) -> ThirdPartyContent:
        """Retrieve URLs of dev.to articles.

        Args:
            sort_by_date (bool, optional): Whether to order articles by descending
                publish date. Defaults to False.

        Returns:
            ThirdPartyContent: List of article URLs.
        """

        request = self._request

        if sort_by_date:
            request.full_url = f"""{CONTENT_PROVIDER["dev"]}/api/articles/latest/"""
        else:
            request.full_url = f"""{CONTENT_PROVIDER["dev"]}/api/articles/"""

        return await self.get_content(request.full_url, "canonical_url")
