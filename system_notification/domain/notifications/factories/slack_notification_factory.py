from typing import Literal

from system_notification.domain.notifications.base_notification import BaseNotification
from system_notification.domain.protocols.notification_protocol import Notification
from system_notification.domain.protocols.notification_sender import NotificationSender
from system_notification.infra.notification_handlers.slack_notification_handler import (
    SlackNotificationHandler,
)


class SlackNotificationFactory:
    target_type = "slack_channel"

    def __init__(self, slack_token: str) -> None:
        self._slack_token = slack_token

    def make_notificaton(
        self, title: str, content: str, priority: Literal[0, 1, 2, 3] = 0
    ) -> Notification:
        return BaseNotification(title=title, content=content, priority=priority)

    def make_sender(self) -> NotificationSender:
        return SlackNotificationHandler(token=self._slack_token)
