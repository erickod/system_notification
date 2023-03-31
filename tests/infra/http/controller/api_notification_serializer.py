import json
from typing import Any, Dict, List, Optional

import pydantic


class Destin(pydantic.BaseModel):
    type: str
    target: str


class Notification(pydantic.BaseModel):
    title: str
    content: str
    destin: List[Destin]
    priority: int = 0


class APINotification(pydantic.BaseModel):
    data: Notification


class ApiNotificationSerializer:
    def __init__(self) -> None:
        self.errors = {}

    def from_raw(self, input: str | bytes) -> Optional[APINotification]:
        try:
            return APINotification.parse_raw(input)
        except pydantic.error_wrappers.ValidationError as err:
            self.errors = json.loads(err.json())
        return None

    def from_dict(self, input: Dict[str, Any]) -> Optional[APINotification]:
        try:
            return APINotification.parse_obj(input)
        except pydantic.error_wrappers.ValidationError as err:
            self.errors = json.loads(err.json())
        return None

    def to_dict(self, input: APINotification) -> Optional[APINotification]:
        try:
            return input.json()
        except pydantic.error_wrappers.ValidationError as err:
            self.errors = json.loads(err.json())
        return None

    @property
    def is_valid(self) -> bool:
        is_valid = not bool(self.errors)
        self.errors = {}
        return is_valid
