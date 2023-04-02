from unittest.mock import AsyncMock, Mock

from system_notification.application.send_notification_usecase.send_notification_usecase import (
    SendNotificationInput,
)
from system_notification.domain.exceptions.notification_error import TargetNotFound
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.domain.protocols.controller_protocol import Controller
from system_notification.infra.http.controller.send_notification_controller import (
    SendNotificationController,
)
from system_notification.infra.http.server.helpers.http_request import HttpRequest

payload = {
    "data": {
        "title": "What is Lorem Ipsum?",
        "content": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. ",
        "destin": [{"type": "slack_channel", "target": "tech_logs"}],
        "priority": 0,
    }
}


def undecorate_controller(instance: Controller) -> Controller:
    undecorated_method = getattr(instance.handle, "__wrapped__")
    setattr(instance, "handle", undecorated_method)
    return instance


async def test_instantiation_params() -> None:
    http_server = Mock()
    send_notifcation_usecase = AsyncMock()
    serializer = Mock()
    sut = SendNotificationController(
        http_server=http_server,
        send_notifcation_usecase=send_notifcation_usecase,
        serializer=serializer,
    )
    assert sut.http_server is http_server
    assert sut.send_notification is send_notifcation_usecase
    assert sut.serializer is serializer


async def test_ensure_handle_calls_serialize_from_dict_method() -> None:
    http_server = Mock()
    send_notifcation_usecase = AsyncMock()
    serializer = Mock()
    sut = SendNotificationController(
        http_server=http_server,
        send_notifcation_usecase=send_notifcation_usecase,
        serializer=serializer,
    )
    undecorate_controller(sut)
    await sut.handle(sut, HttpRequest(headers={}, body={}, params={}))
    serializer.from_dict.assert_called()


async def test_ensure_return_400_when_serialize_has_errors() -> None:
    http_server = Mock()
    send_notifcation_usecase = AsyncMock()
    serializer = Mock()
    serializer.is_valid = False
    sut = SendNotificationController(
        http_server=http_server,
        send_notifcation_usecase=send_notifcation_usecase,
        serializer=serializer,
    )
    undecorate_controller(sut)
    response = await sut.handle(sut, HttpRequest(headers={}, body={}, params={}))
    assert response.status_code == 400


async def test_ensure_usecase_is_called_with_right_params() -> None:
    http_server = Mock()
    send_notifcation_usecase = AsyncMock()
    serializer = Mock()
    serializer.is_valid = True
    sut = SendNotificationController(
        http_server=http_server,
        send_notifcation_usecase=send_notifcation_usecase,
        serializer=serializer,
    )
    undecorate_controller(sut)
    await sut.handle(sut, HttpRequest(headers={}, body=payload, params={}))
    send_notifcation_usecase.execute.assert_called_with(
        SendNotificationInput(
            title="What is Lorem Ipsum?",
            content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. ",
            target=[NotificationTarget(_type="slack_channel", _target="tech_logs")],
            priority=0,
            placeholders={},
        )
    )


async def test_return_when_occur_target_error() -> None:
    def execute(*args, **kwargs):
        raise TargetNotFound({})

    send_notifcation_usecase = AsyncMock()
    send_notifcation_usecase.execute.side_effect = execute
    sut = SendNotificationController(
        http_server=Mock(),
        send_notifcation_usecase=send_notifcation_usecase,
        serializer=Mock(),
    )
    undecorate_controller(sut)
    await sut.handle(sut, HttpRequest(headers={}, body=payload, params={}))
    send_notifcation_usecase.execute.assert_called_with(
        SendNotificationInput(
            title="What is Lorem Ipsum?",
            content="Lorem Ipsum is simply dummy text of the printing and typesetting industry. ",
            target=[NotificationTarget(_type="slack_channel", _target="tech_logs")],
            priority=0,
            placeholders={},
        )
    )
