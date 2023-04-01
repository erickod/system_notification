import json
from typing import Any, Dict, List, Optional

import pydantic


class DestinSchema(pydantic.BaseModel):
    type: str
    target: str


class NotificationSchema(pydantic.BaseModel):
    title: str
    content: str
    destin: List[DestinSchema]
    priority: int = 0
    placeholders: Dict[str, str] = {}


class APINotificationSchema(pydantic.BaseModel):
    data: NotificationSchema


class ApiNotificationSerializer:
    def __init__(self) -> None:
        self.errors = {}

    def from_raw(self, input: str | bytes) -> Optional[APINotificationSchema]:
        try:
            return APINotificationSchema.parse_raw(input)
        except pydantic.error_wrappers.ValidationError as err:
            self.errors = json.loads(err.json())
        return None

    def from_dict(self, input: Dict[str, Any]) -> Optional[APINotificationSchema]:
        try:
            return APINotificationSchema.parse_obj(input)
        except pydantic.error_wrappers.ValidationError as err:
            self.errors = json.loads(err.json())
        return None

    def to_dict(self, input: APINotificationSchema) -> Optional[APINotificationSchema]:
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
