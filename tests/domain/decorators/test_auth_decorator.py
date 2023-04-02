from system_notification.domain.decorators import JWTAuthControllerDecorator
from system_notification.infra.http.server.helpers.http_request import HttpRequest
from system_notification.infra.http.server.helpers.http_response import HttpResponse
from system_notification.infra.jwt import JoseJWTAdapter

jwt_adapter = JoseJWTAdapter(secret="secret")
jwt_auth_validation = JWTAuthControllerDecorator(jwt_adapter=jwt_adapter)


class FakeController:
    def __init__(self, response: HttpResponse) -> None:
        self._response = response

    @jwt_auth_validation
    async def handle(self, request: HttpRequest) -> HttpResponse:
        return self._response


async def test_jwt_auth_validation_decorator_returns_controller_response_when_client_is_authenticated() -> None:
    jwt_token = jwt_adapter.encode({"email": "mail@mail.com", "user": "John Duo"})
    response = HttpResponse(
        status_code=200,
        body={},
    )
    controller = FakeController(response)
    output_response = await controller.handle(
        HttpRequest(headers={"authorization": f"Bearer {jwt_token}"})
    )
    assert jwt_auth_validation.authenticated
    assert response is output_response


async def test_jwt_auth_validation_decorator_returns_status_401_when_client_is_not_authenticated() -> None:
    jwt_auth_validation = JWTAuthControllerDecorator(jwt_adapter=jwt_adapter)
    response = HttpResponse(
        status_code=200,
        body={},
    )

    controller = FakeController(response)
    output_response = await controller.handle(
        HttpRequest(headers={"authorization": f"Bearer INVALID TOKEN"})
    )

    assert jwt_auth_validation.authenticated == False
    assert output_response.status_code == 401
    assert output_response.body == {
        "message": "Not Authorized",
        "detail": "invalid API token",
    }
