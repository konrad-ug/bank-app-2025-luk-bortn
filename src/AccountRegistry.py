from src.account import Account
class AccountRegistry:

    def __init__(self):
        self.accounts = []

    def add_account(self, account: Account) -> None:
        self.accounts.append(account)

    def get_account_by_pesel(self, pesel: str):
        result = [el for el in self.accounts if el.pesel == pesel]

        if len(result) == 0:
            return None
        else:
            return result[0]

    def get_all_accounts(self) -> list[Account]:
        return self.accounts

    def number_of_accounts(self) -> int:
        return len(self.accounts)