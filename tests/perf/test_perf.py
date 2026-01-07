"""imports"""
import requests

import random

class TestPerformance:
    url = "http://127.0.0.1:5000/api/accounts"
    transfer_url = f"http://127.0.0.1:5000/api/accounts/11111111111/transfer"
    delete_url = f"http://127.0.0.1:5000/api/accounts/11111111111"

    account = {
        "name": "james",
        "surname": "Doe",
        "pesel": "11111111111",
        "promo_code": "prm"
    }

    def test_performance_create_100_accounts_by_try(self):
        for _ in range(100):
            pesel_number = str(random.randint(10000000000, 99999999999))
            new_obj = self.account.copy()
            new_obj["pesel"] = pesel_number
            try:
                add_response = requests.post(self.url, json=new_obj, timeout=0.5)

                print(add_response)
            except requests.exceptions.Timeout as error:
                print(f'The request timed out. Error {error}')

            finally:
                try:
                    delete_response = requests.delete(f"{self.url}/{pesel_number}" , timeout=0.5)
                    print(delete_response)
                except requests.exceptions.RequestException as delete_error:
                    print(f'error occurred while deleting account {delete_error}')

    def test_performance_create_100_accounts_by_assert(self):
        for _ in range(100):
            pesel_number = str(random.randint(10000000000, 99999999999))
            new_obj = self.account.copy()
            new_obj["pesel"] = pesel_number

            add_response = requests.post(self.url, json=new_obj, timeout=0.5)
            print(add_response)

            assert add_response.status_code == 201

            delete_response = requests.delete(f"{self.url}/{pesel_number}", timeout=0.5)
            print(delete_response)

            assert delete_response.status_code == 200


    def test_add_100_operations_to_account(self):
        new_obj = self.account.copy()
        response = requests.post(self.url, json=new_obj, timeout=0.5)

        assert response.status_code == 201
        assert response.json()["message"] == "Account created"

        transfer_info = {"type": "incoming", "amount": 1000}

        try:
            for _ in range(100):
                response = requests.post(self.transfer_url, json=transfer_info, timeout=10)
                assert response.status_code == 200

        finally:
            delete_response = requests.delete(self.delete_url, timeout=0.5)
            assert delete_response.status_code == 200
            assert delete_response.json()["message"] == "Account deleted"


