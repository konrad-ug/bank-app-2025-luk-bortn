import os
from pymongo import MongoClient
from src.AccountRegistry import AccountRegistry
from src.account import Account

class MongoAccountsRepository:
    def __init__(self, mongo_uri=None, db_name=None, collection_name=None, collection=None):
        if collection is not None:
            self._collection = collection
            return
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        db_name = os.getenv("MONGO_DB", "bank_app")
        collection_name = os.getenv("MONGO_COLLECTION", "accounts")

        client = MongoClient(mongo_uri)
        db = client[db_name]
        self._collection = db[collection_name]

    def save_all(self, accounts):
        self._collection.delete_many({})
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True
            )

    def load_all(self, registry: AccountRegistry):
        registry.accounts = []
        for acc in self._collection.find({}, {"_id": 0}):
            account = Account(
                name=acc["name"],
                surname=acc["surname"],
                pesel=acc["pesel"],
                promo_code=acc.get("promo_code")
            )

            registry.add_account(account)

    def delete_all(self):
        self._collection.delete_many({})

    def get_raw_list(self):
        return list(self._collection.find({}, {"_id": 0}))