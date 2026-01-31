"""all necessary imports"""
from flask import Flask, request, jsonify
from src.AccountRegistry import AccountRegistry
from src.account import Account
from src.MongoAccountsRepository import MongoAccountsRepository
app = Flask(__name__)
registry = AccountRegistry()
mongo_repo = MongoAccountsRepository()
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
    result = {"status": "success", "data": accounts_data}
    return jsonify(result), 200


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
                "name": acc.name,
                "surname": acc.surname,
                "pesel": acc.pesel,
                "balance": acc.balance
            }), 200

    return jsonify({"message": "Account not found"}), 404


@app.route("/api/accounts/<pesel>", methods=['PATCH'])
def update_account(pesel):
    props = request.get_json()
    if props is None:
        return jsonify({"message": "Invalid JSON"}), 400


    accounts = registry.get_all_accounts()


    for account in accounts:
        if account.pesel == pesel:

            if "name" in props:
                account.name = props["name"]
            if "surname" in props:
                account.surname = props["surname"]
            if "promo_code" in props:
                account.promo_code = props["promo_code"]

            return jsonify({"message": "Account updated"}), 200


    return jsonify({"message": "Account not found"}), 404


@app.route("/api/accounts/<pesel>", methods=['DELETE'])
def delete_account(pesel):
    """Deletes an account by pesel."""
    accounts = registry.get_all_accounts()   # pobieramy TYLKO raz
    accounts_before = len(accounts)


    new_accounts = [acc for acc in accounts if acc.pesel != pesel]
    accounts_after = len(new_accounts)

    if accounts_after == accounts_before:
        return jsonify({"message": "Account not found"}), 404

    registry.accounts = new_accounts

    return jsonify({"message": "Account deleted"}), 200



@app.route("/api/accounts/<pesel>/transfer", methods=["POST"])
def transfer(pesel):
    body = request.get_json()


    account = registry.get_account_by_pesel(pesel)
    if account is None:
        return jsonify({"message": "Account not found"}), 404


    required_keys = {"type", "amount"}
    body_keys = set(body.keys())
    if body_keys != required_keys:
        return jsonify({"message": "Invalid JSON"}), 400

    amount = body["amount"]
    transfer_type = body["type"]


    if not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"message": "Invalid amount"}), 400

    allowed_types = ("incoming", "outgoing", "express")
    if transfer_type not in allowed_types:
        return jsonify({"message": "Unknown transfer type"}), 400

    if transfer_type == "incoming":
        account.incoming_transfer(amount)

    elif transfer_type == "outgoing":
        success = account.outcoming_transfer(amount)
        if not success:
            return jsonify({"message": "Insufficient funds"}), 422

    elif transfer_type == "express":
        success = account.express_outcoming_transfer(amount)
        if not success:
            return jsonify({"message": "Insufficient funds"}), 422

    return jsonify({"message": "Transfer accepted"}), 200

@app.route('/api/accounts/save', methods=['POST'])
def save_accounts():
    """
    Zapisuje obecny stan kont z rejestru do bazy danych MongoDB.
    """
    try:

        current_accounts = registry.accounts

        mongo_repo.save_all(current_accounts)

        return jsonify({"status": "success", "message": "Rejestr kont został zapisany do bazy danych."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/accounts/load', methods=['POST'])
def load_accounts():
    """
    Ładuje konta z bazy danych MongoDB do rejestru (nadpisując obecne).
    """
    mongo_repo.load_all(registry)  # zwraca listę dictów

    # konwersja dict → Account
    registry.accounts = [
        Account(
            name=acc.get("name", ""),
            surname=acc.get("surname", ""),
            pesel=acc.get("pesel", ""),
            promo_code=acc.get("promo_code")
        )
        for acc in registry.accounts
    ]

    return jsonify({
        "status": "success",
        "message": "Załadowano konta z bazy danych."
    }), 200