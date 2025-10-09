import contextlib
from typing import Dict, Literal, Optional

from system_notification.domain.exceptions.notification_error import TargetNotFound
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols.notification_factory_protocol import (
    NotificationFactory,
)
from system_notification.domain.protocols.notification_protocol import Notification
from system_notification.domain.protocols.notification_sender import NotificationSender


class NotificationFactoryCaller:
    def __init__(self) -> None:
        self._factories: Dict[str, NotificationFactory] = {}

    def add_factory(self, factory: NotificationFactory) -> None:
        self._factories[factory.target_type] = factory

    async def get_sender(self, target: NotificationTarget) -> Optional[NotificationSender]:
        with contextlib.suppress(KeyError):
            factory = self._factories[target.type]
            return factory.make_sender()
        raise TargetNotFound(
            {
                "is_sent": False,
                "destin": {
                    "target_type": target.type,
                    "target": target.target,
                },
                "detail": "unknown_handler",
            }
        )

    async def get_notification(
        self,
        title: str,
        content: str,
        destin: NotificationTarget,
        priority: Literal[0, 1, 2, 3] = 0,
    ) -> Optional[Notification]:
        factory = self._factories[destin.type]
        return factory.make_notificaton(title, content, priority)

    def __len__(self) -> int:
        return len(self._factories.values())
