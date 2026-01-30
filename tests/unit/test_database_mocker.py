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
        acc1 = Account("Jan", "Kowalski", "12345678901", "")
        acc1.balance = 100
        acc2 = Account("Anna", "Nowak", "98765432109", "")
        acc2.balance = 200

        accounts = [acc1, acc2]
        repo.save_all(accounts)


        mock_collection.delete_many.assert_called_once_with({})

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
        mock_collection.update_one.assert_has_calls(expected_calls, any_order=True)

    def test_load_all_accounts(self, repo, mock_collection, mocker):

        fake_db_data = [
            {"pesel": "111", "name": "Test1", "balance": 50},
            {"pesel": "222", "name": "Test2", "balance": 60}
        ]

        mock_collection.find.return_value = fake_db_data


        mock_registry = mocker.Mock(spec=AccountRegistry)
        mock_registry.accounts = ["stare_smieci"]


        repo.load_all(mock_registry)

        mock_collection.find.assert_called_once()
        assert mock_registry.accounts == []

        expected_calls = [
            mocker.call({"pesel": "111", "name": "Test1", "balance": 50}),
            mocker.call({"pesel": "222", "name": "Test2", "balance": 60})
        ]
        mock_registry.add_account.assert_has_calls(expected_calls)