# pylint: disable=R0903
"""
dayong.abc
~~~~~~~~~~

Object interfaces used within Dayong.
"""

from abc import ABC
from typing import Any


class Client(ABC):
    """Interface for a client class supporting any third-party service."""

    @staticmethod
    async def get_content(data: Any, *args: Any, **kwargs: Any) -> Any:
        """Parse response data from a web request for specific content or detail.

        Returns:
            Any: Part of the response data.
        """
        raise NotImplementedError
