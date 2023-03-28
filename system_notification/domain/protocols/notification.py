from datetime import datetime
from typing import Any, List, Protocol


class Notification(Protocol):
    @property
    def is_sent(self) -> bool:
        pass

    @property
    def is_scheduled(self) -> bool:
        pass

    def is_scheduled_to(self, date: datetime) -> bool:
        pass

    def schedule(self, date: datetime) -> bool:
        pass

    def can_be_sent_at(self, date: datetime) -> bool:
        pass

    def set_vars(vars: Any) -> None:
        pass

    def get_targets(self) -> List[str]:
        pass

    def get_text(self, apply_vars: bool = True) -> str:
        pass
