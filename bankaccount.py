"""
I'd like you to make a class that represents a bank account.

Your bank account should accept an optional balance argument (defaulting to 0), have a balance attribute, and have deposit, withdraw, and transfer methods:

>>> a1 = BankAccount()
>>> a1.balance
0
>>> a1.deposit(10)
>>> a1.balance
10
>>> a2 = BankAccount(balance=20)
>>> a2.withdraw(15)
>>> a2.balance
5
>>> a1.transfer(a2, 3)
>>> a1
BankAccount(balance=7)
>>> a2
BankAccount(balance=8)

Your bank account should also have a nice string representation (as shown above).
"""

class BankAccount:
    
    # balance=0 is the way we set a default argument,
    # ie we make passing balance in optional
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("Cannot initialise with negative balance")
        self.balance = balance

    def __repr__(self):
        return f"BankAccount(balance={self.balance})"

    def deposit(self, amount):
        if amount < 0:
            raise ValueError("Cannot deposit negative amounts")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Cannot withdraw. Too poor!")
        self.balance -= amount

    def transfer(self, destination_account, amount):
        # TODO: this check happens inside .deposit(),
        # can we reuse the validation somehow?
        if amount < 0:
            raise ValueError("cannot transfer negative amounts")

        self.withdraw(amount)
        destination_account.deposit(amount)
