from typing import Coroutine, Protocol


class HttpClient(Protocol):
    def get(self, url: str) -> Coroutine:
        pass

    def post(self, url: str, json, files=None) -> Coroutine:
        pass

    def put(self, url: str, json) -> Coroutine:
        pass

    def patch(self, url: str, json) -> Coroutine:
        pass

    def delete(self, url: str) -> Coroutine:
        pass
