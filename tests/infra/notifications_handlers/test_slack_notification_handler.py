from typing import Any, Dict, Tuple, Union

import pytest
from slack_sdk.errors import SlackApiError

from system_notification.domain.exceptions.notification_error import TargetNotFound
from system_notification.domain.notifications import BaseNotification
from system_notification.domain.notifications.notification_target import (
    NotificationTarget,
)
from system_notification.infra.notification_handlers import SlackNotificationHandler

token = "ANY VALID SLACK API TOKEN"
notification = BaseNotification(title="My Notification", content="Thats works!")
notification.add_target(NotificationTarget("slack_channel", "tech_logs"))


class SlackFakeClient:
    def __init__(
        self,
        as_success: bool = True,
        raises_with: Union[Tuple[str, Dict[str, str]], Tuple] = (),
    ) -> None:
        self.raises_with = raises_with
        self.as_success = as_success
        self.chat_postMessage_is_called: bool = False

    def chat_postMessage(self, *args, **kwargs) -> Dict[str, Any]:
        if len(self.raises_with) >= 2:
            raise SlackApiError(
                message=self.raises_with[0], response=self.raises_with[1]
            )
        self.chat_postMessage_is_called = True
        return {"ok": self.as_success}

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self


async def test_instantiation_params():
    client = SlackFakeClient()
    sut = SlackNotificationHandler(token=token, client=client)
    assert sut._token == token
    assert sut._client is client


async def test_ensure_send_method_calls_chat_postMessage_from_client():
    client = SlackFakeClient(as_success=True)
    sut = SlackNotificationHandler(token=token, client=client)
    await sut.send(notification)
    assert client.chat_postMessage_is_called
    assert notification.is_sent


async def test_when_the_server_responded_with_an_error_the_handler_should_raises_RuntimeError():
    client = SlackFakeClient(as_success=True, raises_with=("token_error", {}))
    sut = SlackNotificationHandler(token=token, client=client)
    with pytest.raises(TargetNotFound) as e:
        await sut.send(notification)
