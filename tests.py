from classes.Robots import BiscointRobot
import unittest
from unittest.mock import Mock

BiscointRobot = Mock()

def fake_get_offer(op, amount, is_quote):
    return {'offerId': 'EtRb8i2YTzDBWDHiQ', 'base': 'BTC', 'quote': 'BRL', 'op': 'buy', 'isQuote': True, 'baseAmount': '0.00014887', 'quoteAmount': '50.00', 'efPrice': '335863.51', 'createdAt': '2021-10-16T20:15:00.109Z', 'expiresAt': '2021-10-16T20:15:15.109Z', 'apiKeyId': 'moeGJ9tQ6TRGkJN8c'}

class TestRobot(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestRobot, self).__init__(*args, **kwargs)
        self.robot = BiscointRobot()
        self.robot.get_offer.side_effect = fake_get_offer
 

    def test_robot_get_offer(self):
        offer = self.robot.get_offer(op='buy', amount='50',is_quote=True)
        self.assertIsNotNone(offer)
        self.assertIn('offerId', offer)
        self.assertIn('base', offer)
        self.assertIn('quote', offer)
        self.assertIn('baseAmount', offer)
        self.assertIn('quoteAmount', offer)



if __name__ == '__main__':
    unittest.main()



