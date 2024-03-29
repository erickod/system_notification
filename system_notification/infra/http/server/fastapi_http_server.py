import contextlib
import json
from typing import Any, Dict

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from system_notification.domain.protocols import Controller
from system_notification.infra.http.server.helpers.http_request import HttpRequest


def get_query_params_as_dict(request: Request) -> Dict[Any, Any]:
    query_params: Dict[Any, Any] = {}
    for key, value in request.query_params.items():
        values_as_list = request.query_params.getlist(key)
        if len(values_as_list) > 1:
            query_params[key] = values_as_list
            continue
        query_params[key] = value
    return query_params


class FastApiHttpServer:
    def __init__(self, server=uvicorn, app=FastAPI()) -> None:
        self._app = app
        self._server = server

    def serve(self, port: int = 8000) -> None:
        self._server.run(self._app, port=port)

    def on(self, method: str, url: str, controller: Controller) -> None:
        async def fastapi_controller(
            request: Request, params: Dict[Any, Any] = Depends(get_query_params_as_dict)
        ) -> Any:
            application_request = HttpRequest(
                headers={**request.headers},
                body=await self.__get_body(request),
                params=params,
            )
            response = await controller.handle(application_request)
            return JSONResponse(
                content=response.body,
                status_code=response.status_code,
            )

        def asdf(name: str = "any valid name") -> str:
            return name

        self._app.add_api_route(
            path=url,
            endpoint=fastapi_controller,
            methods=[method.upper()],
            # dependencies=[Depends(lambda: None)],
        )

    async def __get_body(self, request: Request) -> Dict[Any, Any]:
        with contextlib.suppress(json.decoder.JSONDecodeError):
            data = await request.json()
            return data
        return {}
