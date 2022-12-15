import pytest
from pykeychain import AlreadyExistsException, NotFoundException, Storage


@pytest.fixture()
def storage(service, account):
    def _remove_entries(storage, account):
        try:
            storage.delete(account)
        except NotFoundException:
            pass

    storage = Storage(service)
    _remove_entries(storage, account)
    yield storage
    _remove_entries(storage, account)


@pytest.mark.manual
def test_add_item(storage, account):
    storage.save_password(account, "123")
    with pytest.raises(AlreadyExistsException):
        storage.save_password(account, "123")


@pytest.mark.manual
def test_get_item(storage, account):
    with pytest.raises(NotFoundException):
        _ = storage.get_password(account)

    storage.save_password(account, "123")
    assert storage.get_password(account) == "123"


@pytest.mark.manual
def test_delete_item(storage, account):
    with pytest.raises(NotFoundException):
        storage.delete(account)

    storage.save_password(account, "123")
    storage.delete(account)

    with pytest.raises(NotFoundException):
        _ = storage.get_password(account)


@pytest.mark.manual
def test_check_item_exists(storage, account):
    assert not storage.item_exists(account)
    storage.save_password(account, "123")
    assert storage.item_exists(account)
    storage.delete(account)
    assert not storage.item_exists(account)
