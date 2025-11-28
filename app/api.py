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
    """shows all account on site"""
    print("Get all accounts request received")
    accounts = registry.get_all_accounts()
    accounts_data = [
        {
            "name": acc.first_name,
            "surname": acc.last_name,
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
def get_account_by_pesel(pesel):
    """returns account with according pesel number"""

    result = registry.get_account_by_pesel(pesel)
    if result is None:
        return jsonify({"message": "Account not found"}), 404
    return jsonify(result), 200

@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    """updates account with according pesel number"""
    accounts = registry.get_all_accounts()
    new_obj = request.get_json()
    for account in accounts:
        if account.pesel == pesel:
            if "name" in new_obj:
                account.name = new_obj["name"]
            if "surname" in new_obj:
                account.surname = new_obj["surname"]
            return jsonify({"message": "Account updated"}), 200

    return jsonify({"message": "Account not found"}), 404


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    """deletes account"""
    initial_len = len(registry.get_all_accounts())
    accounts = [el for el in registry.get_all_accounts() if el.pesel != pesel]
    registry.accounts = accounts
    if len(accounts) == initial_len:
        return jsonify({"message": "Account not found"}), 404
    return jsonify({"message": "Account deleted"}), 200