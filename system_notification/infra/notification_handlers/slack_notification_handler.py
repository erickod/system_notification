from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from system_notification.domain.exceptions.notification_error import TargetNotFound
from system_notification.domain.notifications.base_notification import BaseNotification


class SlackNotificationHandler:
    def __init__(self, token: str, client=WebClient) -> None:
        self._token = token
        self._client = client(token=token)
        self.target_type = "slack_channel"

    async def send(self, notification: BaseNotification) -> None:
        # TODO: find a way to notification make a self validation
        assert notification.target, "O target da notificação não pode estar vazio"
        try:
            channel = notification.target.target
            response = self._client.chat_postMessage(
                channel=f"#{channel}",
                text=notification.get_text(),
                username=notification.title,
                # icon_emoji=":blush:",
            )
            assert response["ok"]
        except SlackApiError as err:
            raise TargetNotFound(
                {
                    "is_sent": False,
                    "destin": {
                        "target_type": notification.target.type,
                        "target": notification.target.target,
                    },
                    "detail": err.response.get("error", "unknow error"),
                }
            )
        notification.mark_as_sent()
