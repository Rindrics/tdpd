import unittest
from datetime import datetime
from ..stock import Stock
from ..rule import PriceRule, AndRule

class AndRuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        goog = Stock("GOOG")
        goog.update(datetime(2014, 2, 10), 8)
        goog.update(datetime(2014, 2, 11), 10)
        goog.update(datetime(2014, 2, 12), 12)
        msft = Stock("MSFT")
        msft.update(datetime(2014, 2, 10), 10)
        msft.update(datetime(2014, 2, 11), 10)
        msft.update(datetime(2014, 2, 12), 12)
        redhat = Stock("RHT")
        redhat.update(datetime(2014, 2, 10), 7)
        cls.exchange = {"GOOG": goog, "MSFT": msft, "RHT": redhat}

    def test_an_AndRule_matches_if_all_component_rules_are_true(self):
        rule = AndRule(PriceRule("GOOG", lambda stock: stock.price > 8), PriceRule("MSFT", lambda stock: stock.price > 10))
        self.assertTrue(rule.matches(self.exchange))
