import asyncio
import sys

import pytest as pytest

from foo_recursive import foo_recursive
from misc import async_session


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_foo_recursive_depth_a():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="ASC",
            depth=1,
            sort_fld="title"
        )
        await session.flush()
        await session.rollback()

        assert len(res) == 6
        assert res[0].title == "root"
        assert res[-1].title == "root_4"


@pytest.mark.asyncio
async def test_foo_recursive_depth_b():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="ASC",
            depth=3,
            sort_fld="title"
        )

        assert len(res) == 156
        assert res[0].title == "root"
        assert res[-1].title == "root_4_4_4"


@pytest.mark.asyncio
async def test_foo_recursive_sort_direction_a():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="ASC",
            depth=3,
            sort_fld="title"
        )

        assert len(res) == 156
        assert res[0].title == "root"
        assert res[-1].title == "root_4_4_4"


@pytest.mark.asyncio
async def test_foo_recursive_sort_direction_b():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="DESC",
            depth=3,
            sort_fld="title"
        )

        assert len(res) == 156
        assert res[0].title == "root"
        assert res[-1].title == "root_0_0_0"


@pytest.mark.asyncio
async def test_foo_recursive_sort_field():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="ASC",
            depth=3,
            sort_fld="id"
        )

        assert len(res) == 156
        assert res[0].title == "root"
        assert res[-1].title == "root_2_4_0"


@pytest.mark.asyncio
async def test_foo_recursive_sort_field():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="DESC",
            depth=3,
            sort_fld="id"
        )

        assert len(res) == 156
        assert res[0].title == "root"
        assert res[-1].title == "root_3_0_2"


@pytest.mark.asyncio
async def test_foo_recursive_root_id_a():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="ASC",
            depth=3,
            sort_fld="id"
        )

        assert len(res) == 156
        assert res[0].title == "root"
        assert res[-1].title == "root_2_4_0"


@pytest.mark.asyncio
async def test_foo_recursive_root_id_b():
    async with async_session() as session:
        res = await foo_recursive(
            session=session,
            sort_dir="ASC",
            depth=3,
            sort_fld="id",
            root_id="93a0a548-e608-459e-b57d-f76bb9c850aa"
        )

        assert len(res) == 30
        assert res[0].title == "root_0_0_1_0"
        assert res[-1].title == "root_0_0_1_3_2"
