import pytest
from src.company_account import CompanyAccount


class TestCompanyAccount:

    def test_company_account_create(self, mocker):
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.json.return_value = {
            "result": {
                "subject": {
                    "name": "Firma Testowa",
                    "nip": "0123456789",
                    "statusVat": "Czynny"
                }
            }
        }

        company = CompanyAccount("company Inc.", "0123456789")

        assert company.name == "company Inc."
        assert len(company.nip) == 10

        mock_get.assert_called_once()


        company = CompanyAccount("company Inc.", "01234567891")
        assert company.nip == "INVALID"

    def test_create_account_not_registered(self, mocker):
        # Symulujemy odpowiedź, że firma nie istnieje
        mock_get = mocker.patch('requests.get')
        mock_get.return_value.json.return_value = {
            "result": {"subject": None}
        }

        # Oczekujemy błędu ValueError
        with pytest.raises(ValueError, match="Company not registered!!"):
            CompanyAccount("Mafia", "8461627563")


    def test_outcoming_transfer(self):
        company = CompanyAccount("Firma", "12345678901")
        company.balance = 100
        company.outcoming_transfer(20)
        assert company.balance == 80

    def test_incoming_transfer(self):
        company = CompanyAccount("Firma", "12345678901")
        company.balance = 100
        company.incoming_transfer(20)
        assert company.balance == 120

    def test_express_outcoming_transfer(self):
        company = CompanyAccount("Firma", "12345678901")
        company.balance = 1000
        company.express_outcoming_transfer(500)
        assert company.balance == 495