# pylint: disable=R0903
"""
dayong.exts.contents
~~~~~~~~~~~~~~~~~~~~

"""
from typing import Any, Optional


class ThirdPartyContent:
    """Represents content from third-party service/content providers."""

    def __init__(self, content: Any, constraint: Optional[Any] = None) -> None:
        if isinstance(content, list):
            self.content = ThirdPartyContent.collect(content, constraint)
        else:
            self.content = content

    @staticmethod
    def collect(content_list: Any, constraint: Any) -> list[Any]:
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
