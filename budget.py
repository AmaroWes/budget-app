class Category:
    
    def __init__(self, name):
        self.name = str(name)
        self.ledger = list()
        self.amount = 0

        if len(self.name) % 2 == 0:
            self.output_name = "*" * (15 - int((len(self.name) / 2))) + self.name + "*" * (15 - int((len(self.name) / 2)))
        else:
            self.output_name = "*" * (15 - int((len(self.name)))) + self.name + "*" * (14 - int((len(self.name)) / 2))

    def __str__(self):
        text = f"{self.output_name}\n"
        for i in range(len(self.ledger)):
            num = self.ledger[i]['amount']
            if isinstance(num, int):
                num = str(num) + ".00"
            if len(self.ledger[i]['description']) > 23:
                aux = self.ledger[i]['description']
                aux = aux[:23]
                text += f"{aux} {num}\n"
            elif len(self.ledger[i]['description']) == 0:
                aux = " "*(30 - len(str(num)))
                text += f"{aux}{num}\n"
            else:
                aux = " " * (30 - (len(self.ledger[i]['description']) + len(str(num))))
                text += f"{self.ledger[i]['description']}{aux}{num}\n"
        text += f"Total: {self.amount}"
        return text

    def deposit(self, amount, desc=""):
        self.ledger.append({"amount": amount, "description": desc})
        self.amount += amount

    def withdraw(self, amount, desc=""):
        aux = self.check_funds(amount)
        if aux:
            self.ledger.append({"amount": -amount, "description": desc})
            self.amount -= amount
        return aux

    def get_balance(self):
        return self.amount
    
    def transfer(self, amount, dest):
        aux = self.check_funds(amount)
        if aux:
            self.withdraw(amount, f"Transfer to {dest.name}")
            dest.deposit(amount, f"Transfer from {self.name}")
        return aux
    
    def check_funds(self, amount):
        if self.amount < amount:
            return False
        else:
            return True


def create_spend_chart(categories):
    total = list()
    names = list()
    text = [["Percentage spent by category"]]
    max_name_len = 0
    # capturing the name and values of the categories
    for c in range(len(categories)):
        aux = categories[c].ledger
        num = 0
        for i in range(len(aux)):
            if aux[i]['amount'] < 0:
                num += aux[i]['amount']

        if max_name_len < len(categories[c].name):
            max_name_len = len(categories[c].name)
        total.append(num)
        names.append(categories[c].name)

    # creating the lines of the text
    size = max_name_len + 13
    percent = 100
    for i in range(size):
        if i < 11:
            if percent == 100:
                aux_text = f"{percent}|"
            elif percent == 0:
                aux_text = f"  {percent}|"
            else:
                aux_text = f" {percent}|"
            for n in range(len(names)):
                aux_percent = -percent
                if total[n] > aux_percent:
                    aux_text += f"   "
                else:
                    aux_text += f" o "
            text.append([aux_text + " "])
            percent -= 10
        elif i == 11:
            text.append(["    ----------"])
        else:
            for n in range(max_name_len):
                aux_text = f"    "
                for j in range(len(names)):
                    try:
                        aux_text += f" {names[j][n]} "
                    except IndexError:
                        aux_text += f"   "
                text.append([aux_text + " "])

    # creating the return str
    output = ""
    for i in range(size):
        if i == size - 1:
            output += f"{text[i][0]}"
        else:
            output += f"{text[i][0]}\n"

    return output