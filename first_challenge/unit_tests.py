import unittest
from unittest.mock import call, patch

from first_challenge import type_check


def join_collections(*collections):
    result = []
    for collection in collections:
        result.extend(collection)
    return result

def nothing():
    pass

def lonely_island(main_character, supporting_character, **kwargs):
    return f"This is the tale of {main_character} and {supporting_character}!"

def divide_by_zero(numbers):
    return [number / 0 for number in numbers]


class TestTypeCheck(unittest.TestCase):
    """Test the function of the decorator."""

    @patch("builtins.print")
    def test_check_in(self, mock_print):
        """The decorator should report invalid "in" arguments."""
        # Single type
        decorated = type_check("in")(list)(join_collections)
        result = decorated('asdf', 'movie')
        mock_print.assert_has_calls(
            [call("Invalid input arguments, expected <class 'list'>!")])
        self.assertEqual(mock_print.call_count, 1)
        self.assertEqual(result, ['a', 's', 'd', 'f', 'm', 'o', 'v', 'i', 'e'])

        # Multiple types
        mock_print.reset_mock()
        decorated = type_check("in")(list, tuple, set, type(_ for _ in []))(join_collections)
        result = decorated('asdf', 'movie')
        mock_print.assert_has_calls(
            [call("Invalid input arguments, expected <class 'list'>, <class 'tuple'>, <class 'set'>, <class 'generator'>!")])
        self.assertEqual(mock_print.call_count, 1)
        self.assertEqual(result, ['a', 's', 'd', 'f', 'm', 'o', 'v', 'i', 'e'])

        # Valid input
        mock_print.reset_mock()
        decorated = type_check("in")(list, tuple, set, type(_ for _ in []))(join_collections)
        result = decorated([1, 2], (3,), {4})
        mock_print.assert_not_called()
        self.assertEqual(result, [1, 2, 3, 4])

    @patch("builtins.print")
    def test_check_out(self, mock_print):
        """The decorator should report an invalid "out" value."""
        # Single type
        decorated = type_check("out")(
            type("Epyt", (type,),{"__repr__": lambda self: f"{self.__name__[::-1].lower()} {self.__class__.__name__[::-1].lower()}"})("Ym", (), {}))(nothing)
        # Why do I do these things?
        result = decorated()
        mock_print.assert_has_calls(
            [call("Invalid output value, expected my type!")])
        self.assertEqual(mock_print.call_count, 1)
        self.assertEqual(result, None)

        # Multiple types
        mock_print.reset_mock()
        decorated = type_check("out")(str, bool, Exception)(nothing)
        result = decorated()
        mock_print.assert_has_calls(
            [call("Invalid output value, expected <class 'str'>, <class 'bool'>, <class 'Exception'>!")])
        self.assertEqual(mock_print.call_count, 1)
        self.assertEqual(result, None)

        # Valid output
        mock_print.reset_mock()
        decorated = type_check("out")(type(None))(nothing)
        result = decorated()
        mock_print.assert_not_called()
        self.assertEqual(result, None)

    @patch("builtins.print")
    def test_check_both(self, mock_print):
        """The decorator should report invalid "in" and "out" together."""
        decorated = type_check("in")(float)(lonely_island)
        decorated = type_check("out")(int)(decorated)
        result = decorated("Captain Jack Sparrow", "Bill", pirates=True)
        mock_print.assert_has_calls(
            [call("Invalid input arguments, expected <class 'float'>!"),
             call("Invalid output value, expected <class 'int'>!")])
        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(result, "This is the tale of Captain Jack Sparrow and Bill!")

    @patch("builtins.print")
    def test_check_decorated_exception(self, mock_print):
        """The decorator should not supress any exceptions raised."""
        decorated = type_check("in")(list, tuple)(divide_by_zero)
        decorated = type_check("out")(list, tuple)(decorated)
        with self.assertRaises(ZeroDivisionError):
            decorated({1, 2, 3, 4, 5, 6})
        mock_print.assert_has_calls([call("Invalid input arguments, expected <class 'list'>, <class 'tuple'>!")])

if __name__ == '__main__':
    unittest.main()