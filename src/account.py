import datetime
import re
from lib.smtp import SMTPClient

class Account:
    def __init__(self, name, surname, pesel, promo_code):
        self.name = name
        self.surname = surname
        self.balance = 0.0
        self.loan = 0.0
        self.operations = []

        if type(pesel) is str and pesel.isdigit() and len(pesel) == 11:
            self.pesel = pesel
        else:
            self.pesel = "INVALID"

        self.promo_code = None
        birthday_str = self.get_birthday_date()
        if birthday_str is not None:
            year = int(birthday_str[6:])
            if re.fullmatch(r"^PROM_\w{3}$", promo_code) and year < 1960:
                self.promo_code = promo_code
                self.balance += 50

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "pesel": self.pesel,
            "promo_code": self.promo_code,
            "balance": self.balance
        }

    def get_birthday_date(self):
        if self.pesel == "INVALID":
            return None
        digits = self.pesel[0:6]
        year = int(digits[0]) * 10 + int(digits[1])
        month = int(digits[2]) * 10 + int(digits[3])
        day = int(digits[4]) * 10 + int(digits[5])

        if month >= 1 and month <= 12:
            year += 1900
        elif month >= 21 and month <= 32:
            month -= 20
            year += 2000
        elif month >= 41 and month <= 52:
            month -= 40
            year += 2100
        elif month >= 61 and month <= 72:
            month -= 60
            year += 2200
        elif month >= 81 and month <= 92:
            month -= 80
            year += 1800

        return f"{day:02d}-{month:02d}-{year}"


    def outcoming_transfer(self, cash):
        if cash <= 0 or self.balance <= cash:
            return
        else:
            self.balance -= cash
            self.operations.append(-1 * cash)

    def incoming_transfer(self, cash):
        if cash > 0:
            self.balance += cash
            self.operations.append(cash)
        else:
            return

    def express_outcoming_transfer(self, cash):
        fee = 1
        if cash <= 0 or (self.balance - (cash + fee)) < 0:
            return False

        else:
            self.balance -= (cash + fee)
            self.operations.append(-1 * (cash + fee))

            return True

    def submit_for_loan(self, amount):
        """Sprawdza warunki przyznania kredytu."""

        if len(self.operations) >= 3:
            last_three = self.operations[-3:]
            if all(op > 0 for op in last_three):
                self.loan += amount
                self.balance += amount
                return True

        if len(self.operations) >= 5:
            last_five_sum = sum(self.operations[-5:])
            if last_five_sum > amount:
                self.loan += amount
                self.balance += amount
                return True
        return False

    def send_history_via_email(self, email):
        today = datetime.date.today()
        subject = f"Account Transfer History {today}"
        text = f"Personal account history: {self.operations}"

        return SMTPClient.send(subject, text, email)