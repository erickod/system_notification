from dataclasses import dataclass, field
from typing import Dict, List, Literal, Optional

from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols import NotificationSender
from system_notification.domain.protocols.factory_caller_protocol import FactoryCaller
from system_notification.domain.protocols.notification_protocol import Notification
from system_notification.domain.exceptions.notification_error import TargetNotFound



@dataclass
class SendNotificationInput:
    title: str
    content: str
    target: List[NotificationTarget] = field(default_factory=list)
    priority: Literal[0, 1, 2, 3] = 0
    placeholders: Dict[str, str] = field(default_factory=dict)
    icon: str = ""


@dataclass
class SendNotificationOutput:
    status: str
    target: Optional[NotificationTarget] = None


class SendNotificationUseCase:
    def __init__(self, factory_caller: FactoryCaller) -> None:
        self._factory_caller = factory_caller

    async def execute(
        self, input: SendNotificationInput
    ) -> List[SendNotificationOutput]:
        output: List[SendNotificationOutput] = []
        if not input.target:
            raise TargetNotFound(
                {
                    "is_sent": False,
                    "detail": "missing at least one target"
                }
            )
        for target in input.target:
            sender: Optional[
                NotificationSender
            ] = await self._factory_caller.get_sender(target=target)
            notification: Optional[
                Notification
            ] = await self._factory_caller.get_notification(
                input.title, input.content, target, input.priority
            )
            assert sender
            assert notification
            # TODO: create test to ensure notification.add_target is called with each target item from targets
            notification.add_target(target=target)
            notification.set_vars(input.placeholders)
            notification.icon = input.icon
            await sender.send(notification)
            output.append(
                SendNotificationOutput(status=notification.status, target=target)
            )
        return output
