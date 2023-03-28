import pytest

from system_notification.domain import BaseNotification

title = "My Notification"
content = "Hello! This is a basic notification"


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
