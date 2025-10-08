from system_notification.domain.notifications import NotificationTarget


async def test_notification_target_instantiation_parmas() -> None:
    sut = NotificationTarget(_type="slack_channel", _target="tech_logs")
    assert sut.target == "tech_logs"
    assert sut.type == "slack_channel"
