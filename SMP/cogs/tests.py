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



if __name__ == '__main__':
    unittest.main()