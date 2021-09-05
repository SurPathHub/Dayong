"""
dayong.models
~~~~~~~~~~~~~

A model maps to a single database table. It contains fields and behaviors of
the data stored in the database.
"""
from typing import Optional

from sqlmodel import Field, SQLModel


class TableModel(SQLModel):  # pylint: disable=R0903
    """Base class for table models.

    NOTE: Do not use this for things other than annotations.
    """


class AnonymousMessageTable(TableModel, table=True):
    """Table model for anonymous messages."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    nickname: str
    message: str
