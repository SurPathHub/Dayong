"""
dayong.models
~~~~~~~~~~~~~

A model maps to a single database table. It contains fields and behaviors of the data
stored in the database.
"""
from typing import Optional

from sqlmodel import Field, SQLModel


<<<<<<< HEAD
class TableModel(SQLModel):  # pylint: disable=R0903
    """Base class for table models.

    Do not modify or use this for things other than annotations as it is not
    advised to inherit from table models. See:
    https://sqlmodel.tiangolo.com/tutorial/fastapi/multiple-models/
    """


class AnonymousMessageTable(TableModel, table=True):
    """Table model for anonymous messages."""

=======
class Message(SQLModel):
    """Base model class for message table models."""

    message_id: str


class AnonMessage(Message, table=True):
    """Table model for anonymized guild messages."""

<<<<<<< HEAD
    __tablename__ = "anon_messages"
>>>>>>> a34eab6... feat: add functional slash command
=======
    # pyright cannot recognize the type of SQLModel.__tablename__
    # See: https://github.com/tiangolo/sqlmodel/issues/98
    __tablename__ = "anon_messages"  # type: ignore
>>>>>>> fd9070d... refactor: apply pyright
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    nickname: str
    message: str
