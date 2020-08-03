import unittest
from brailfun import new_cell

testing_cell = new_cell(power=5, time_on=0.5, time_off=0)

class test_brailfun(unittest.TestCase):

    def test_01_clamp(self):
        testcase = [-5, 0, 140, 73.25, 255, 302]
        expected = [0, 0, 140, 73.25, 255, 255]
        for index, _ in enumerate(testcase):
            self.assertEqual(testing_cell.clamp(testcase[index]), expected[index])

    def test_02_clamp(self):
        testcase = ["a", ["a"], {"a"}, set("a"), ("a")]
        expected = []
        for index, _ in enumerate(testcase):
            with self.assertRaises(TypeError):
                testing_cell.clamp(testcase[index])

    def test_random_letter(self):
        testcase = "abcdefghijklmnñopqrstuvwxyz"
        self.assertIn(testing_cell.random_letter(), testcase)

    def test_translator(self):
        testcase = [" ","a", "j", "s", "w", "á", "ñ"]
        expected = [[0,0,0,0,0,0],[1,0,0,0,0,0], [0,1,0,1,1,0], [0,1,1,1,0,0], [0,1,0,1,1,1], [1,0,0,0,0,0], [1,1,0,1,1,1]]
        for index, _ in enumerate(testcase):
            self.assertEqual(testing_cell.translator(testcase[index]), expected[index])

    def test_01_pinout(self):
        testcase = testing_cell.pinout(signal_pin=4, d3=23, d5=12)
        expected = {"signal_pin":4, "d1": 4, "d2": 17, "d3": 23, "d4": 22, "d5": 12, "d6": 24}
        self.assertEqual(testcase, expected)
        testing_cell.pinout(signal_pin=18, d1=4, d2=17, d3=27, d4=22, d5=23, d6=24)

    def test_02_pinout(self):
        testcase = testing_cell.pinout(d1="hola", d2={23}, d5=[3])
        expected = {"signal_pin":18, "d1": 4, "d2": 17, "d3": 27, "d4": 22, "d5": 23, "d6": 24}
        self.assertEqual(testcase, expected)

if __name__ == "__main__":
    unittest.main()