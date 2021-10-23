# pylint: disable=R0903
"""
dayong.exts.contents
~~~~~~~~~~~~~~~~~~~~

Handlers for third-party content.
"""
from typing import Any, Optional


class ThirdPartyContent:
    """Represents content from third-party service/content provider."""

    content: Any

    @staticmethod
    async def collect(content_list: Any, constraint: Any) -> list[Any]:
        """Parse response data for specific parts.

        Args:
            content_list (Any): The sequence to be processed.
            constraint (Any): Any immutable type that can be used as a dictionary key.

        Returns:
            list[Any]: A list of parsed response data.
        """
        parts: list[Any] = []

        if constraint:
            for content in content_list:
                parts.append(content[constraint])
        else:
            parts = content_list

        return parts

    @classmethod
    async def parse(
        cls, content: Any, constraint: Optional[Any] = None
    ) -> "ThirdPartyContent":
        """Parse response data.

        Returns:
            ThirdPartyContent: Class instance containing parsed third party content.
        """
        tp_content = ThirdPartyContent()
        if isinstance(content, list):
            tp_content.content = await ThirdPartyContent.collect(content, constraint)
        else:
            tp_content.content = content
        return tp_content
