import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import config
import asyncpg
import pytest


async def test_health_check(ac: AsyncClient):
    data = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }
    response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == data


# The following fixture will be automatically used for all test functions that require it.
@pytest.fixture(autouse=True)
async def prepare_database():
    # Replace the connection parameters with your actual database configuration
    conn_params = {
        "host": "postgres_test",  # The service name of the PostgreSQL container
        "port": 5432,  # The port mapped to the PostgreSQL container
        "user": "postgres",
        "password": "postgres",
        "database": "db_test",
    }
    # Attempt to establish a connection to the database
    conn = await asyncpg.connect(**conn_params)
    try:
        # Test the connection by executing a simple query
        await conn.execute("SELECT 1")
    except asyncpg.exceptions.PostgresError:
        # Raise an exception if there is an error connecting to the database
        pytest.fail("Failed to connect to the database")
    finally:
        # Close the connection
        await conn.close()

def test_database_connection():
    # This test will automatically use the `prepare_database` fixture before running
    # and check if the database connection is successful.
    pass