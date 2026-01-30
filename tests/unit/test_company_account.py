import pytest
from src.company_account import CompanyAccount

@pytest.mark.skip(reason="Te testy łączą się z prawdziwym API - wyłączone na rzecz testów z mockami")
class TestCompanyAccount:


    def test_company_account_create(self):
        company = CompanyAccount("company Inc.", "0123456789")
        assert type(company.name) is str
        assert company.name == "company Inc."
        assert type(company.nip) is str
        assert len(company.nip) == 10

        company = CompanyAccount("company Inc.", "01234567891")
        assert company.nip == "INVALID"

    def test_outcoming_transfer(self):
        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.outcoming_transfer(-20)
        assert company.balance == 100

        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.outcoming_transfer(200)
        assert company.balance == 100

        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.outcoming_transfer(20)
        assert company.balance == 80


    def test_incoming_transfer(self):
        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.incoming_transfer(20)
        assert company.balance == 120

        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.incoming_transfer(-20)
        assert company.balance == 100

    def test_express_outcoming_transfer(self):
        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 1000
        company.express_outcoming_transfer(500)

        assert company.balance == 495

        company.balance = 20
        company.express_outcoming_transfer(30)
        assert company.balance == 20

        company.balance = 500
        company.express_outcoming_transfer(-20)
        assert company.balance == 500
