from typing import Literal

from system_notification.application import SendNotificationUseCase
from system_notification.application.send_notification_usecase import (
    SendNotificationInput,
)
from system_notification.domain.notification_factory_caller import (
    NotificationFactoryCaller,
)
from system_notification.domain.notifications.base_notification import BaseNotification
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols.notification_protocol import Notification
from system_notification.domain.protocols.notification_sender import NotificationSender


class FakeNotificationSender:
    def __init__(self) -> None:
        self.send_is_called: bool = False
        self.notification: Notification
        self.target_type: str = "testing"

    async def send(self, notification: Notification) -> None:
        self.notification = notification
        self.send_is_called = True


class FakeTestingFactory:
    def __init__(self, sender: NotificationSender) -> None:
        self.target_type: str = "testing"
        self.sender = sender

    def make_notificaton(
        self, title: str, content: str, target: str, priority: Literal[0, 1, 2, 3] = 0
    ) -> Notification:
        return BaseNotification(title=title, content=content, priority=priority)

    def make_sender(self) -> NotificationSender:
        return self.sender


async def test_ensure_execute_calls_send_from_sender() -> None:
    input = SendNotificationInput(
        title="Any Title",
        content="Any Content",
        target=NotificationTarget("testing", "#123"),
    )
    sender = FakeNotificationSender()
    notification_factory_caller = NotificationFactoryCaller()
    notification_factory_caller.add_factory(FakeTestingFactory(sender))
    sut = SendNotificationUseCase(factory_caller=notification_factory_caller)
    await sut.execute(input)
    assert sender.send_is_called