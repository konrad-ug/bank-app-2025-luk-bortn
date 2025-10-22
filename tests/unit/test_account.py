from src.account import Account

class TestAccount:
    def test_account_create(self):
        account = Account("John", "Doe", "12345678910","")
        assert account.first_name == "John" #sprawdzanie imienia
        assert account.last_name == "Doe" # sprawdzanie nazwiska

    def test_balance(self):
        account = Account("John", "Doe", "12345678910", "promo")
        assert type(account.balance) is float  # sprawdzanie balance

    def test_pesel(self):
        account = Account("John", "Doe", "12345678910", "promo")
        assert account.pesel == "12345678910"  # sprawdzanie czy str, tylko cyfry i dlugosc 11

        account = Account("John", "Doe", "123456789101", "promo")
        assert account.pesel == "INVALID"  # sprawdzanie warunku blednego wpisania

    def test_promo_code(self):
        account = Account("John", "Doe", "12345678910","")
        assert account.promo_code is None # promo_code pusty

        account = Account("John", "Doe", "12345678910", "PROM_1234")
        assert account.promo_code is None # promo_code niepoprawny

        account = Account("John", "Doe", "", "PROM_360")
        assert account.promo_code is None # promo_code nie zaakceptowany przez brak wiek peselu

        account = Account("John", "Doe", "59061212345", "PROM_360")
        assert account.promo_code is None # promo_code dla osoby urodzonej poniej niz rok 1960


    def test_outcoming_transfer(self):

        account_1 = Account("John", "Doe", "59061212345", "PROM_360")
        account_1.balance = 100

        account_1.outcoming_transfer(20)

        assert account_1.balance == 80


        account_1 = Account("John", "Doe", "59061212345", "PROM_360")
        account_1.balance = 20
        account_1.outcoming_transfer(30)
        assert account_1.balance == 20

    def test_incoming_transfer(self):
        account_1 = Account("John", "Doe", "59061212345", "PROM_360")
        account_1.balance = 0

        account_1.incoming_transfer(400)
        assert account_1.balance == 400

        account_1.balance = 0

        account_1.incoming_transfer(-20)
        assert account_1.balance == 0

    def test_express_outcoming_transfer(self):
        user = Account("Lukasz", "Bortnowski", "11111111111", "")
        user.balance = 1000
        user.express_outcoming_transfer(500) # 1000 - 505 == 495

        assert user.balance == 499

        user.balance = 20
        user.express_outcoming_transfer(30) #stan konta za maly
        assert user.balance == 20

        user.balance = 500
        user.express_outcoming_transfer(-20) # ujemny transfer srodkow
        assert user.balance == 500

        user.balance = 10
        user.express_outcoming_transfer(10)
        assert user.balance == -1