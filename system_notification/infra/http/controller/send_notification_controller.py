from copy import deepcopy
from dataclasses import asdict

from system_notification.application.send_notification_usecase.send_notification_usecase import (
    SendNotificationInput,
    SendNotificationUseCase,
)
from system_notification.domain.exceptions.notification_error import TargetNotFound
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols.controller_protocol import HttpServer
from system_notification.infra.http.server.helpers.http_request import HttpRequest
from system_notification.infra.http.server.helpers.http_response import HttpResponse
from tests.infra.http.controller.api_notification_serializer import (
    ApiNotificationSerializer,
)


class SendNotificationController:
    http_server: HttpServer

    def __init__(
        self,
        http_server: HttpServer,
        send_notifcation_usecase: SendNotificationUseCase,
        serializer: ApiNotificationSerializer,
    ) -> None:
        self.http_server = http_server
        self.send_notification = send_notifcation_usecase
        self.serializer = serializer
        self.http_server.on("POST", "/notification", self)

    async def handle(self, request: HttpRequest) -> HttpResponse:
        self.serializer.from_dict(request.body)
        input_errors = deepcopy(self.serializer.errors)
        if not self.serializer.is_valid:
            return HttpResponse(status_code=400, body=input_errors)
        try:
            return await self._handle(request)
        except TargetNotFound as err:
            return HttpResponse(status_code=400, body={"error": err.args})
        except Exception as err:
            return HttpResponse(status_code=500, body={"error": err.args})

    async def _handle(self, request: HttpRequest) -> HttpResponse:
        notification = request.body.get("data", {})
        first_target = notification.get("destin", [])[0]
        input = SendNotificationInput(
            title=notification.get("title"),
            content=notification.get("content"),
            priority=notification.get("priority", 0),
            target=NotificationTarget(
                _type=first_target.get("type"), _target=first_target.get("target")
            ),
        )
        output = await self.send_notification.execute(input)
        return HttpResponse(
            status_code=202,
            body={
                "data": {
                    "notification_sent": output.sent,
                    "sent_to": asdict(output.target),
                }
            },
        )
