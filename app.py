import os

from fastapi import FastAPI
from mangum import Mangum

from system_notification.application.send_notification_usecase.send_notification_usecase import (
    SendNotificationUseCase,
)
from system_notification.config.config import SETTINGS
from system_notification.domain.notification_factory_caller import (
    NotificationFactoryCaller,
)
from system_notification.domain.notifications.factories.slack_notification_factory import (
    SlackNotificationFactory,
)
from system_notification.infra.http.controller.health_check_controller import (
    HealthCheckController,
)
from system_notification.infra.http.controller.send_notification_controller import (
    SendNotificationController,
)
from system_notification.infra.http.server.fastapi_http_server import FastApiHttpServer
from system_notification.infra.http.server.flask_http_server import FlaskHttpServer
from tests.infra.http.controller.api_notification_serializer import (
    ApiNotificationSerializer,
)

server = FastApiHttpServer(app=FastAPI(root_path=f"/{os.environ.get('STAGE', '')}"))
# server = FlaskHttpServer()
factory_caller = NotificationFactoryCaller()
factory_caller.add_factory(
    SlackNotificationFactory(slack_token=SETTINGS.get("SLACK_API_TOKEN", ""))
)
uc = SendNotificationUseCase(factory_caller=factory_caller)
send_notification_controller = SendNotificationController(
    http_server=server,
    send_notifcation_usecase=uc,
    serializer=ApiNotificationSerializer(),
)
health_check_controller = HealthCheckController(
    http_server=server,
)
handler = Mangum(server._app)
if __name__ == "__main__":
    server.serve(port=5000)
