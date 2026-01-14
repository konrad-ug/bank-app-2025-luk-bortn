from behave import *
import requests

URL = "http://localhost:5000"
@step('I create an account using name: "{name}", last name: "{surname}", pesel: "{pesel}"')
def create_account(context, name, surname, pesel):
    json_body = {
    "name": f"{name}",
    "surname": f"{surname}",
    "pesel": pesel,
    "promo_code" : "XYZ_code"
    }
    create_resp = requests.post(URL + "/api/accounts", json = json_body)
    assert create_resp.status_code == 201


@step('Account registry is empty')
def clear_account_registry(context):
    response = requests.get(URL + "/api/accounts")
    accounts = response.json()
    for account in accounts:
        pesel = account["pesel"]
        requests.delete(URL + f"/api/accounts/{pesel}")


@step('Number of accounts in registry equals: "{count}"')
def is_account_count_equal_to(context, count):
    response = requests.get(URL + "/api/accounts/count")
    assert response.status_code == 200
    assert response.json()["count"] == int(count)

@step('Account with pesel "{pesel}" exists in registry')
def check_account_with_pesel_exists(context, pesel):
    response = requests.get(f"http://localhost:5000/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()["pesel"] == pesel

@step('Account with pesel "{pesel}" does not exist in registry')
def check_account_with_pesel_does_not_exist(context, pesel):
    response = requests.get(URL + "/api/accounts")
    assert response.status_code == 200
    accounts = response.json()

    pesels = [acc["pesel"] for acc in accounts]
    assert pesel not in pesels


@step('I delete account with pesel: "{pesel}"')
def delete_account(context, pesel):
    response = requests.delete(URL + f"/api/accounts/{pesel}")
    assert response.status_code in (200,204)
    assert response.json()["message"] == "Account deleted"

@step('I update "{field}" of account with pesel: "{pesel}" to "{value}"')
def update_field(context, field, pesel, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    newObj = response.json()
    newObj[field] = value
    patch = requests.patch(URL + f"/api/accounts/{pesel}", json=newObj)
    assert patch.status_code == 200
    assert patch.json()["message"] == "Account updated"


@step('Account with pesel "{pesel}" has "{field}" equal to "{value}"')
def field_equals_to(context, pesel, field, value):
    response = requests.get(URL + f"/api/accounts/{pesel}")
    assert response.status_code == 200
    assert response.json()[field] == value
