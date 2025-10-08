from typing import Literal, Protocol, Tuple

from system_notification.domain.protocols.notification_protocol import Notification
from system_notification.domain.protocols.notification_sender import NotificationSender


class NotificationFactory(Protocol):
    target_type: str

    def make_notificaton(
        self, title: str, content: str, priority: Literal[0, 1, 2, 3] = 0
    ) -> Notification:
        pass

    def make_sender(self) -> NotificationSender:
        pass
