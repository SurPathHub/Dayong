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

    message_id: str


class AnonMessage(Message, table=True):
    """Table model for anonymized guild messages."""

    __tablename__ = "anon_messages"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    nickname: str
    message: str
