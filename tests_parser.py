import unittest
import parser


class MyTestCase(unittest.TestCase):
    def test_parser_SYE(self):
        self.assertAlmostEqual(parser.calc("((((((1234) - 1) + 2) - 2) + 1) + 0)", parser.ShuntingYardEvaluator), 1234)
        self.assertAlmostEqual(parser.calc("            5 + (            21)", parser.ShuntingYardEvaluator), 26)
        self.assertAlmostEqual(parser.calc("56 - 8*(5-2)", parser.ShuntingYardEvaluator), 32)
        self.assertAlmostEqual(parser.calc("44/(21)", parser.ShuntingYardEvaluator), 44/21)
        self.assertAlmostEqual(parser.calc("(9^2) - 1", parser.ShuntingYardEvaluator), 80)
        self.assertAlmostEqual(parser.calc("-2^(0.5)", parser.ShuntingYardEvaluator), (-2)**(0.5))

    def test_parser_PCE(self):
        self.assertAlmostEqual(parser.calc("123^100"), 123**100)
        self.assertAlmostEqual(parser.calc("0^0"), 1)
        self.assertAlmostEqual(int(parser.calc("1000^2 / 99999999")), 0)
        self.assertAlmostEqual(parser.calc("44/(21)"), 44/21)
        self.assertAlmostEqual(parser.calc("(9^2) - 1"), 80)
        self.assertAlmostEqual(parser.calc("-2^(0.5)"), -(2)**0.5)

    def test_dec_inc(self):
        self.assertAlmostEqual(parser.calc(parser.eval_dec_inc("dec(1)")), 0)
        self.assertAlmostEqual(parser.calc(parser.eval_dec_inc("dec(inc(dec(inc(43))))")), 43)
        self.assertAlmostEqual(parser.calc(parser.eval_dec_inc("dec(dec(dec(dec(2) + 7)))")), 5)
        self.assertAlmostEqual(parser.calc(parser.eval_dec_inc("dec(0.2)")), -0.8)
        self.assertAlmostEqual(parser.calc(parser.eval_dec_inc("dec(1) / dec(1)")), float("inf"))


if __name__ == '__main__':
    unittest.main()


