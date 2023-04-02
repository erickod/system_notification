from typing import Dict, Protocol, TypeVar

JWT_TYPES = TypeVar("JWT_TYPES", str, bytes, int, float)


class JWTAdapter(Protocol):
    def encode(self, data: Dict[JWT_TYPES, JWT_TYPES]) -> str:
        pass

    def decode(
        self, data: str, verify_signature: bool = True
    ) -> Dict[JWT_TYPES, JWT_TYPES]:
        pass

    def is_valid(self, data: str, verify_signature: bool = True) -> bool:
        pass
