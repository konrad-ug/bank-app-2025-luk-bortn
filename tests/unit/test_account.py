from src.account import Account
import pytest
class TestAccount:

    @pytest.fixture
    def account(self):
        return Account("John", "Doe", "00000000000", "_360")

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
        assert account.promo_code == "PROM_360" and account.balance == 50 # promo_code dla osoby urodzonej poniej niz rok 1960

        account = Account("John", "Doe", "59061212345", "PROM_360")

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

    def test_get_birthday_date(self):

        user = Account("A", "b", "", "promoCode")
        assert user.get_birthday_date() is None

        user = Account("A","b","90050100000","promoCode")
        assert user.get_birthday_date() == "01-05-1990"

        user = Account("A", "b", "04251300000", "promoCode")
        assert user.get_birthday_date() == "13-05-2004"

        user = Account("A", "b", "88812400000", "PROM360")
        assert (user.get_birthday_date() == "24-01-1888" and user.balance == 0)


        user = Account("A", "b", "21450400000", "promoCode")
        assert user.get_birthday_date() == "04-05-2121"

        user = Account("A", "b", "88812400000", "promoCode")
        assert user.get_birthday_date() == "24-01-1888"

        user = Account("A", "b", "23610600000", "promoCode")
        assert user.get_birthday_date() == "06-01-2223"

        user = Account("A", "b", "88812400000", "promoCode")
        assert user.get_birthday_date() == "24-01-1888"

    def test_apply_promo_code_old_user(self):
        user = Account("a","B","40031512345","PROM_ABC")  # data: 15-03-1940
        assert user.promo_code == "PROM_ABC"
        assert user.balance == 50  # +50 zł

    def test_apply_promo_code_young_user(self):
        user = Account("A","B","04251312345", "PROM_ABC")  # data: 13-05-2004
        assert user.promo_code is None
        assert user.balance == 0  # bez zmian

    def test_apply_promo_code_triggers_promo_and_bonus(self):
        user = Account("","","40031512345","PROM_ABC")  # rok 1940
        # Linia 20
        assert user.promo_code == "PROM_ABC"
        # Linia 21
        assert user.balance == 50