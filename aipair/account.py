# Account class with id, customer, balance and method for deposit, withdraw and getbalance

class Account:
    def __init__(self, id, customer, balance=0):
        self.id = id
        self.customer = customer
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        """
        Withdraws a specified amount from the account balance.

        Args:
            amount (float): The amount to withdraw. Must be positive and less than or equal to the current balance.

        Raises:
            ValueError: If the withdrawal amount is not positive or if there is insufficient balance.
        """
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount

    def get_balance(self):
        return self.balance
    
    
    