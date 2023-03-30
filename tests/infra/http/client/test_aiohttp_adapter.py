import inspect
from typing import Any, Self
from unittest.mock import AsyncMock

from system_notification.infra.http.client.aiohttp_adapter import AioHttpAdapter


class ClientSessionFake:
    def __init__(self, status=200) -> None:
        self.status = 200
        self.read_is_called: bool = False
        self.request_is_called: bool = False
        self.json_is_called: bool = False

    async def json(self) -> Any:
        self.json_is_called = True
        return {}

    def request(self, *args, **kwargs) -> Any:
        self.request_is_called = True
        return self

    async def read(self) -> Any:
        self.read_is_called = True

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        pass


async def test_make_async_returns_a_coroutine() -> None:
    sut = AioHttpAdapter()
    output = await sut._make_async(data=AsyncMock())
    assert inspect.iscoroutinefunction(output)


async def test_get_method_calls_make_request() -> None:
    session = ClientSessionFake()
    sut = AioHttpAdapter(client_session=session)
    output = await sut.get("https://companyhero.com")
    assert session.json_is_called
    assert session.request_is_called
    assert session.read_is_called
    assert await output.json() == {}


async def test_post_method_calls_make_request() -> None:
    client_session = ClientSessionFake()
    sut = AioHttpAdapter(client_session=client_session)
    await sut.post("https://companyhero.com", json={})
    assert client_session.json_is_called
    assert client_session.request_is_called
    assert client_session.read_is_called


async def test_post_method_calls_make_request_with_files() -> None:
    client_session = ClientSessionFake()
    sut = AioHttpAdapter(client_session=client_session)
    await sut.post("https://companyhero.com", json={}, files={"anyfile": b""})
    assert client_session.json_is_called
    assert client_session.request_is_called
    assert client_session.read_is_called


async def test_put_method_calls_make_request() -> None:
    client_session = ClientSessionFake()
    sut = AioHttpAdapter(client_session=client_session)
    await sut.put("https://companyhero.com", json={})
    assert client_session.json_is_called
    assert client_session.request_is_called
    assert client_session.read_is_called


async def test_patch_method_calls_make_request() -> None:
    client_session = ClientSessionFake()
    sut = AioHttpAdapter(client_session=client_session)
    await sut.patch("https://companyhero.com", json={})
    assert client_session.json_is_called
    assert client_session.request_is_called
    assert client_session.read_is_called


async def test_delete_method_calls_make_request() -> None:
    client_session = ClientSessionFake()
    sut = AioHttpAdapter(client_session=client_session)
    await sut.delete("https://companyhero.com")
    assert client_session.json_is_called
    assert client_session.request_is_called
    assert client_session.read_is_called
