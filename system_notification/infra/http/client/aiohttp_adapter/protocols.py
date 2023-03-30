from typing import Any, Protocol, Self


class ClientSession(Protocol):
    def request(self, *args, **kwargs) -> Any:
        return self

    async def read(self, *args, **kwargs) -> Any:
        return

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        pass
