from unittest import mock

import pytest
import sh
from pykeychain import AlreadyExistsException, NotFoundException, Storage


@pytest.fixture()
def storage(service, account):
    yield Storage(service)


@pytest.fixture()
def patched_security():
    with mock.patch("sh.security", create=True) as patched_security:
        yield patched_security


def test_add_item(patched_security, storage, account):
    storage.save_password(account, "123")


def test_add_existing_item(patched_security, storage, account):
    patched_security.side_effect = sh.ErrorReturnCode_45("", b"", b"")
    with pytest.raises(AlreadyExistsException):
        storage.save_password(account, "123")


def test_get_not_existed_item(patched_security, storage, account):
    patched_security.side_effect = sh.ErrorReturnCode_44("", b"", b"")

    with pytest.raises(NotFoundException):
        _ = storage.get_password(account)


def test_get_item(patched_security, storage, account):
    def set_command_output(_cmd, _flag, s, a, _out):
        _out.write("123\n")

    patched_security.side_effect = set_command_output
    assert storage.get_password(account) == "123"


def test_delete_not_existed_item(patched_security, storage, account):
    patched_security.side_effect = sh.ErrorReturnCode_44("", b"", b"")

    with pytest.raises(NotFoundException):
        storage.delete(account)


def test_delete_item(patched_security, storage, account):
    storage.delete(account)


def test_check_not_existend_item_exists(patched_security, storage, account):
    patched_security.side_effect = sh.ErrorReturnCode_44("", b"", b"")

    assert not storage.item_exists(account)


def test_check_item_exists(patched_security, storage, account):
    assert storage.item_exists(account)
