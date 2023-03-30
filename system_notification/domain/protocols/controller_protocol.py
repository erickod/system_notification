from typing import Protocol

from system_notification.infra.http.server.helpers.http_request import HttpRequest
from system_notification.infra.http.server.helpers.http_response import HttpResponse


class HttpServer(Protocol):
    def serve(self, port: int = 8000) -> None:
        ...

    def on(self, method: str, url: str, controller: "Controller") -> None:
        ...


class Controller(Protocol):
    http_server: HttpServer

    def __init__(self, http_server: HttpServer) -> None:
        ...

    async def handle(self, request: HttpRequest) -> HttpResponse:
        ...
