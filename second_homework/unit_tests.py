import unittest
from second_homework import function_that_says_ni


class FunctionThatSaysNiValidShrubbery(unittest.TestCase):

    def setUp(self):
        self.first_valid_bush = {"name": "Храст", "cost": 12.20}
        self.second_valid_bush = {"name": "sHrub", "cost": 3}
        self.third_valid_bush = {"name": "buSH", "cost": 4.50}
        self.fourth_valid_bush = {"name": "Bush"}
        self.fifth_valid_bush = {"name": "Храст", "cost": 40}

        self.first_invalid_bush = {"cost": 4.50}
        self.second_invalid_bush = {"name": "malyk hrast", "cost": 4.50}
        self.third_invalid_bush = {"name": "ffff", "cost": 100}

    def test_with_all_valid_positional_bushes(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush, self.third_valid_bush)
        self.assertEqual(result, '19.70лв')

    def test_with_all_valid_positional_bushes_with_free_bush(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush, self.third_valid_bush,
                                       self.fourth_valid_bush)
        self.assertEqual(result, '19.70лв')

    def test_with_combined_positional_bushes(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush, self.third_valid_bush,
                                       self.first_invalid_bush)
        self.assertEqual(result, '19.70лв')

    def test_with_combined_positional_bushes_with_free_bush(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush, self.third_valid_bush,
                                       self.fourth_valid_bush, self.first_invalid_bush, self.second_invalid_bush)
        self.assertEqual(result, '19.70лв')

    def test_with_all_valid_named_bushes(self):
        result = function_that_says_ni(abcde=self.third_valid_bush, defg=self.second_valid_bush)
        self.assertEqual(result, '7.50лв')

    def test_with_all_valid_named_bushes_with_free_bush1(self):
        result = function_that_says_ni(abcde=self.third_valid_bush, defg=self.second_valid_bush,
                                       a=self.fourth_valid_bush)
        self.assertEqual(result, '7.50лв')

    def test_with_all_valid_named_bushes_with_free_bush2(self):
        result = function_that_says_ni(bcde=self.third_valid_bush, defg=self.second_valid_bush,
                                       a=self.fourth_valid_bush)
        self.assertEqual(result, '7.50лв')

    def test_with_combined_named_bushes(self):
        result = function_that_says_ni(abcde=self.third_valid_bush, defg=self.second_valid_bush,
                                       hij=self.first_invalid_bush, defa=self.second_invalid_bush)
        self.assertEqual(result, '7.50лв')

    def test_with_combined_named_bushes_with_free_bush1(self):
        result = function_that_says_ni(abcde=self.third_valid_bush, defg=self.second_valid_bush,
                                       hij=self.first_invalid_bush, a=self.fourth_valid_bush)
        self.assertEqual(result, '7.50лв')

    def test_with_combined_named_bushes_with_free_bush2(self):
        result = function_that_says_ni(bcde=self.third_valid_bush, defg=self.second_valid_bush,
                                       hij=self.first_invalid_bush, a=self.fourth_valid_bush)
        self.assertEqual(result, '7.50лв')

    def test_with_all_valid(self):
        result = function_that_says_ni(self.first_valid_bush,
                                       abcdefghijklmno=self.second_valid_bush)
        self.assertEqual(result, '15.20лв')

    def test_with_all_valid_with_free(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush,
                                       abcdefghijklmno=self.fourth_valid_bush)
        self.assertEqual(result, '15.20лв')

    def test_with_combined1(self):
        result = function_that_says_ni(self.first_valid_bush, self.first_invalid_bush,
                                       self.second_invalid_bush,
                                       aabccz=self.second_invalid_bush, abcdefghijklmno=self.second_valid_bush)
        self.assertEqual(result, '15.20лв')

    def test_with_combined2(self):
        result = function_that_says_ni(self.first_valid_bush, self.first_invalid_bush,
                                       self.second_invalid_bush,
                                       aabccz=self.first_invalid_bush, abcdefghijklmno=self.second_invalid_bush)
        self.assertEqual(result, '12.20лв')

    def test_with_combined3(self):
        result = function_that_says_ni(self.first_invalid_bush, self.second_invalid_bush,
                                       aabccz=self.first_valid_bush, abcdefghijklmn=self.second_valid_bush)
        self.assertEqual(result, '15.20лв')

    def test_with_combined4(self):
        result = function_that_says_ni(self.first_invalid_bush, self.second_invalid_bush,
                                       z=self.fourth_valid_bush, abbcdefg=self.third_valid_bush)
        self.assertEqual(result, '4.50лв')

    def test_with_combined_with_free1(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush, self.first_invalid_bush,
                                       self.second_invalid_bush,
                                       aabcc=self.second_invalid_bush, abcdefghijklmno=self.fourth_valid_bush)
        self.assertEqual(result, '15.20лв')

    def test_with_combined_with_free2(self):
        result = function_that_says_ni(self.second_valid_bush, self.first_invalid_bush,
                                       self.second_invalid_bush, abcdefg=self.fourth_valid_bush,
                                       hijklmn=self.third_valid_bush)
        self.assertEqual(result, '7.50лв')


class FunctionThatSaysNiInvalidShrubbery(unittest.TestCase):

    def setUp(self):
        self.first_valid_bush = {"name": "Храст", "cost": 12.20}
        self.second_valid_bush = {"name": "sHrub", "cost": 3}
        self.third_valid_bush = {"name": "buSH", "cost": 4.50}
        self.fourth_valid_bush = {"name": "Bush"}
        self.fifth_valid_bush = {"name": "Храст", "cost": 40}

        self.first_invalid_bush = {"cost": 4.50}
        self.second_invalid_bush = {"name": "malyk hrast", "cost": 4.50}
        self.third_invalid_bush = {"name": "ffff", "cost": 100}

    def test_with_empty_input(self):
        result = function_that_says_ni()
        self.assertEqual(result, 'Ni!')

    def test_with_all_valid_positional_expensive_bushes(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush,
                                       self.third_valid_bush, self.fifth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_all_valid_named_expensive_bushes(self):
        result = function_that_says_ni(a=self.first_valid_bush, b=self.second_valid_bush,
                                       c=self.third_valid_bush, d=self.fifth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_all_valid_combined_expensive_bushes(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush,
                                       a=self.third_valid_bush, b=self.fifth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_expensive_positional_bushes(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush,
                                       self.first_invalid_bush, self.second_invalid_bush,
                                       self.third_valid_bush, self.fifth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_expensive_named_bushes(self):
        result = function_that_says_ni(a=self.first_valid_bush, b=self.second_valid_bush,
                                       c=self.first_invalid_bush, d=self.second_invalid_bush,
                                       e=self.third_valid_bush, f=self.fifth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_expensive_combined_bushes(self):
        result = function_that_says_ni(self.first_valid_bush, self.second_valid_bush,
                                       self.first_invalid_bush, c=self.third_invalid_bush,
                                       a=self.third_valid_bush, b=self.fifth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_all_invalid_positional_bushes(self):
        result = function_that_says_ni(self.first_invalid_bush, self.second_invalid_bush)
        self.assertEqual(result, 'Ni!')

    def test_all_invalid_named_bushes(self):
        result = function_that_says_ni(a=self.first_invalid_bush, b=self.second_invalid_bush)
        self.assertEqual(result, 'Ni!')

    def test_all_invalid_bushes(self):
        result = function_that_says_ni(self.first_invalid_bush, a=self.third_invalid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_free_positional_bushes(self):
        result = function_that_says_ni(self.fourth_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_not_beautiful_named_bushes1(self):
        result = function_that_says_ni(c=self.third_invalid_bush, a=self.second_valid_bush, b=self.third_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_not_beautiful_named_bushes2(self):
        result = function_that_says_ni(cdefg=self.third_invalid_bush, a=self.second_valid_bush, b=self.third_valid_bush)
        self.assertEqual(result, 'Ni!')

    def test_with_not_beautiful_combined_bushes(self):
        result = function_that_says_ni(self.second_valid_bush, self.first_invalid_bush,
                                       abcd=self.third_invalid_bush, efgh=self.third_valid_bush)
        self.assertEqual(result, 'Ni!')


if __name__ == '__main__':
    unittest.main()
