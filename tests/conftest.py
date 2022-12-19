import pytest


@pytest.fixture
def account():
    yield "account_name_80241384-0006-492e-8a95-0522699358c1"


@pytest.fixture
def service():
    yield "service_name_80241384-0006-492e-8a95-0522699358c1"


@pytest.fixture
def accounts():
    accounts = []
    for i in range(10):
        accounts.append(f"some_account_{i}")

    accounts.append("pikachu")

    yield accounts
