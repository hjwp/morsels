import unittest

from bankaccount import BankAccount


class BankAccountTests(unittest.TestCase):

    """Tests for BankAccount."""

    def test_new_account_balance_default(self):
        account = BankAccount()
        self.assertEqual(account.balance, 0)

    def test_opening_balance(self):
        account = BankAccount(balance=100)
        self.assertEqual(account.balance, 100)

    def test_deposit(self):
        account = BankAccount()
        account.deposit(100)
        self.assertEqual(account.balance, 100)

    def test_withdraw(self):
        account = BankAccount(balance=100)
        account.withdraw(40)
        self.assertEqual(account.balance, 60)

    def test_repr(self):
        account = BankAccount()
        self.assertIn("BankAccount(", repr(account))
        self.assertIn("balance=0", repr(account))
        self.assertNotIn("balance=200", repr(account))
        account.deposit(200)
        self.assertIn("balance=200)", repr(account))
        self.assertNotIn("balance=0", repr(account))

    def test_transfer(self):
        mary_account = BankAccount(balance=100)
        dana_account = BankAccount(balance=0)

        mary_account.transfer(dana_account, 20)

        self.assertEqual(mary_account.balance, 80)
        self.assertEqual(dana_account.balance, 20)

    # To test bonus 1, comment out the next line
    def test_deposit_and_withdraw_validation(self):
        mary_account = BankAccount(balance=100)
        # Can't start with negative balance
        with self.assertRaises(ValueError):
            dana_account = BankAccount(balance=-10)

        dana_account = BankAccount(balance=0)
        self.assertEqual(dana_account.balance, 0)
        self.assertEqual(mary_account.balance, 100)

        # Can't deposit negative amount
        with self.assertRaises(ValueError):
            mary_account.deposit(-10)
        self.assertEqual(mary_account.balance, 100)

        # Can't withdraw more than we have (no overdrafting)
        with self.assertRaises(ValueError):
            mary_account.withdraw(101)
        self.assertEqual(mary_account.balance, 100)

        # Can't transfer more than we have
        with self.assertRaises(ValueError):
            mary_account.transfer(dana_account, 101)
        self.assertEqual(mary_account.balance, 100)
        self.assertEqual(dana_account.balance, 0)

        # Can't transfer negative amount
        with self.assertRaises(ValueError):
            mary_account.transfer(dana_account, -5)

        # We can transfer everything
        mary_account.transfer(dana_account, 100)
        self.assertEqual(mary_account.balance, 0)
        self.assertEqual(dana_account.balance, 100)

        # We can transfer partial amounts
        dana_account.transfer(mary_account, 10)
        self.assertEqual(mary_account.balance, 10)
        self.assertEqual(dana_account.balance, 90)

        # We can't transfer a negative amount, even when both accounts have money
        with self.assertRaises(ValueError):
            mary_account.transfer(dana_account, -5)
        self.assertEqual(mary_account.balance, 10)
        self.assertEqual(dana_account.balance, 90)

    # To test bonus 2, comment out the next line
    @unittest.expectedFailure
    def test_account_number_and_accounts_registry(self):
        # Re-import the BankAccount class
        import importlib
        import bank_account

        importlib.reload(bank_account)
        from bank_account import BankAccount

        self.assertEqual(BankAccount.accounts, [])

        # First account added to registry
        account1 = BankAccount()
        self.assertEqual(BankAccount.accounts, [account1])

        # Second account added to registry
        account2 = BankAccount(100)
        self.assertEqual(BankAccount.accounts, [account1, account2])

        # The account numbers are unique
        self.assertNotEqual(account1.number, account2.number)

        account3 = BankAccount(300)
        self.assertEqual(BankAccount.accounts[2].balance, account3.balance)
        account3.transfer(account2, 50)
        self.assertEqual(BankAccount.accounts[2].balance, account3.balance)
        self.assertEqual(BankAccount.accounts[1].balance, account2.balance)

        # New account number is also unique
        self.assertNotEqual(account1.number, account3.number)
        self.assertNotEqual(account2.number, account3.number)

    # To test bonus 3, comment out the next line
    @unittest.expectedFailure
    def test_balance_cannot_be_written(self):
        account1 = BankAccount()
        account2 = BankAccount(100)
        self.assertEqual(account1.balance, 0)
        with self.assertRaises(Exception):
            account1.balance = 50
        self.assertEqual(account1.balance, 0)
        self.assertEqual(account2.balance, 100)
        with self.assertRaises(Exception):
            account2.balance = 50
        self.assertEqual(account2.balance, 100)
        account1.deposit(100)
        account2.deposit(10)
        self.assertEqual(account1.balance, 100)
        self.assertEqual(account2.balance, 110)
        with self.assertRaises(Exception):
            account2.balance = 500
        self.assertEqual(account2.balance, 110)
        account2.transfer(account1, 50)
        self.assertEqual(account1.balance, 150)
        self.assertEqual(account2.balance, 60)


class AllowUnexpectedSuccessRunner(unittest.TextTestRunner):
    """Custom test runner to avoid FAILED message on unexpected successes."""

    class resultclass(unittest.TextTestResult):
        def wasSuccessful(self):
            return not (self.failures or self.errors)


if __name__ == "__main__":
    from platform import python_version
    import sys

    if sys.version_info < (3, 6):
        sys.exit("Running {}.  Python 3.6 required.".format(python_version()))
    unittest.main(verbosity=2, testRunner=AllowUnexpectedSuccessRunner)
