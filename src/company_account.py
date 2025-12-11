import os
import datetime
import requests

class CompanyAccount: # pragma: no cover
    def __init__(self, name, nip):
        self.name = name
        self.balance = 0.0
        self.loan = 0.0
        self.operations = []

        if len(nip) == 10:

            if self.check_status_Vat(nip):
                self.nip = nip
                print(f"Konto firmowe dla {self.name} zostało utworzone.")
            else:
                raise ValueError("Company not registered!!")
        else:
            self.nip = "INVALID"

    def check_status_Vat(self, nip):

        base_url = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl/")

        if not base_url.endswith("/"):
            base_url += "/"

        today = datetime.date.today()
        url = f'{base_url}api/search/nip/{nip}?date={today}'

        try:
            response = requests.get(url)
            data = response.json()

            print(f"--> [LOG API MF] Odpowiedź dla NIP {nip}: {data}")

            if "result" not in data or data["result"] is None:
                return False

            subject = data["result"]["subject"]
            if subject is None:
                return False

            return subject["statusVat"] == "Czynny"

        except requests.exceptions.RequestException as error:
            print(f"--> [BŁĄD API] Nie udało się połączyć z MF: {error}")
            return False

    def outcoming_transfer(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount

    def incoming_transfer(self, amount):
        if amount > 0:
            self.balance += amount

    def express_outcoming_transfer(self, amount):
        fee = 5
        if amount > 0 and self.balance >= amount + fee:
            self.balance -= (amount + fee)

    def take_loan(self, amount: float) -> bool:
        if self.balance >= amount * 2 and -1775.0 in self.operations:
            self.loan += amount
            self.balance += amount
            return True
        else:
            return False