from system_notification.infra.jwt import JoseJWTAdapter


async def test_instantiation_parms() -> None:
    secret = "any valid secret"
    sut = JoseJWTAdapter(secret=secret)
    assert sut._secret is secret


async def test_encode_decode_methods() -> None:
    secret = "any valid secret"
    sut = JoseJWTAdapter(secret=secret)
    decoded_data = {"type": "str", "content": "Any value"}
    encoded_data = sut.encode(decoded_data)
    assert sut.decode(encoded_data) == decoded_data


async def test_is_valid_should_return_true_when_jwt_is_valid() -> None:
    secret = "any valid secret"
    sut = JoseJWTAdapter(secret=secret)
    decoded_data = {"type": "str", "content": "Any value"}
    encoded_data = sut.encode(decoded_data)
    assert sut.is_valid(encoded_data)


async def test_is_valid_should_return_false_when_jwt_is_invalid() -> None:
    secret = "any valid secret"
    sut = JoseJWTAdapter(secret=secret)
    decoded_data = {"type": "str", "content": "Any value"}
    encoded_data = sut.encode(decoded_data)
    assert not sut.is_valid(encoded_data + "asdf")
