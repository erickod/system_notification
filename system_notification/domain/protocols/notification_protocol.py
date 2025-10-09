from datetime import datetime
from typing import Any, Dict, List, Protocol, runtime_checkable


@runtime_checkable
class Notification(Protocol):
    @property
    def vars(self) -> Dict[str, str]:
        pass

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

    def set_vars(self, vars: Dict[str, str]) -> None:
        pass

    def get_targets(self) -> List[str]:
        pass

    def get_text(self, apply_vars: bool = True) -> str:
        pass
