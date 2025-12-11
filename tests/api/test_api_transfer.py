"""imports"""
import requests

class TestApiTransfer:
    """Tests for api transfers"""
    url = "http://127.0.0.1:5000/api/accounts/"
    acc1 = {
        "name": "james",
        "surname": "Doe",
        "pesel": "111111111",
        "promo_code": "prm"
    }

    transfer_data = {
        "type": "",
        "amount" : ""
    }


    def test_transfer_passed(self):
        account = self.acc1.copy()
        account["pesel"] = "33333333333"
        requests.post(self.url, json=account)

        response = requests.get(self.url + "/" + account["pesel"] + "/transfer")

        assert response.status_code == 200
        assert response.json()["message"] == "Transfer accepted"


