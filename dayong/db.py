"""
dayong.db
~~~~~~~~~

Database connections used within Dayong.
"""
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from dayong.models import TableModel


class DBConnection:
    """Provides methods for interacting with table models."""

    def __init__(self, connection_uri: str):
        self.engine = create_async_engine(connection_uri)

    async def create_table(self) -> None:
        """Create database table."""
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def add_row(self, model: TableModel) -> None:
        """Add row to instance of `db.TableModel`."""
        async with AsyncSession(self.engine) as session:
            session.add(model)
            await session.commit()

    # NOTE: Wait 'til https://github.com/tiangolo/sqlmodel/pull/58 gets merged
    # async def get_row_by_username(self, username: str) -> Union[_T, None]:
    #     """Fetch information on author by username.
    #     Args:
    #         username (str): The server member's username.
    #     Returns:
    #         Union[_T, None]: Scalar value if the username exists, None
    #             otherwise.
    #     """
    #
    # async with AsyncSession(AnonymousMessageTable) as session:
    #     statement = select(self.anon_table).where(
    #         AnonymousMessageTable.username == username
    #     )
    #     result = await session.exec(statement)
    #     return result.first()
