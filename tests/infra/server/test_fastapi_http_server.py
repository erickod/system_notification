from typing import Dict
from unittest.mock import AsyncMock, Mock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from system_notification.domain.protocols.controller_protocol import HttpServer
from system_notification.infra.http.server.fastapi_http_server import FastApiHttpServer
from system_notification.infra.http.server.helpers.http_request import HttpRequest
from system_notification.infra.http.server.helpers.http_response import HttpResponse


class FakeServer:
    def __init__(self) -> None:
        self.run_called: bool = False

    def run(self, *args, **kwargs):
        self.run_called = True


class FakeController:
    http_server: HttpServer

    def __init__(
        self,
        http_server: HttpServer,
        response_dict: Dict[str, str],
        endpoint: str = "/",
        method: str = "GET",
        status_code: int = 200,
    ) -> None:
        self.endpoint = endpoint
        self.http_server = http_server
        self.http_server.on(method.upper(), endpoint, self)
        self.response_dict = response_dict
        self.status_code = status_code

    async def handle(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(status_code=self.status_code, body=self.response_dict)


async def test_serve_calls_run_with_right_params() -> None:
    server = FakeServer()
    sut = FastApiHttpServer(server=server)
    sut.serve()
    assert server.run_called


async def test_register_controller_calls_add_api_route_with_right_params() -> None:
    fake_app = Mock()
    controller = AsyncMock()
    server = FakeServer()
    sut = FastApiHttpServer(server=server, app=fake_app)
    sut.on("GET", "/", controller=controller)
    fake_app.add_api_route.assert_called()


async def test_ensure_fastapi_can_handle_controller_post_inside_its_inner_view() -> None:
    app = FastAPI()
    sut = FastApiHttpServer(app=app)
    controller = FakeController(
        http_server=sut,
        response_dict={"data": "testing"},
        status_code=200,
        endpoint="/testing",
        method="POST",
    )
    client = TestClient(app)
    response = client.post(
        controller.endpoint + "?name=John&name=Duo&email=mail@mail.com",
        json={"post_data": {}},
    )
    assert response.status_code == controller.status_code
    assert response.json() == controller.response_dict


async def test_ensure_fastapi_can_handle_controller_get_inside_its_inner_view() -> None:
    app = FastAPI()
    sut = FastApiHttpServer(app=app)
    controller = FakeController(
        http_server=sut,
        response_dict={"data": "testing"},
        status_code=200,
        endpoint="/testing",
        method="GET",
    )
    client = TestClient(app)
    response = client.get(
        controller.endpoint + "?name=John&name=Duo&email=mail@mail.com",
    )
    assert response.status_code == controller.status_code
    assert response.json() == controller.response_dict
