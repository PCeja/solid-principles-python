import unittest
from solid import (
    Order, SMSAuth, NotARobot,
    CreditPaymentProcessor, DebitPaymentProcessor, BitcoinPaymentProcessor
)


class TestOrder(unittest.TestCase):
    def setUp(self):
        """Create a fresh Order instance for each test"""
        self.order = Order()
        # Reset class variables to avoid interference between tests
        self.order.items = []
        self.order.quantities = []
        self.order.prices = []
    
    def test_add_item_single(self):
        """Test that add_item correctly adds a single item with quantity and price"""
        self.order.add_item("Keyboard", 1, 50)
        
        self.assertEqual(self.order.items, ["Keyboard"])
        self.assertEqual(self.order.quantities, [1])
        self.assertEqual(self.order.prices, [50])
    
    def test_add_item_multiple(self):
        """Test that add_item correctly adds multiple items with quantities and prices"""
        self.order.add_item("Keyboard", 1, 50)
        self.order.add_item("SSD", 1, 150)
        self.order.add_item("USB Cable", 2, 5)
        
        self.assertEqual(self.order.items, ["Keyboard", "SSD", "USB Cable"])
        self.assertEqual(self.order.quantities, [1, 1, 2])
        self.assertEqual(self.order.prices, [50, 150, 5])
    
    def test_total_price_empty(self):
        """Test that total_price returns 0 for an empty order"""
        total = self.order.total_price()
        self.assertEqual(total, 0)
    
    def test_total_price_single_item(self):
        """Test that total_price returns the correct total for a single item"""
        self.order.add_item("Keyboard", 1, 50)
        total = self.order.total_price()
        self.assertEqual(total, 50)
    
    def test_total_price_multiple_items(self):
        """Test that total_price returns the correct total for multiple items"""
        self.order.add_item("Keyboard", 1, 50)
        self.order.add_item("SSD", 1, 150)
        self.order.add_item("USB Cable", 2, 5)
        
        total = self.order.total_price()
        # Expected: (1 * 50) + (1 * 150) + (2 * 5) = 50 + 150 + 10 = 210
        self.assertEqual(total, 210)
    
    def test_total_price_with_different_quantities(self):
        """Test that total_price correctly multiplies quantity by price"""
        self.order.add_item("Mouse", 3, 25)
        self.order.add_item("Monitor", 2, 200)
        
        total = self.order.total_price()
        # Expected: (3 * 25) + (2 * 200) = 75 + 400 = 475
        self.assertEqual(total, 475)


class TestSMSAuth(unittest.TestCase):
    def setUp(self):
        """Create a fresh SMSAuth instance for each test"""
        self.sms_auth = SMSAuth()
        # Reset the authorized flag
        self.sms_auth.authorized = False
    
    def test_verify_code_sets_authorized_true(self):
        """Test that verify_code sets authorized to True"""
        self.assertFalse(self.sms_auth.authorized)
        self.sms_auth.verify_code("123456")
        self.assertTrue(self.sms_auth.authorized)
    
    def test_is_authorized_returns_false_initially(self):
        """Test that is_authorized returns False before verification"""
        result = self.sms_auth.is_authorized()
        self.assertFalse(result)
    
    def test_is_authorized_returns_true_after_verification(self):
        """Test that is_authorized returns True after verify_code is called"""
        self.sms_auth.verify_code("123456")
        result = self.sms_auth.is_authorized()
        self.assertTrue(result)
    
    def test_is_authorized_returns_correct_status(self):
        """Test that is_authorized returns the correct authorization status"""
        # Initially not authorized
        self.assertFalse(self.sms_auth.is_authorized())
        
        # After verification
        self.sms_auth.verify_code("999999")
        self.assertTrue(self.sms_auth.is_authorized())


class TestNotARobot(unittest.TestCase):
    def setUp(self):
        """Create a fresh NotARobot instance for each test"""
        self.not_a_robot = NotARobot()
        # Reset the authorized flag
        self.not_a_robot.authorized = False
    
    def test_not_a_robot_sets_authorized_true(self):
        """Test that not_a_robot sets authorized to True"""
        self.assertFalse(self.not_a_robot.authorized)
        self.not_a_robot.not_a_robot()
        self.assertTrue(self.not_a_robot.authorized)
    
    def test_is_authorized_returns_false_initially(self):
        """Test that is_authorized returns False before not_a_robot is called"""
        result = self.not_a_robot.is_authorized()
        self.assertFalse(result)
    
    def test_is_authorized_returns_true_after_not_a_robot(self):
        """Test that is_authorized returns True after not_a_robot is called"""
        self.not_a_robot.not_a_robot()
        result = self.not_a_robot.is_authorized()
        self.assertTrue(result)
    
    def test_is_authorized_returns_correct_status(self):
        """Test that is_authorized returns the correct authorization status"""
        # Initially not authorized
        self.assertFalse(self.not_a_robot.is_authorized())
        
        # After calling not_a_robot
        self.not_a_robot.not_a_robot()
        self.assertTrue(self.not_a_robot.is_authorized())


class TestCreditPaymentProcessor(unittest.TestCase):
    def setUp(self):
        """Create a fresh Order instance for each test"""
        self.order = Order()
        self.order.items = []
        self.order.quantities = []
        self.order.prices = []
        self.order.status = "open"
        self.order.add_item("Test Item", 1, 100)
    
    def test_pay_sets_order_status_to_paid(self):
        """Test that pay sets order status to PAID"""
        processor = CreditPaymentProcessor("1234")
        processor.pay(self.order)
        self.assertEqual(self.order.status, "PAID")
    
    def test_stores_security_code(self):
        """Test that security code is stored correctly"""
        processor = CreditPaymentProcessor("5678")
        self.assertEqual(processor.security_code, "5678")


class TestDebitPaymentProcessor(unittest.TestCase):
    def setUp(self):
        """Create a fresh Order instance for each test"""
        self.order = Order()
        self.order.items = []
        self.order.quantities = []
        self.order.prices = []
        self.order.status = "open"
        self.order.add_item("Test Item", 1, 100)
    
    def test_pay_with_authorized_sms_auth_succeeds(self):
        """Test that pay succeeds when user is authorized via SMS"""
        auth = SMSAuth()
        auth.verify_code("1234")
        processor = DebitPaymentProcessor("9876", auth)
        processor.pay(self.order)
        self.assertEqual(self.order.status, "PAID")
    
    def test_pay_without_authorization_raises_exception(self):
        """Test that pay raises exception when user is not authorized"""
        auth = SMSAuth()  # Not verified
        processor = DebitPaymentProcessor("9876", auth)
        with self.assertRaises(Exception) as context:
            processor.pay(self.order)
        self.assertEqual(str(context.exception), "Not Authorized")
    
    def test_works_with_not_a_robot_authorizer(self):
        """Test that DebitPaymentProcessor works with NotARobot (LSP compliance)"""
        auth = NotARobot()
        auth.not_a_robot()
        processor = DebitPaymentProcessor("9876", auth)
        processor.pay(self.order)
        self.assertEqual(self.order.status, "PAID")
    
    def test_not_a_robot_unauthorized_raises_exception(self):
        """Test that pay raises exception when NotARobot is not authorized"""
        auth = NotARobot()  # Not verified
        processor = DebitPaymentProcessor("9876", auth)
        with self.assertRaises(Exception) as context:
            processor.pay(self.order)
        self.assertEqual(str(context.exception), "Not Authorized")


class TestBitcoinPaymentProcessor(unittest.TestCase):
    def setUp(self):
        """Create a fresh Order instance for each test"""
        self.order = Order()
        self.order.items = []
        self.order.quantities = []
        self.order.prices = []
        self.order.status = "open"
        self.order.add_item("Test Item", 1, 100)
    
    def test_pay_sets_order_status_to_paid(self):
        """Test that pay sets order status to PAID"""
        processor = BitcoinPaymentProcessor("wallet123")
        processor.pay(self.order)
        self.assertEqual(self.order.status, "PAID")
    
    def test_stores_wallet_id(self):
        """Test that wallet_id is stored correctly"""
        processor = BitcoinPaymentProcessor("my_wallet_abc")
        self.assertEqual(processor.wallet_id, "my_wallet_abc")


if __name__ == "__main__":
    unittest.main()
