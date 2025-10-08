import functools
from typing import Any, Callable

from system_notification.domain.protocols.controller_protocol import Controller
from system_notification.domain.protocols.jwt_adapter_protocol import JWTAdapter
from system_notification.infra.http.server.helpers.http_request import HttpRequest
from system_notification.infra.http.server.helpers.http_response import HttpResponse


class JWTAuthControllerDecorator:
    def __init__(self, jwt_adapter: JWTAdapter) -> None:
        self._jwt_adapter = jwt_adapter
        self._is_authenticated: bool = False

    @property
    def authenticated(self) -> bool:
        return self._is_authenticated

    def __call__(self, controller: Callable, *args, **kwargs) -> Callable:
        self._undecorated_callable = controller

        @functools.wraps(controller)
        async def wrapper(controller_instance: Callable, request: HttpRequest) -> Any:
            authorization_list = request.headers.get("authorization", "").split(" ")
            if len(authorization_list) <= 1 or not self._jwt_adapter.is_valid(
                data=authorization_list[1]
            ):
                return HttpResponse(
                    status_code=401,
                    body={
                        "message": "Not Authorized",
                        "detail": "invalid API token",
                    },
                )
            self._is_authenticated = True
            return await controller(controller_instance, request=request)

        return wrapper
