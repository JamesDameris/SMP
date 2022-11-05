import unittest
from steammarket import *


class TestCogs(unittest.TestCase):

    def test_wear_parser(self):
        self.assertEqual("", wearParser(""));
        self.assertEqual("RandomType", wearParser("RandomType"))
        self.assertEqual("(Minimal Wear)", wearParser("minimal wear"))
        self.assertEqual("(Minimal Wear)", wearParser("minimal-wear"))
        self.assertEqual("(Minimal Wear)", wearParser("Minimal Wear"))
        self.assertEqual("(Minimal Wear)", wearParser("Minimal-Wear"))
        self.assertEqual("(Factory New)", wearParser("factory new"))
        self.assertEqual("(Factory New)", wearParser("factory-new"))
        self.assertEqual("(Factory New)", wearParser("Factory New"))
        self.assertEqual("(Factory New)", wearParser("Factory-New"))
        self.assertEqual("(Battle-Scarred)", wearParser("battle scarred"))
        self.assertEqual("(Battle-Scarred)", wearParser("battle-scarred"))
        self.assertEqual("(Battle-Scarred)", wearParser("Battle Scarred"))
        self.assertEqual("(Battle-Scarred)", wearParser("Battle-Scarred"))
        self.assertEqual("(Well-Worn)", wearParser("well worn"))
        self.assertEqual("(Well-Worn)", wearParser("well-worn"))
        self.assertEqual("(Well-Worn)", wearParser("well Worn"))
        self.assertEqual("(Well-Worn)", wearParser("Well-Worn"))
        self.assertEqual("(Field-Tested)", wearParser("field tested"))
        self.assertEqual("(Field-Tested)", wearParser("field-tested"))
        self.assertEqual("(Field-Tested)", wearParser("Field Tested"))
        self.assertEqual("(Field-Tested)", wearParser("Field-Tested"))

    def test_search_match(self):
        self.assertEqual("P90 | Asiimov (Factory New)", search_match(name="new p90 asiimov", appid=730))
        self.assertEqual("Sticker | LGB eSports | Katowice 2015", search_match(name="lgb esports katowice 2015 sticker", appid=730))
        self.assertEqual("Antwerp 2022 Legends Sticker Capsule", search_match(name="antwerp 2022 sticker capsule legends", appid=730))
        self.assertEqual("AK-47 | Ice Coaled (Field-Tested)", search_match(name="ak-47 ice coaled field tested", appid=730))
        self.assertEqual("Recoil Case", search_match(name="recoil case", appid=730))



if __name__ == '__main__':
    unittest.main()