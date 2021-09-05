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

    Do not modify or use this for things other than annotations as it is not
    advised to inherit from table models. See:
    https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/
    """


class AnonymousMessageTable(TableModel, table=True):
    """Table model for anonymous messages."""

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    nickname: str
    message: str
