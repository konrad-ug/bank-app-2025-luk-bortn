import pytest
from src.AccountRegistry import AccountRegistry
from src.account import Account
@pytest.fixture
def account_registry():
    return AccountRegistry()

def test_account_registry(account_registry):
    assert account_registry.accounts == []

def test_add_account(account_registry):
    account = Account("john", "doe", "00000000000", "promo-code")
    account_registry.add_account(account)
    assert account_registry.accounts == [account]


def test_get_account_by_pesel_found(account_registry):
    account = Account("john", "doe", "00000000000", "promo-code")
    account_registry.add_account(account)
    assert account_registry.get_account_by_pesel("00000000000") == account

def test_get_account_by_pesel_not_found(account_registry):
    account = Account("john", "doe", "00000000000", "promo-code")
    account_registry.add_account(account)
    assert account_registry.get_account_by_pesel("00000000001") is None


def test_get_all_accounts(account_registry):
    account = Account("john", "doe", "00000000000", "promo-code")
    account_registry.add_account(account)
    assert account_registry.get_all_accounts() == [account]


def test_number_of_accounts(account_registry):
    account_1 = Account("john", "doe", "00000000000", "promo-code")
    account_2 = Account("john", "Marston", "00000000001", "promo-code")
    account_registry.accounts = [account_1, account_2]
    assert account_registry.number_of_accounts() == 2