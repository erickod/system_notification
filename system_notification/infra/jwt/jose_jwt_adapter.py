import contextlib
from typing import Dict

from jose import jwt
from system_notification.config import SETTINGS
from system_notification.domain.protocols.jwt_adapter_protocol import JWT_TYPES


class JoseJWTAdapter:
    def __init__(
        self, *, secret: str = SETTINGS.get("SECRET", ""), jwt_handler=jwt
    ) -> None:
        self._jwt = jwt_handler
        self._secret = secret

    def encode(self, data: Dict[JWT_TYPES, JWT_TYPES]) -> str:
        return self._jwt.encode(data, self._secret, algorithm="HS256")

    def decode(
        self, data: str, verify_signature: bool = True
    ) -> Dict[JWT_TYPES, JWT_TYPES]:
        return self._jwt.decode(
            data, self._secret, options={"verify_signature": verify_signature}
        )

    def is_valid(self, data: str, verify_signature: bool = True) -> bool:
        with contextlib.suppress(Exception) as e:
            self.decode(data, verify_signature)
            return True
        return False
