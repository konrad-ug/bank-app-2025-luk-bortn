import requests



class TestApiTransfer:

    base_url = "http://127.0.0.1:5000/api/accounts"

    account = {
        "name": "James",
        "surname": "Doe",
        "pesel": "33333333333",
        "promo_code": "prm",
        "balance" : 0
    }

    transfer = {
        "amount": 500,
        "type": "incoming"
    }

    transfer_url = "http://127.0.0.1:5000/api/accounts/33333333333/transfer"
    def test_transfer_success(self):
        # 1. Tworzymy konto
        requests.post(self.base_url, json=self.account)

        # 2. Wykonujemy transfer
        response = requests.post(self.transfer_url, json=self.transfer)
        assert response.status_code == 200
        assert response.json()["message"] == "Transfer accepted"

        # 3. Usuwamy konto
        requests.delete(self.base_url)


    def test_transfer_account_not_found(self):
        transferUrl = "http://127.0.0.1:5000/api/accounts/11111111111/transfer"
        response = requests.post(transferUrl, json=self.transfer)
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"


    def test_transfer_invalid_JSON(self):
        requests.post(self.base_url, json=self.account)

        # 2. Wykonujemy transfer
        response = requests.post(self.transfer_url, json={"type": "incoming"})
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid JSON"

        response = requests.post(self.transfer_url, json={"amound": 5})
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid JSON"

        response = requests.post(self.transfer_url, json={"type": "incoming", "amound": 5})
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid JSON"

        # 3. Usuwamy konto
        requests.delete(self.base_url)

    def test_transfer_bad_amount(self):
        # 1. Tworzymy konto

        transfer_1 = {"type": "incoming", "amount": "string"}
        transfer_2 = {"type": "incoming", "amount": -5}

        requests.post(self.base_url, json=self.account)

        # 2. Wykonujemy transfer
        response = requests.post(self.transfer_url, json=transfer_1)
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid amount"

        response = requests.post(self.transfer_url, json=transfer_2)
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid amount"

        requests.delete(self.base_url)

    def test_transfer_bad_transfer_type(self):
        # 1. Tworzymy konto

        transfer = {"type": "1234", "amount": "string"}

        requests.post(self.base_url, json=self.account)

        # 2. Wykonujemy transfer
        response = requests.post(self.transfer_url, json=transfer)
        assert response.status_code == 400
        assert response.json()["message"] == "Invalid amount"

        requests.delete(self.base_url)

    def test_transfer_express_not_enough_money(self):
        # 1. Tworzymy konto

        transfer = {"type": "express", "amount": 500}

        requests.post(self.base_url, json=self.account)

        # 2. Wykonujemy transfer
        response = requests.post(self.transfer_url, json=transfer)
        assert response.status_code == 422
        assert response.json()["message"] == "Insufficient funds"

        requests.delete(self.base_url)


    def test_transfer_outgoing_not_enough_money(self):
        # 1. Tworzymy konto

        transfer = {"type": "outgoing", "amount": 500}

        requests.post(self.base_url, json=self.account)

        # 2. Wykonujemy transfer
        response = requests.post(self.transfer_url, json=transfer)
        assert response.status_code == 422
        assert response.json()["message"] == "Insufficient funds"

        requests.delete(self.base_url)

    def test_transfer_express_passed(self):
        requests.post(self.base_url, json=self.account)
        setup_transfer = {"type": "incoming", "amount": 1000}
        requests.post(self.transfer_url, json=setup_transfer)

        requests.get(f"{self.base_url}/{self.account['pesel']}")


        express_transfer = {"type": "express", "amount": 500}
        response = requests.post(self.transfer_url, json=express_transfer)

        assert response.status_code == 200