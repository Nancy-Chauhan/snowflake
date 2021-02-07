from datetime import datetime

import pytest

from snowflake import app as flask_app
from snowflake.models import User
from snowflake.schemas.login import LoginSchema, LoginResponseSchema


@pytest.fixture(scope="module", autouse=True)
def app():
    yield flask_app


def test_login_schema_reads_correct_json():
    schema = LoginSchema()

    json = r'{ "token": "12345" }'

    login = schema.loads(json)

    expected = {"token": "12345"}

    assert login == expected


def test_login_response_schema_dumps_correct_json():
    schema = LoginResponseSchema()
    user = User(id='12345', name='Hello', designation='Developer',
                team_name='Engineering', username='hello',
                email='hello@example.com',
                profile_pic='https://example.com/picture.jpg')

    time = datetime.now()
    login = schema.dump({
        'token': '12345',
        'expiry': time,
        'refresh_token': '12345',
        'user': user
    })

    expected = {
        "token": "12345",
        "refreshToken": "12345",
        "expiry": time.isoformat(),
        "user": {
            'name': 'Hello',
            'designation': 'Developer',
            'teamName': 'Engineering',
            'username': 'hello',
            'email': 'hello@example.com',
            'profilePic': 'https://example.com/picture.jpg'
        }
    }

    assert login == expected