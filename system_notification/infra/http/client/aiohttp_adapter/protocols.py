from typing import Any, Protocol


class ClientSession(Protocol):
    def request(self, *args, **kwargs) -> Any:
        return self

    async def read(self, *args, **kwargs) -> Any:
        return

    async def __aenter__(self) -> "ClientSession":
        return self

    async def __aexit__(self, *args, **kwargs) -> None:
        pass
