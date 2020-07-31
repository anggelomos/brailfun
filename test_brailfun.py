import unittest
from brailfun import new_cell

testing_cell = new_cell(power=5, time_on=1, time_off=1)

class test_brailfun(unittest.TestCase):

    def test_clamp_01(self):
        testcase = [-5, 0, 140, 73.25, 255, 302]
        expected = [0, 0, 140, 73.25, 255, 255]
        for index, _ in enumerate(testcase):
            self.assertEqual(testing_cell.clamp(testcase[index]), expected[index])

    def test_clamp_02(self):
        testcase = ["a", ["a"], {"a"}, set("a"), ("a")]
        expected = []
        for index, _ in enumerate(testcase):
            with self.assertRaises(TypeError):
                testing_cell.clamp(testcase[index])

    def test_random_letter(self):
        testcase = "abcdefghijklmnñopqrstuvwxyz"
        self.assertIn(testing_cell.random_letter(), testcase)

    def test_translator(self):
        testcase = [" ","a", "j", "s", "w"]
        expected = [[0,0,0,0,0,0],[1,0,0,0,0,0], [0,1,0,1,1,0], [0,1,1,1,0,0], [0,1,0,1,1,1]]
        for index, _ in enumerate(testcase):
            self.assertEqual(testing_cell.translator(testcase[index]), expected[index])

if __name__ == "__main__":
    unittest.main()