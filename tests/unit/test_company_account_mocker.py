import pytest
from src.company_account import CompanyAccount


class TestCompanyAccount:

    def test_company_account_create(self, mocker):
        # 1. Mockujemy API dla poprawnego NIPu (10 znaków)
        # Dzięki temu test nie łączy się z internetem
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

        # 2. Tworzymy konto (konstruktor zadzwoni do "fałszywego" API)
        company = CompanyAccount("company Inc.", "0123456789")

        assert company.name == "company Inc."
        assert len(company.nip) == 10
        # Sprawdzamy, czy mock został wywołany
        mock_get.assert_called_once()

        # 3. Przypadek błędnej długości (API nie jest wołane)
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

    # --- Testy metod finansowych ---
    # Używamy błędnego NIPu (11 znaków), żeby nie musieć mockować API w każdym teście

    def test_outcoming_transfer(self):
        company = CompanyAccount("Firma", "12345678901")  # INVALID NIP
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