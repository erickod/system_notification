from dataclasses import dataclass, field
from typing import Dict, Literal, Optional

from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols import NotificationSender
from system_notification.domain.protocols.factory_caller_protocol import FactoryCaller
from system_notification.domain.protocols.notification_protocol import Notification


@dataclass
class SendNotificationInput:
    title: str
    content: str
    target: NotificationTarget
    priority: Literal[0, 1, 2, 3] = 0
    placeholders: Dict[str, str] = field(default_factory=dict)


@dataclass
class SendNotificationOutput:
    sent: bool
    target: Optional[NotificationTarget] = None


class SendNotificationUseCase:
    def __init__(self, factory_caller: FactoryCaller) -> None:
        self._factory_caller = factory_caller

    async def execute(self, input: SendNotificationInput) -> SendNotificationOutput:
        sender: Optional[NotificationSender] = await self._factory_caller.get_sender(
            target=input.target
        )
        notification: Optional[
            Notification
        ] = await self._factory_caller.get_notification(
            input.title, input.content, input.target, input.priority
        )
        assert sender
        assert notification
        notification.add_target(target=input.target)
        notification.set_vars(input.placeholders)
        await sender.send(notification)
        return SendNotificationOutput(False)
