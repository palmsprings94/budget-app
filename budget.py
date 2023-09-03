class Category:

    def __init__(self, cat):
        self.category = cat
        self.ledger = list()
        self.amount = 0

    def __str__(self):
        numa = self.category.center(30, "*") + "\n"
        for i in self.ledger:
            numa = numa + i.get("description")[0:23].ljust(23, " ") + str('{:.2f}'.format(i["amount"]))[0:7].rjust(7, " ") + "\n"
        numa = numa + f"Total: {self.amount:4.2f}"
        return numa

    def deposit(self, amount, desc=None):
        if desc is None:
            desc = ""
        self.ledger.append({"amount": amount, "description": desc})
        self.amount = self.amount + amount

    def check_funds(self, amount):
        if self.amount < amount:
            return False
        else:
            return True

    def withdraw(self, amount, desc=None):
        if desc is None:
            desc = ""
        if self.check_funds(amount) is True:
            self.ledger.append({"amount": -amount, "description": desc})
            self.amount = self.amount - amount
            return True
        else:
            return False

    def transfer(self, amount, obj):
        if self.check_funds(amount) is True:
            self.ledger.append({"amount": -amount, "description": "Transfer to " f"{obj.category}"})
            obj.ledger.append({"amount": amount, "description": "Transfer from " f"{self.category}"})
            self.amount = self.amount - amount
            obj.amount = obj.amount + amount
            return True
        else:
            return False

    def get_balance(self):
        return self.amount

def create_spend_chart(categories):

    total_spent = 0
    longest = ""
    for cats in categories:
        if len(cats.category) >= len(longest):
            longest = cats.category
        for i in cats.ledger:
            if i["amount"] < 0:
                total_spent = total_spent + abs(i["amount"])

    percs = []
    for cats in categories:
        cats_spent = 0
        for i in cats.ledger:
            if i["amount"] < 0:
                cats_spent = cats_spent + abs(i["amount"])
        perc_spent = round((cats_spent / total_spent) * 100)
        percs.append(perc_spent)

    chart = "Percentage spent by category \n"
    future = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0]
    for i in future:
        chart = chart + f"{i}|".rjust(4)
        for num in percs:
            if i <= num:
                chart = chart + " o "
            else:
                chart = chart + "   "
        chart = chart + "\n"

    lines = "    " + "---" * len(categories) + "-\n"
    chart = chart + lines
    for i in range(len(longest)):
        chart += "     "
        for cats in categories:
            try:
                chart = chart + cats.category[i] + "  "
            except:
                chart = chart + "   "
        chart = chart + "\n"

    return chart
