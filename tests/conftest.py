import pytest


@pytest.fixture
def account():
    yield "account_name_80241384-0006-492e-8a95-0522699358c1"


@pytest.fixture
def service():
    yield "service_name_80241384-0006-492e-8a95-0522699358c1"
