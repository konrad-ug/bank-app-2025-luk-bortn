import pytest
from src.account import Account
from src.AccountRegistry import AccountRegistry
from src.MongoAccountsRepository import MongoAccountsRepository


class TestMongoRepositoryByMocker:

    @pytest.fixture
    def mock_collection(self, mocker):
        """Fixture tworząca mocka kolekcji MongoDB"""
        return mocker.Mock()

    @pytest.fixture
    def repo(self, mock_collection):
        """Fixture tworząca instancję repozytorium z wstrzykniętym mockiem"""
        return MongoAccountsRepository(collection=mock_collection)

    def test_save_all_accounts(self, repo, mock_collection, mocker):
        # 1. Przygotowanie danych (Given)
        # Tworzymy prawdziwe obiekty kont, żeby sprawdzić jak są mapowane
        acc1 = Account("Jan", "Kowalski", "12345678901", "")
        acc1.balance = 100
        acc2 = Account("Anna", "Nowak", "98765432109", "")
        acc2.balance = 200

        accounts = [acc1, acc2]

        # 2. Wykonanie akcji (When)
        repo.save_all(accounts)

        # 3. Asercje (Then)
        # [cite_start]Sprawdzamy, czy wyczyszczono kolekcję przed zapisem [cite: 7]
        mock_collection.delete_many.assert_called_once_with({})

        # [cite_start]Sprawdzamy, czy zapisano każde konto osobno [cite: 37-41]
        # Używamy mocker.call do sprawdzenia konkretnych argumentów wywołania
        assert mock_collection.update_one.call_count == 2

        expected_calls = [
            mocker.call(
                {"pesel": "12345678901"},
                {"$set": acc1.to_dict()},
                upsert=True
            ),
            mocker.call(
                {"pesel": "98765432109"},
                {"$set": acc2.to_dict()},
                upsert=True
            )
        ]
        # assert_has_calls sprawdza czy wywołania wystąpiły (kolejność any_order=True)
        mock_collection.update_one.assert_has_calls(expected_calls, any_order=True)

    def test_load_all_accounts(self, repo, mock_collection, mocker):
        # 1. Przygotowanie danych (Given)
        # Symulujemy dane zwracane przez bazę (lista słowników)
        fake_db_data = [
            {"pesel": "111", "name": "Test1", "balance": 50},
            {"pesel": "222", "name": "Test2", "balance": 60}
        ]
        # Ustawiamy mocka, aby metoda find() zwracała naszą listę
        mock_collection.find.return_value = fake_db_data

        # Mockujemy AccountRegistry, aby sprawdzić interakcję z nim
        mock_registry = mocker.Mock(spec=AccountRegistry)
        mock_registry.accounts = ["stare_smieci"]  # Symulacja zapełnionego rejestru

        # 2. Wykonanie akcji (When)
        repo.load_all(mock_registry)

        # 3. Asercje (Then)
        # Sprawdzamy czy repozytorium pobrało dane z bazy
        mock_collection.find.assert_called_once()

        # [cite_start]Sprawdzamy czy lista kont w rejestrze została wyczyszczona [cite: 8]
        # (W Twoim kodzie: registry.accounts = [])
        assert mock_registry.accounts == []

        # Sprawdzamy czy dodano konta do rejestru
        # UWAGA: Testujemy Twój obecny kod, który przekazuje słownik (acc) bezpośrednio
        expected_calls = [
            mocker.call({"pesel": "111", "name": "Test1", "balance": 50}),
            mocker.call({"pesel": "222", "name": "Test2", "balance": 60})
        ]
        mock_registry.add_account.assert_has_calls(expected_calls)