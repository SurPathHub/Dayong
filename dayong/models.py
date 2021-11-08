"""
dayong.models
~~~~~~~~~~~~~

A model maps to a single database table. It contains fields and behaviors of the data
stored in the database.
"""
from typing import Optional

from sqlmodel import Field, SQLModel


class Message(SQLModel):
    """Base model class for message table models."""

    id: Optional[int] = Field(default=None, primary_key=True)


class AnonMessage(Message, table=True):
    """Table model for anonymized guild messages."""

    # pyright cannot recognize the type of SQLModel.__tablename__
    # See: https://github.com/tiangolo/sqlmodel/issues/98
    __tablename__ = "anon_messages"  # type: ignore
    message_id: str
    user_id: str
    username: str
    nickname: str
    message: str


class ScheduledTask(SQLModel, table=True):
    """Table model for scheduled tasks."""

    id: Optional[int] = Field(default=None, primary_key=True)
    channel_name: str
    task_name: str
    run: Optional[bool] = Field(default=True)
