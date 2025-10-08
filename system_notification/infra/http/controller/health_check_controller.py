from system_notification.domain.protocols.controller_protocol import HttpServer
from system_notification.infra.http.server.helpers.http_request import HttpRequest
from system_notification.infra.http.server.helpers.http_response import HttpResponse


class HealthCheckController:
    http_server: HttpServer

    def __init__(
        self,
        http_server: HttpServer,
    ) -> None:
        self.http_server = http_server
        self.http_server.on(method="GET", url="/healthz", controller=self)

    async def handle(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(body="OK")
