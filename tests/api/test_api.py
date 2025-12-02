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
        assert response.json() == []

    def test_get_all_accounts(self):
        # 1. Dodaj konto A
        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)

        # 2. Dodaj konto B
        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"

        requests.post(self.url, json=obj2)
        objects = [obj1, obj2]

        # 3. Pobierz wszystkie konta
        response = requests.get(self.url)
        assert response.status_code == 200

        # 4. Sprawdź, że GET zwraca listę *dwóch* kont
        assert len(response.json()) == 2
        for i in range(0, len(objects)):

            assert response.json()[i]["name"] == objects[i]["name"]
            assert response.json()[i]["surname"] == objects[i]["surname"]
            assert response.json()[i]["pesel"] == objects[i]["pesel"]

        # 5. Posprzątaj
        requests.delete(self.url + "/" + obj1["pesel"])
        requests.delete(self.url + "/" + obj2["pesel"])

    def test_get_account_count(self):
        # 1. Dodaj konto A
        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)

        # 2. Dodaj konto B
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
        # 1. Dodaj konto A
        obj1 = self.acc1.copy()
        obj1["pesel"] = "11111111111"
        requests.post(self.url, json=obj1)

        # 2. Dodaj konto B
        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"
        requests.post(self.url, json=obj2)

        response = requests.get(self.url)
        assert response.status_code == 200

        # Porównaj pola (pomijamy balance jeśli jest dodawany automatycznie)
        returned = response.json()[1]

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

        # 2. Dodaj konto B
        obj2 = self.acc1.copy()
        obj2["pesel"] = "22222222222"
        requests.post(self.url, json=obj2)

        # PESEL, którego NIE MA w rejestrze
        missing_pesel = "99999999999"

        # 3. Pobierz konto, które nie istnieje
        response = requests.get(self.url + "/" + missing_pesel)

        # 4. Sprawdź odpowiedź
        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

        # 5. Sprzątanie
        requests.delete(self.url + "/" + obj1["pesel"])
        requests.delete(self.url + "/" + obj2["pesel"])

    def test_update_account_passed(self):
        # 1. Dodaj konto
        obj = self.acc1.copy()
        obj["pesel"] = "44444444444"
        requests.post(self.url, json=obj)

        # 2. Przygotuj zmiany
        obj["name"] = "John"
        obj["surname"] = "Smith"
        # 3. Wykonaj PUT z danymi

        response = requests.patch(self.url + "/" + obj["pesel"], json=obj)

        print("STATUS:", response.status_code)
        print("BODY:", response.text)

        # 4. Sprawdź wynik
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"

        # (opcjonalnie) sprawdź, czy dane faktycznie się zmieniły
        get_response = requests.get(self.url + "/" + obj["pesel"])

        assert get_response.json()["newObj"]["name"] == "John"
        assert get_response.json()["newObj"]["surname"] == "Smith"


        requests.delete(self.url + "/" + obj["pesel"])

    def test_update_account_not_found(self):
        # Próbujemy zaktualizować konto, które nie istnieje
        pesel = "99999999999"
        changes = {"name": "Alice", "surname": "Wonder"}

        response = requests.patch(self.url + "/" + pesel, json=changes)

        assert response.status_code == 404
        assert response.json()["message"] == "Account not found"

    def test_update_account_empty_json(self):
        # Najpierw dodaj konto
        obj = self.acc1.copy()
        obj["pesel"] = "55555555555"
        requests.post(self.url, json=obj)

        # Wyślij PATCH z pustym JSON
        response = requests.patch(self.url + "/" + obj["pesel"], json={})

        # Powinno zwrócić 200, ale konto nie zmienione
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"

        # Sprawdź, że dane są nadal te same
        get_response = requests.get(self.url + "/" + obj["pesel"])
        assert get_response.json()["newObj"]["name"] == obj["name"]
        assert get_response.json()["newObj"]["surname"] == obj["surname"]

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