"""imports"""
import requests


class TestApiCrud:
    url = "http://127.0.0.1:5000/api/accounts"
    acc1 = {
        "name": "james",
        "surname": "Doe",
        "pesel": "111111111",
        "promo_code": "prm"
    }

    def test_create_account_passed(self):
        obj = self.acc1.copy()
        obj["pesel"] = "22222222222"
        response = requests.post(self.url, json=obj)

        assert response.status_code == 201
        assert response.json()["message"] == "Account created"
        requests.delete(self.url + "/" + obj["pesel"])






