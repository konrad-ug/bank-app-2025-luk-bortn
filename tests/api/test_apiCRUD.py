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

    def test_create_account_denied_bad_pesel(self):
        """bad length of pesel or not only digits"""
        obj = self.acc1.copy()
        obj["pesel"] = "123"
        response = requests.post(self.url, json=obj)
        assert response.status_code == 400
        assert response.json()["message"] == "PESEL must be 11 digits"
        requests.delete(self.url + "/" + obj["pesel"])

    def test_create_account_missing_pesel(self):
        obj = {
            "name": "james",
            "surname": "Doe"
        }
        response = requests.post(self.url, json=obj)
        assert response.status_code == 400
        assert response.json()["message"] == "Missing field pesel"

    def test_create_account_missing_name(self):
        obj = {
            "surname": "Doe",
            "pesel": "22222222222"
        }
        response = requests.post(self.url, json=obj)
        assert response.status_code == 400
        assert response.json()["message"] == "Missing field name"

    def test_create_account_missing_surname(self):
        obj = {
            "name": "james",
            "pesel": "22222222222"
        }
        response = requests.post(self.url, json=obj)
        assert response.status_code == 400
        assert response.json()["message"] == "Missing field surname"

    def test_get_all_accounts_empty(self):
        response = requests.get(self.url)
        assert response.status_code == 200
        assert response.json()["data"] == []

    def test_get_all_accounts(self):
        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)

        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"

        requests.post(self.url, json=obj2)
        objects = [obj1, obj2]

        response = requests.get(self.url)
        assert response.status_code == 200

        assert len(response.json()["data"]) == 2
        for i in range(0, len(objects)):

            assert response.json()["data"][i]["name"] == objects[i]["name"]
            assert response.json()["data"][i]["surname"] == objects[i]["surname"]
            assert response.json()["data"][i]["pesel"] == objects[i]["pesel"]

        requests.delete(self.url + "/" + obj1["pesel"])
        requests.delete(self.url + "/" + obj2["pesel"])

    def test_get_account_count(self):

        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)

        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"

        requests.post(self.url, json=obj2)
        objects = [obj1, obj2]
        response = requests.get(self.url)
        assert response.status_code == 200
        assert len(response.json()) == len(objects)

        requests.delete(self.url + "/" + obj1["pesel"])
        requests.delete(self.url + "/" + obj2["pesel"])

    def test_get_account_by_pesel_found(self):
        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)


        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"
        requests.post(self.url, json=obj2)

        response = requests.get(self.url)
        assert response.status_code == 200

        returned = response.json()["data"][1]

        assert returned["name"] == obj2["name"]
        assert returned["surname"] == obj2["surname"]
        assert returned["pesel"] == obj2["pesel"]

        # Sprzątanie
        requests.delete(self.url + "/" + obj1["pesel"])
        requests.delete(self.url + "/" + obj2["pesel"])

    def test_get_account_by_pesel_not_found(self):
        # 1. Dodaj konto A
        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)

        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"
        requests.post(self.url, json=obj2)


        missing_pesel = "99999999999"

        response = requests.get(self.url + "/" + missing_pesel)


        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

        requests.delete(self.url + "/" + obj1["pesel"])
        requests.delete(self.url + "/" + obj2["pesel"])

    def test_update_account_passed(self):

        obj = self.acc1.copy()
        obj["pesel"] = "44444444444"
        requests.post(self.url, json=obj)

        obj["name"] = "John"
        obj["surname"] = "Smith"


        response = requests.patch(self.url + "/" + obj["pesel"], json=obj)

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        # 4. Sprawdź wynik
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"


        get_response = requests.get(self.url + "/" + obj["pesel"])

        assert get_response.json()["name"] == "John"
        assert get_response.json()["surname"] == "Smith"


        requests.delete(self.url + "/" + obj["pesel"])

    def test_update_account_not_found(self):

        pesel = "99999999999"
        changes = {"name": "Alice", "surname": "Wonder"}

        response = requests.patch(self.url + "/" + pesel, json=changes)

        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account_empty_json(self):

        obj = self.acc1.copy()
        obj["pesel"] = "55555555555"
        requests.post(self.url, json=obj)

        response = requests.patch(self.url + "/" + obj["pesel"], json={})


        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"

        get_response = requests.get(self.url + "/" + obj["pesel"])
        assert get_response.json()["name"] == obj["name"]
        assert get_response.json()["surname"] == obj["surname"]

        requests.delete(self.url + "/" + obj["pesel"])


    def test_delete_account_passed(self):
        obj1 = self.acc1.copy()
        obj1["pesel"] = "88888888888"
        requests.post(self.url, json=obj1)

        response = requests.delete(self.url + "/" + obj1["pesel"])

        assert response.status_code == 200
        assert  response.json()["message"] == "Account deleted"

    def test_delete_account_denied(self):
        obj1 = self.acc1.copy()
        obj1["pesel"] = "77777777777"
        requests.post(self.url, json=obj1)

        obj2 = self.acc1.copy()
        obj2["pesel"] = "77777777771"

        response = requests.delete(self.url + "/" + obj2["pesel"])

        assert response.status_code == 404
        assert  response.json()["message"] == "Account not found"

        requests.delete(self.url + "/" + obj1["pesel"])