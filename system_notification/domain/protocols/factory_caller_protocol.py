from typing import Literal, Optional, Protocol

from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols.notification_factory_protocol import (
    NotificationFactory,
)
from system_notification.domain.protocols.notification_protocol import Notification
from system_notification.domain.protocols.notification_sender import NotificationSender


class FactoryCaller(Protocol):
    def add_factory(self, factory: NotificationFactory) -> None:
        pass

    async def get_sender(self, target: NotificationTarget) -> Optional[NotificationSender]:
        pass

    async def get_notification(
        self,
        title: str,
        content: str,
        destin: NotificationTarget,
        priority: Literal[0, 1, 2, 3] = 0,
    ) -> Optional[Notification]:
        pass
