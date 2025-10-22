class CompanyAccount:
    def __init__(self,name, nip):
        self.name = name
        self.balance = 0.0

        if type(nip) is str and len(nip) == 10:
            self.nip = nip
        else:
            self.nip = "INVALID"

    def outcoming_transfer(self, cash):
        if cash <= 0 or self.balance - cash <= 0:
            return
        else:
            self.balance -= cash

    def incoming_transfer(self, cash):
        if cash > 0:
            self.balance += cash
        else:
            return

    def express_outcoming_transfer(self, cash):
        if cash <= 0 or self.balance - cash < -5:
            return
        else:
            self.balance -= (cash + 5) # warunek z dlugiem