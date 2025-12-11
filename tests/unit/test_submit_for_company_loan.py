import pytest
from src.company_account import CompanyAccount


# 1. Dodajemy 'mocker' jako argument do fixtury
@pytest.fixture
def company_account(mocker):
    # 2. "Zatykamy" metodę sprawdzającą NIP.
    # Mówimy: "Dla klasy CompanyAccount, metoda check_status_Vat ma zawsze zwracać True"
    mocker.patch.object(CompanyAccount, 'check_status_Vat', return_value=True)

    # 3. Teraz możemy bezpiecznie utworzyć obiekt, nawet ze zmyślonym NIPem
    return CompanyAccount("John Inc.", "0000000000")


def test_not_enough_balance_for_loan(company_account):
    company_account.operations = [-1775]
    company_account.balance = 1000
    # Upewnij się, że masz metodę take_loan w klasie CompanyAccount!
    assert company_account.take_loan(10000) == False


def test_no_transfer_to_zus(company_account):
    company_account.balance = 1000
    # Pusta lista operacji (brak ZUS)
    company_account.operations = []
    assert company_account.take_loan(100) == False


def test_positive_company_loan(company_account):
    company_account.balance = 1000
    # Zakładamy, że -1775 to przelew do ZUS
    company_account.operations = [-1775]

    assert company_account.take_loan(500)