"""all necessary imports"""
from flask import Flask, request, jsonify
from src.AccountRegistry import AccountRegistry
from src.account import Account
app = Flask(__name__)
registry = AccountRegistry()
@app.route("/api/accounts", methods=['POST'])
def create_account():
    """adds account to registry"""
    data = request.get_json()
    required_fields = ["name", "surname", "pesel"]

    for field in required_fields:
        if field not in data:
            return jsonify({"message": "Missing field " + field}), 400

    if not data["pesel"].isdigit() or len(data["pesel"]) != 11:
        return jsonify({"message": "PESEL must be 11 digits"}), 400

    if registry.get_account_by_pesel(data["pesel"]):
        return jsonify({"message": "Account with this pesel already exists"}), 409

    print("Create account request: ",data)

    account = Account(
        data["name"],
        data["surname"],
        data["pesel"],
        data["promo_code"]
    )

    registry.add_account(account)
    return jsonify({"message": "Account created"}), 201





@app.route("/api/accounts", methods=['GET'])
def get_all_accounts():
    accounts = registry.get_all_accounts()
    accounts_data = [
        {
            "name": acc.name,
            "surname": acc.surname,
            "pesel": acc.pesel,
            "balance": acc.balance
        }
        for acc in accounts
    ]
    return jsonify(accounts_data), 200


@app.route("/api/accounts/count", methods=['GET'])
def get_account_count():
    """returns number of accounts"""
    print("Get account count request received")
    count = registry.number_of_accounts()
    return jsonify({"count": count}), 200


@app.route("/api/accounts/<pesel>", methods=['GET'])
def get_account(pesel):
    accounts = registry.get_all_accounts()

    for acc in accounts:
        if acc.pesel == pesel:
            return jsonify({
                "newObj": {
                    "name": acc.name,
                    "surname": acc.surname,
                    "pesel": acc.pesel,
                    "balance": acc.balance
                }
            }), 200

    return jsonify({"message": "Account not found"}), 404


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    # 1. Pobierz dane do zmiany
    props = request.get_json()
    if props is None:
        return jsonify({"message": "Invalid JSON"}), 400

    # 2. Pobierz wszystkie konta
    accounts = registry.get_all_accounts()

    # 3. Szukaj konta po peselu
    for account in accounts:
        if account.pesel == pesel:
            # 4. Aktualizuj pola, które są w props
            if "name" in props:
                account.name = props["name"]
            if "surname" in props:
                account.surname = props["surname"]
            if "promo_code" in props:
                account.promo_code = props["promo_code"]

            # 5. Zwróć sukces
            return jsonify({"message": "Account updated"}), 200

    # 6. Nie znaleziono konta
    return jsonify({"message": "Account not found"}), 404


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    """Deletes an account by pesel."""
    accounts_before = len(registry.get_all_accounts())

    registry.accounts = [acc for acc in registry.get_all_accounts() if acc.pesel != pesel]

    accounts_after = len(registry.get_all_accounts())

    if accounts_after == accounts_before:
        return jsonify({"message": "Account not found"}), 404

    return jsonify({"message": "Account deleted"}), 200
