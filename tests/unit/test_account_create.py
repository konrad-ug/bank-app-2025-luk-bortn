from src.account import Account

class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678910","")
        assert account.first_name == "John" #sprawdzanie imienia
        assert account.last_name == "Doe" # sprawdzanie nazwiska


    def test_balance(self):
        account = Account("John", "Doe", "12345678910","promo")
        assert type(account.balance) is float # sprawdzanie balance

    def test_pesel(self):
        account = Account("John", "Doe", "12345678910","promo")
        assert account.pesel == "12345678910" #sprawdzanie czy str, tylko cyfry i dlugosc 11

        account = Account("John", "Doe", "123456789101","promo")
        assert account.pesel == "INVALID" # sprawdzanie warunku blednego wpisania

    def test_promo_code(self):
        account = Account("John", "Doe", "12345678910","")
        assert account.promo_code is None # promo_code pusty

        account = Account("John", "Doe", "12345678910", "PROM_1234")
        assert account.promo_code is None # promo_code niepoprawny

        account = Account("John", "Doe", "", "PROM_360")
        assert account.promo_code is None # promo_code nie zaakceptowany przez brak wiek peselu

        account = Account("John", "Doe", "59061212345", "PROM_360")
        assert account.promo_code is None # promo_code dla osoby urodzonej poniej niz rok 1960
