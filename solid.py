# SOLID

from abc import ABC, abstractmethod

class Order:
    items = []
    quantities =[]
    prices = []
    status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total


class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass

# Uses composition over inheritance
class SMSAuth(Authorizer):
    authorized = False

    def verify_code(self, code):
        print(f"Verifying code: {code}")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class NotARobot(Authorizer):
    authorized = False

    def not_a_robot(self):
        print("Not a robot")
        self.authorized = True

    def is_authorized(self) -> bool:
        return self.authorized

class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, order):
        pass

class CreditPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code):
        self.security_code = security_code

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "PAID"

class DebitPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code, auth: Authorizer):
        self.auth = auth
        self.security_code = security_code

    def pay(self, order):
        if not self.auth.is_authorized():
            raise Exception("Not Authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "PAID"

class BitcoinPaymentProcessor(PaymentProcessor):

    def __init__(self, wallet_id):
        self.wallet_id = wallet_id

    def pay(self, order):
        print("Processing bitcoin payment type")
        print(f"Verifying security code: {self.wallet_id}")
        order.status = "PAID"

order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB Cable", 2, 5)

print(order.total_price())
authorizer = NotARobot()
processor = DebitPaymentProcessor("9876", authorizer)
authorizer.not_a_robot()
processor.pay(order)