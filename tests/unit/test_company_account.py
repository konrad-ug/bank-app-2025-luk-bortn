from src.company_account import CompanyAccount

class TestCompanyAccount:

    def test_company_account_create(self):
        company = CompanyAccount("company Inc.", "0123456789")
        assert type(company.name) is str
        assert company.name == "company Inc."
        assert type(company.nip) is str
        assert len(company.nip) == 10

        company = CompanyAccount("company Inc.", "01234567891") #dlugosc nieprawidowa
        assert company.nip == "INVALID"

    def test_outcoming_transfer(self):
        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.outcoming_transfer(-20)
        assert company.balance == 100 # zla kwota przelewu

        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.outcoming_transfer(200)
        assert company.balance == 100 # kwota za duza

        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.outcoming_transfer(20)
        assert company.balance == 80 #dobry warunek


    def test_incoming_transfer(self):
        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.incoming_transfer(20)
        assert company.balance == 120 #dobry warunek

        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 100
        company.incoming_transfer(-20)
        assert company.balance == 100 # zla kwota przelewu

    def test_express_outcoming_transfer(self):
        company = CompanyAccount("company Inc.", "01234567891")
        company.balance = 1000
        company.express_outcoming_transfer(500) # 1000 - 505 == 495

        assert company.balance == 495

        company.balance = 20
        company.express_outcoming_transfer(30) #stan konta za maly
        assert company.balance == 20

        company.balance = 500
        company.express_outcoming_transfer(-20) # ujemny transfer srodkow
        assert company.balance == 500

        company.balance = 10
        company.express_outcoming_transfer(10) # warunek z dlugiem
        assert company.balance == -5