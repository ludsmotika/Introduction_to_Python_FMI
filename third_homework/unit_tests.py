import unittest
import ast
from third_homework import Tone, Interval, Chord

# Replace with the path to the file
HOMEWORK_FILENAME = 'third_homework.py'


def check_class_in_file(filename, class_name):
    with open(filename, "r") as file:
        file_content = file.read()

    parsed_ast = ast.parse(file_content)

    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            return True
    return False


class TestClassPresence(unittest.TestCase):
    def test_class_presence(self):
        filename = HOMEWORK_FILENAME
        class_names = ['Tone', 'Interval', 'Chord']
        for name in class_names:
            self.assertTrue(check_class_in_file(filename, name),
                            f"Class {name} not found in {filename}")


INPUT_ERROR_MESSAGE = 'Invalid input type: Expected'
INVALID_OPERATION_ERROR_MESSAGE = 'Invalid operation'
VALID_TONES = (
    'C', 'C#', 'D', 'D#', 'E', 'F',
    'F#', 'G', 'G#', 'A', 'A#', 'B'
)


class TestTone(unittest.TestCase):

    def setUp(self):
        self.c = Tone('C')
        self.c_sharp = Tone('C#')
        self.d = Tone('D')
        self.d_sharp = Tone('D#')
        self.e = Tone('E')
        self.f = Tone('F')
        self.f_sharp = Tone('F#')
        self.g = Tone('G')
        self.g_sharp = Tone('G#')
        self.a = Tone('A')
        self.a_sharp = Tone('A#')
        self.b = Tone('B')
        self.tones = [self.c, self.c_sharp, self.d, self.d_sharp,
                      self.e, self.f, self.f_sharp, self.g,
                      self.g_sharp, self.a, self.a_sharp, self.b]

    def test_init_with_valid_tones(self):
        for tone in VALID_TONES:
            current_tone = Tone(tone)
            self.assertEqual(current_tone.tone, tone)

    """Test for my solution."""

    # def test_init_with_invalid_tones(self):
    #     with self.assertRaises(ValueError) as context:
    #         Tone("H")
    #     self.assertIn(f'{INPUT_ERROR_MESSAGE} one of {VALID_TONES}', str(context.exception))

    def test_tone_str(self):
        for index, tone in enumerate(self.tones):
            self.assertEqual(str(tone), VALID_TONES[index])

    def test_add_with_tone(self):
        result_chord = self.c + self.g
        self.assertIsInstance(result_chord, Chord)
        self.assertEqual(str(result_chord), 'C-G')

    def test_add_with_interval(self):
        perfect_fifth = Interval(7)
        result_tone = self.c + perfect_fifth
        self.assertEqual(str(result_tone), str(self.g))

        result_tone = self.c + Interval(12)
        self.assertEqual(str(result_tone), str(self.c))

        result_tone = self.g + perfect_fifth
        self.assertEqual(str(result_tone), str(self.d))

    def test_add_with_invalid_second_param_int(self):
        with self.assertRaises(TypeError) as context:
            self.c + 5
        self.assertIn(INVALID_OPERATION_ERROR_MESSAGE, str(context.exception))

    def test_add_with_invalid_second_param_bool(self):
        with self.assertRaises(TypeError) as context:
            self.c + True
        self.assertIn(INVALID_OPERATION_ERROR_MESSAGE, str(context.exception))

    def test_sub_with_tone(self):
        result = self.g - self.c
        first_expected_interval = Interval(7)
        self.assertEqual(str(result), str(first_expected_interval))

        result = self.c - self.g
        second_expected_interval = Interval(5)
        self.assertEqual(str(result), str(second_expected_interval))

    def test_sub_with_interval(self):
        perfect_fifth = Interval(7)
        result_tone = self.c - perfect_fifth
        self.assertEqual(str(result_tone), str(self.f))

        minor_third = Interval(3)
        result_tone = self.a_sharp - minor_third
        self.assertEqual(str(result_tone), str(self.g))

    def test_sub_with_invalid(self):
        with self.assertRaises(TypeError) as context:
            self.c - "invalid"
        self.assertIn(INVALID_OPERATION_ERROR_MESSAGE, str(context.exception))


INTERVAL_NAMES = (
    'unison', 'minor 2nd', 'major 2nd', 'minor 3rd',
    'major 3rd', 'perfect 4th', 'diminished 5th', 'perfect 5th',
    'minor 6th', 'major 6th', 'minor 7th', 'major 7th'
)

SHORTEST_INTERVAL = 0
LONGEST_INTERVAL = 11
INTERVALS_COUNT = 12


class TestInterval(unittest.TestCase):

    def setUp(self):
        self.unison = Interval(0)
        self.minor_second = Interval(1)
        self.major_second = Interval(2)
        self.minor_third = Interval(3)
        self.major_third = Interval(4)
        self.perfect_fourth = Interval(5)
        self.diminished_fifth = Interval(6)
        self.perfect_fifth = Interval(7)
        self.minor_sixth = Interval(8)
        self.major_sixth = Interval(9)
        self.minor_seventh = Interval(10)
        self.major_seventh = Interval(11)

        self.intervals = [self.unison, self.minor_second, self.major_second,
                          self.minor_third, self.major_third, self.perfect_fourth,
                          self.diminished_fifth, self.perfect_fifth, self.minor_sixth,
                          self.major_sixth, self.minor_seventh, self.major_seventh]

    def test_init(self):
        for index, interval in enumerate(self.intervals):
            self.assertEqual(interval.length, index)

    def test_set_length_with_big_number(self):
        result = Interval(13)
        self.assertEqual(result.length, 1)

    def test_str(self):
        for index, interval in enumerate(self.intervals):
            self.assertEqual(str(interval), INTERVAL_NAMES[index])

    def test_add_with_interval(self):
        result_interval = self.perfect_fifth + self.minor_third
        self.assertEqual(str(result_interval), str(self.minor_seventh))

    def test_add_with_tone(self):
        with self.assertRaises(TypeError) as context:
            self.unison + Tone('C')
        self.assertIn(INVALID_OPERATION_ERROR_MESSAGE, str(context.exception))


TONES_COUNT_ERROR_MESSAGE = 'Cannot have a chord made of only 1 unique tone'


class TestChord(unittest.TestCase):

    def test_init(self):
        c, d_sharp, g = Tone("C"), Tone("D#"), Tone("G")
        c_minor_chord = Chord(c, d_sharp, g)
        expected_tones = [Tone('C'), Tone('D#'), Tone('G')]
        for index, tone in enumerate(c_minor_chord.tones):
            self.assertEqual(str(tone), str(expected_tones[index]))

        c, another_c, f = Tone("C"), Tone("C"), Tone("F")
        csus4_chord = Chord(c, f, another_c)
        expected_tones = [Tone('C'), Tone('F')]
        for index, tone in enumerate(csus4_chord.tones):
            self.assertEqual(str(tone), str(expected_tones[index]))

        f, c, d, a, g = Tone("F"), Tone("C"), Tone("D"), Tone("A"), Tone("G")
        f_sixth_ninth_chord = Chord(f, c, d, a, g)
        expected_tones = [Tone('F'), Tone('G'), Tone('A'), Tone('C'), Tone('D')]
        for index, tone in enumerate(f_sixth_ninth_chord.tones):
            self.assertEqual(str(tone), str(expected_tones[index]))

    def test_str(self):
        c, d_sharp, g = Tone("C"), Tone("D#"), Tone("G")
        c_minor_chord = Chord(c, d_sharp, g)
        self.assertEqual(str(c_minor_chord), 'C-D#-G')

        c, another_c, f = Tone("C"), Tone("C"), Tone("F")
        csus4_chord = Chord(c, f, another_c)
        self.assertEqual(str(csus4_chord), 'C-F')

        f, c, d, a, g = Tone("F"), Tone("C"), Tone("D"), Tone("A"), Tone("G")
        f_sixth_ninth_chord = Chord(f, c, d, a, g)
        self.assertEqual(str(f_sixth_ninth_chord), 'F-G-A-C-D')

    def test_init_with_invalid_tones_count(self):
        with self.assertRaises(TypeError) as context:
            Chord(Tone('C'), Tone('C'))
        self.assertIn(TONES_COUNT_ERROR_MESSAGE, str(context.exception))

    def test_is_minor(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        self.assertEqual(c_minor_chord.is_minor(), True)
        c_not_minor_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
        self.assertEqual(c_not_minor_chord.is_minor(), False)

    def test_is_major(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        self.assertEqual(c_major_chord.is_major(), True)
        c_not_major_chord = Chord(Tone("C"), Tone("D"), Tone("G"))
        self.assertEqual(c_not_major_chord.is_major(), False)

    def test_is_power(self):
        c_power_chord = Chord(Tone("C"), Tone("F"), Tone("G"))
        self.assertEqual(c_power_chord.is_power_chord(), True)

        c_not_power_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        self.assertEqual(c_not_power_chord.is_power_chord(), False)

    def test_add_with_tone(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        result_chord = c5_chord + Tone("E")
        self.assertEqual(str(result_chord),'C-E-G')

        second_result_chord = result_chord + Tone("E")
        self.assertEqual(str(second_result_chord),'C-E-G')

    def test_add_with_chord(self):
        c5_chord = Chord(Tone("C"), Tone("G"))
        this_other_chord = Chord(Tone("A"), Tone("B"))
        result_chord = c5_chord + this_other_chord
        self.assertEqual(str(result_chord),'C-G-A-B')

        first_chord = Chord(Tone("C"), Tone("B"))
        second_chord = Chord(Tone("A"), Tone("B"))
        result_chord = first_chord + second_chord
        self.assertEqual(str(result_chord),'C-A-B')

    def test_sub_with_valid_tone(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        result_chord = c_major_chord - Tone("E")
        self.assertEqual(str(result_chord),'C-G')

    def test_sub_with_invalid_tone(self):
        with self.assertRaises(TypeError) as context:
            chord =  Chord(Tone("C"), Tone("G"))
            chord - Tone("G")
        self.assertEqual(TONES_COUNT_ERROR_MESSAGE, str(context.exception))

    def test_sub_with_non_included_tone(self):
        with self.assertRaises(TypeError) as context:
            c_power_chord = Chord(Tone("C"), Tone("G"))
            result_chord = c_power_chord - Tone("E")
        self.assertEqual('Cannot remove tone E from chord C-G', str(context.exception))

    def test_sub_with_main_tone(self):
        c_major_chord = Chord(Tone("C"), Tone("E"), Tone("G"))
        result_chord = c_major_chord - Tone("C")
        self.assertEqual(str(result_chord), 'E-G')

    def test_transposed(self):
        c_minor_chord = Chord(Tone("C"), Tone("D#"), Tone("G"))
        d_minor_chord = c_minor_chord.transposed(Interval(2))
        self.assertEqual(str(d_minor_chord), 'D-F-A')

        a_sharp_minor_chord = d_minor_chord.transposed(-Interval(4))
        self.assertEqual(str(a_sharp_minor_chord), 'A#-C#-F')


if __name__ == '__main__':
    unittest.main()
