import pytest

from system_notification.domain.exceptions.notification_error import TargetNotFound
from system_notification.domain.notification_factory_caller import (
    NotificationFactoryCaller,
)
from system_notification.domain.notifications.base_notification import BaseNotification
from system_notification.domain.notifications.factories.slack_notification_factory import (
    SlackNotificationFactory,
)
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.infra.notification_handlers.slack_notification_handler import (
    SlackNotificationHandler,
)


async def test_ensure_has_no_factory_registered_at_instantiation_time():
    sut = NotificationFactoryCaller()
    assert len(sut) == 0


async def test_registering_a_factory():
    sut = NotificationFactoryCaller()
    sut.add_factory(SlackNotificationFactory(slack_token="any valid token"))
    assert len(sut) == 1


async def test_raises_TargetNotFound_at_get_an_unknown_sender():
    sut = NotificationFactoryCaller()
    sut.add_factory(SlackNotificationFactory(slack_token="any valid token"))

    with pytest.raises(TargetNotFound):
        await sut.get_sender(
            NotificationTarget(_type="any unknown target", _target="123")
        )


async def test_can_recover_a_sender():
    sut = NotificationFactoryCaller()
    sut.add_factory(SlackNotificationFactory(slack_token="any valid token"))
    sender = await sut.get_sender(
        NotificationTarget(_type="slack_channel", _target="123")
    )
    assert type(sender) is SlackNotificationHandler


async def test_make_a_notification():
    sut = NotificationFactoryCaller()
    sut.add_factory(SlackNotificationFactory(slack_token="any valid token"))
    notification = await sut.get_notification(
        title="title",
        content="content",
        destin=NotificationTarget(_type="slack_channel", _target="123"),
    )
    assert type(notification) is BaseNotification
