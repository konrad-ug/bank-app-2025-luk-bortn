import pytest
from src.account import Account



@pytest.fixture
def account():
    return Account("John", "Doe", "00000000000", "_360")

def test_submit_for_loan_last_three_positive(account):
    account.operations = [1,2,3]
    assert account.submit_for_loan(1000.0) == True
    assert account.loan == 1000.0
    assert account.balance == 1000.0

def test_submit_for_loan_last_three_negative(account):
    account.operations = [300, 400, 500, -600, -1000]
    assert account.submit_for_loan(300.0) == False
    assert account.loan == 0
    assert account.balance == 0

def test_submit_for_loan_last_five_sum_bigger_than_amount_positive(account):
    account.operations = [1,2,3,-4,5]
    assert account.submit_for_loan(2.0) == True
    assert account.loan == 2.0
    assert account.balance == 2.0