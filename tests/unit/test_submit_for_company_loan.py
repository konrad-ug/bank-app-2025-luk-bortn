import pytest
from src.company_account import CompanyAccount



@pytest.fixture
def company_account():
    return CompanyAccount("John Inc.", "0000000000")



def test_not_enough_balance_for_loan(company_account):
    company_account.operations = [-1775]
    company_account.balance = 1000

    assert company_account.take_loan(10000) == False


def test_no_transfer_to_zus(company_account):
    company_account.balance = 1000
    assert company_account.take_loan(100) == False


def test_positive_company_loan(company_account):
    company_account.balance = 1000
    company_account.operations = [-1775]

    assert company_account.take_loan(500)