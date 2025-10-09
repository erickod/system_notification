from dataclasses import dataclass


@dataclass
class NotificationTarget:
    _type: str
    _target: str

    @property
    def type(self) -> str:
        return str(self._type).lower()

    @property
    def target(self) -> str:
        return str(self._target).lower()

    def __str__(self) -> str:
        return f"{self.type}:{self.target}"
