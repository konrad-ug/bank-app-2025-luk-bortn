from src.account import Account
from src.company_account import CompanyAccount
from datetime import date
import pytest

class TestEmailByMocker:

    @pytest.fixture
    def today_str(self):
        return date.today().strftime("%Y-%m-%d")

    def test_email_send_account(self, mocker,today_str):
        mock_get = mocker.patch('src.account.SMTPClient.send')
        mock_get.return_value = False

        account = Account("John","Doe", "12345678901", "")
        account.operations = [1,2,3,4,5]

        assert not account.send_history_via_email("test@email.com")

    def test_personal_account_email_success(self, mocker, today_str):

        mock_send = mocker.patch('src.account.SMTPClient.send')
        mock_send.return_value = True


        history_data = [100, -1, 500]
        account = Account("Jan", "Kowalski", "33333333333", "")
        account.operations = history_data

        email = "jan@nowak.pl"


        result = account.send_history_via_email(email)


        assert result is True
        mock_send.assert_called_once_with(
            f"Account Transfer History {today_str}",
            f"Personal account history: [100, -1, 500]",
            "jan@nowak.pl"
        )

    def test_company_account_email_success(self, mocker, today_str):
        mocker.patch('src.company_account.CompanyAccount.check_status_Vat', return_value=True)

        mock_send = mocker.patch('src.company_account.SMTPClient.send')
        mock_send.return_value = True

        account = CompanyAccount("Firma", "3333333333")
        history_data = [1, 2, -3]
        account.operations = history_data

        email = "jan@nowak.pl"

        result = account.send_history_via_email(email)


        assert result is True
        mock_send.assert_called_once_with(
            f"Account Transfer History {today_str}",
            f"Company account history: [1, 2, -3]",
            "jan@nowak.pl"
        )

    def test_company_account_email_server_error(self, mocker, today_str):
        mocker.patch('src.company_account.CompanyAccount.check_status_Vat', return_value=True)
        mock_send = mocker.patch('src.company_account.SMTPClient.send', return_value=False)

        account = CompanyAccount("Firma", "3333333333")
        result = account.send_history_via_email("jan@nowak.pl")

        assert result is False
        mock_send.assert_called_once()