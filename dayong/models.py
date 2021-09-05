"""
dayong.models
~~~~~~~~~~~~~

<<<<<<< HEAD
A model maps to a single database table. It contains fields and behaviors of the data
stored in the database.
=======
A model maps to a single database table. It contains fields and behaviors of
the data stored in the database.
>>>>>>> 89e51bc... feat: moderate anon messages on sql database
"""
from typing import Optional

from sqlmodel import Field, SQLModel


<<<<<<< HEAD
class Message(SQLModel):
    """Base model class for message table models."""

    message_id: str


class AnonMessage(Message, table=True):
    """Table model for anonymized guild messages."""

    # pyright cannot recognize the type of SQLModel.__tablename__
    # See: https://github.com/tiangolo/sqlmodel/issues/98
    __tablename__ = "anon_messages"  # type: ignore
=======
class TableModel(SQLModel):  # pylint: disable=R0903
    """Base class for table models.

    NOTE: Do not use this for things other than annotations.
    """


class AnonymousMessageTable(TableModel, table=True):
    """Table model for anonymous messages."""

>>>>>>> 89e51bc... feat: moderate anon messages on sql database
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    nickname: str
    message: str
