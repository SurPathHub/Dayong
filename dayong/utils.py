"""
dayong.utils
~~~~~~~~~~~~

This module provides useful functions that facilitate some of Dayong's routine
operations.
"""

SUPPORTED_DB = ("postgres://",)


def format_db_url(database_url: str) -> str:
    """Format the default database URL to support async requests/transactions.

    One case this is useful is when the hosting provider automatically provisions the
    database and changing the database URL isn't simple.

    Args:
        database_url (str): The default url of a supported database.

    Returns:
        str: A unique sequence of characters that identifies the database.
    """
    db_scheme = next(
        se_scheme if se_scheme in database_url else "" for se_scheme in SUPPORTED_DB
    )

    if not db_scheme:
        return database_url

    if db_scheme == "postgres://":
        db_name = "postgresql://"
    else:
        db_name = db_scheme

    return database_url.replace(
        db_scheme, f"""{db_name.replace("://", "+asyncpg://")}"""
    )


if __name__ == "__main__":
    pass
