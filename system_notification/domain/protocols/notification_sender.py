from typing import Protocol, runtime_checkable

from system_notification.domain.protocols.notification_protocol import Notification


@runtime_checkable
class NotificationSender(Protocol):
    target_type: str

    async def send(self, notification: Notification) -> None:
        pass
