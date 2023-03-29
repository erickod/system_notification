import pytest

from system_notification.domain import BaseNotification
from system_notification.domain.notifications import NotificationTarget

title = "My Notification"
vars = {"full_name": "John Duo"}
content = "Hello, {full_name}! This is a basic notification"
final_text = "Hello, John Duo! This is a basic notification"


@pytest.mark.parametrize(
    ["priority", "expected_priority"],
    [("Any value different from int", 0), (None, 0), (0, 0), (1, 1), (2, 2), (3, 3)],
)
async def test_instatiation_params(priority, expected_priority) -> None:
    sut = BaseNotification(title=title, content=content, priority=priority)
    assert sut.title == title
    assert sut.content == content
    assert sut.is_sent == False
    assert sut.priority == expected_priority
    assert sut.vars == {}
    with pytest.raises(NotImplementedError):
        assert sut.is_scheduled == False


async def test_mark_as_sent_method() -> None:
    sut = BaseNotification(title=title, content=content)
    sut.mark_as_sent()
    assert sut.is_sent


async def test_get_text_should_replace_string_placeholders_using_vars_values() -> None:
    sut = BaseNotification(title=title, content=content)
    sut.set_vars(vars)
    assert sut.get_text() == final_text


async def test_get_text_should_not_replace_string_placeholders_when_apply_vars_flag_is_false() -> None:
    sut = BaseNotification(title=title, content=content)
    sut.set_vars(vars)
    assert sut.get_text(apply_vars=False) == content


async def test_get_text_should_return_the_raw_text_if_no_vars_was_setted() -> None:
    sut = BaseNotification(title=title, content=content)
    assert sut.get_text() == content


async def test_add_target() -> None:
    target = NotificationTarget(_type="slack_channel", _target="tech_logs")
    target_not_in_sut = NotificationTarget(_type="any", _target="any")
    sut = BaseNotification(title=title, content=content)
    sut.add_target(target)
    assert target in sut
    assert target_not_in_sut not in sut
    assert sut.target == target
