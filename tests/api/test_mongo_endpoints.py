import requests
from src.MongoAccountsRepository import MongoAccountsRepository
class TestMongoEndpoints:
    mongoDB: MongoAccountsRepository = MongoAccountsRepository()
    url: str = "http://localhost:5000/api/accounts"
    url_save: str = "http://localhost:5000/api/accounts/save"
    url_delete: str = "http://localhost:5000/api/accounts/11111111111"
    url_load: str = "http://localhost:5000/api/accounts/load"
    def test_save_accounts(self) -> None:
        self.mongoDB.delete_all()
        resp_add: requests.Response = requests.post(self.url, json={
            "name": "luki",
            "surname": "bortn",
            "pesel": "11111111111",
            "promo_code": "XYZ_123"
        })

        assert resp_add.status_code == 201

        resp_save: requests.Response = requests.post(self.url_save)
        assert resp_save.status_code == 200

        lista = self.mongoDB.get_raw_list()

        assert len(lista) == 1
        self.mongoDB.delete_all()

        requests.delete(self.url_delete)

    def test_load_accounts(self):
        """"""
        '''
        try:
            self.mongoDB.delete_all()
            resp_add: requests.Response = requests.post(self.url, json={
                "name": "luki",
                "surname": "bortn",
                "pesel": "11111111111",
                "promo_code": "XYZ_123"
            })

            assert resp_add.status_code == 201

            resp_save: requests.Response = requests.post(self.url_save)
            assert resp_save.status_code == 200

            lista = self.mongoDB.get_raw_list()

            assert len(lista) == 1

            resp: requests.Response = requests.post(self.url_load)
            assert resp.status_code == 200

            lista = self.mongoDB.get_raw_list()
            assert len(lista) == 1

            resp_api: requests.Response =  requests.get("http://localhost:5000/api/accounts")
            assert len(resp_api.json()) == 1

        finally:
            self.mongoDB.delete_all()
            requests.delete(self.url_delete)
            '''

