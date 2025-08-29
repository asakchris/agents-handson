import unittest  
from accounts import Account, get_share_price  

class TestAccount(unittest.TestCase):  
    def setUp(self):  
        self.account = Account('1234', 1000.0)  

    def test_initial_balance(self):  
        self.assertEqual(self.account.balance, 1000.0)  

    def test_deposit_positive(self):  
        self.account.deposit(500.0)  
        self.assertEqual(self.account.balance, 1500.0)  

    def test_deposit_negative(self):  
        with self.assertRaises(ValueError):  
            self.account.deposit(-100.0)  

    def test_withdraw_positive(self):  
        self.account.withdraw(300.0)  
        self.assertEqual(self.account.balance, 700.0)  

    def test_withdraw_exceeds_balance(self):  
        with self.assertRaises(ValueError):  
            self.account.withdraw(2000.0)  

    def test_buy_shares_success(self):  
        self.account.buy_shares('AAPL', 2)  
        self.assertEqual(self.account.holdings['AAPL'], 2)  
        self.assertEqual(self.account.balance, 700.0)  

    def test_buy_shares_insufficient_funds(self):  
        with self.assertRaises(ValueError):  
            self.account.buy_shares('TSLA', 2)  

    def test_sell_shares_success(self):  
        self.account.buy_shares('AAPL', 2)  
        self.account.sell_shares('AAPL', 1)  
        self.assertEqual(self.account.holdings['AAPL'], 1)  
        self.assertEqual(self.account.balance, 850.0)  

    def test_sell_shares_insufficient_holdings(self):  
        with self.assertRaises(ValueError):  
            self.account.sell_shares('AAPL', 3)  

    def test_get_portfolio_value(self):  
        self.account.buy_shares('AAPL', 2)  
        self.assertEqual(self.account.get_portfolio_value(), 700.0 + 2 * get_share_price('AAPL'))  

    def test_profit_loss(self):  
        self.account.buy_shares('AAPL', 2)  
        self.assertEqual(self.account.get_profit_loss(), self.account.get_portfolio_value() - self.account.initial_deposit)  

    def test_get_holdings(self):  
        self.account.buy_shares('AAPL', 2)  
        self.assertEqual(self.account.get_holdings(), {'AAPL': 2})  

    def test_get_transactions(self):  
        self.account.deposit(500.0)  
        self.assertEqual(self.account.get_transactions(), ['Deposited: 500.0'])  

if __name__ == '__main__':  
    unittest.main()