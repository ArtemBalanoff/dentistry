import pytest
from jsonschema import ValidationError, validate


def validate_schema(instance, schema):
    try:
        validate(instance=instance, schema=schema)
    except ValidationError as e:
        pytest.fail(f'JSON схема не соответствует ожидаемой: {e}')


def generate_phone_number():
    phone_int = 10 ** 9
    while True:
        phone_int += 1
        yield '8' + str(phone_int)
