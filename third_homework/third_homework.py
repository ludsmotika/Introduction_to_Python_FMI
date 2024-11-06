INPUT_ERROR_MESSAGE = 'Invalid input type: Expected'
INVALID_OPERATION_ERROR_MESSAGE = 'Invalid operation'
VALID_TONES = (
    'C', 'C#', 'D', 'D#', 'E', 'F',
    'F#', 'G', 'G#', 'A', 'A#', 'B'
)


class Tone:

    def __init__(self, tone):
        self.tone = tone

    @property
    def tone(self):
        return self._tone

    @tone.setter
    def tone(self, value):
        if value not in VALID_TONES:
            raise ValueError(f'{INPUT_ERROR_MESSAGE} one of {VALID_TONES}')
        self._tone = value

    def __str__(self):
        return self.tone

    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self, other)
        elif isinstance(other, Interval):
            starting_index = VALID_TONES.index(self.tone)
            shifted_tone = VALID_TONES[(starting_index + other.length) % INTERVALS_COUNT]
            return Tone(shifted_tone)

        raise TypeError(INVALID_OPERATION_ERROR_MESSAGE)

    def __sub__(self, other):
        if isinstance(other, Tone):
            first_tone_index = VALID_TONES.index(self.tone)
            second_tone_index = VALID_TONES.index(other.tone)
            interval_len = first_tone_index - second_tone_index

            if first_tone_index <= second_tone_index:
                interval_len += INTERVALS_COUNT

            return Interval(interval_len)
        elif isinstance(other, Interval):
            starting_index = VALID_TONES.index(self.tone)
            shifted_tone = VALID_TONES[starting_index - other.length]
            return Tone(shifted_tone)

        raise TypeError(INVALID_OPERATION_ERROR_MESSAGE)


# The indices correspond to the interval length
INTERVAL_NAMES = (
    'unison', 'minor 2nd', 'major 2nd', 'minor 3rd',
    'major 3rd', 'perfect 4th', 'diminished 5th', 'perfect 5th',
    'minor 6th', 'major 6th', 'minor 7th', 'major 7th'
)

SHORTEST_INTERVAL = 0
LONGEST_INTERVAL = 11
INTERVALS_COUNT = 12


class Interval:

    def __init__(self, length, is_direction_forward=True):
        self._set_length(length)
        self._is_direction_forward = is_direction_forward

    def __neg__(self):
        return Interval(self.length, False)

    @property
    def is_direction_forward(self):
        return self._is_direction_forward

    @property
    def length(self):
        return self._length

    def _set_length(self, value):
        if not isinstance(value, int):
            raise TypeError(f'{INPUT_ERROR_MESSAGE} {str(int)}')

        if value < SHORTEST_INTERVAL:
            raise ValueError(f'{INPUT_ERROR_MESSAGE} a non-negative integer')

        self._length = value % INTERVALS_COUNT

    def __str__(self):
        return INTERVAL_NAMES[self.length]

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.length + other.length)
        raise TypeError(INVALID_OPERATION_ERROR_MESSAGE)


MIN_TONES_COUNT_IN_CHORD = 2
TONES_COUNT_ERROR_MESSAGE = 'Cannot have a chord made of only 1 unique tone'


def rearrange_tuple(input_tuple, skip_index):
    start_index = skip_index + 1
    end_index = skip_index - 1


    if start_index <= end_index:
        result_tuple = input_tuple[start_index:end_index + 1]
    else:
        result_tuple = input_tuple[start_index:] + input_tuple[:end_index + 1]

    if skip_index is not None:
        skip_tone = input_tuple[skip_index]
        result_tuple = [tone for tone in result_tuple if tone != skip_tone]

    return result_tuple


class Chord:
    def __init__(self, main_tone, *args, **kwargs):
        secondary_tones = list(args) + list(kwargs.values())
        self.tones = Chord._extract_and_sort_tones(main_tone, secondary_tones)

    @property
    def tones(self):
        return self._tones

    @property
    def main_tone(self):
        return self._tones[0]

    @property
    def secondary_tones(self):
        return self._tones[1:]

    @tones.setter
    def tones(self, value):
        if len(value) < MIN_TONES_COUNT_IN_CHORD:
            raise TypeError(TONES_COUNT_ERROR_MESSAGE)

        self._tones = value

    @staticmethod
    def _extract_and_sort_tones(main_tone, secondary_tones=None):

        if secondary_tones is None:
            return list(main_tone)

        unique_secondary_tones = set(filter(lambda tone: str(tone) != str(main_tone), secondary_tones))
        unique_secondary_tones_strs = [str(tone) for tone in unique_secondary_tones]

        main_tone_index = VALID_TONES.index(str(main_tone))
        rearranged_tones = rearrange_tuple(VALID_TONES, main_tone_index)

        sorted_tones = [main_tone]

        for tone in rearranged_tones:
            if tone in unique_secondary_tones_strs:
                sorted_tones.append(next((t for t in unique_secondary_tones if str(t) == tone)))

        return sorted_tones

    def __str__(self):
        return '-'.join([str(tone) for tone in self.tones])

    def _contains_interval(self, interval):
        first_possible_tone = VALID_TONES[self.tones.index(self.main_tone) - interval.length]
        second_possible_tone = VALID_TONES[self.tones.index(self.main_tone) + interval.length]

        if any(str(tone) in [first_possible_tone, second_possible_tone] for tone in self.tones):
            return True

        return False

    def is_minor(self):
        return self._contains_interval(Interval(3))

    def is_major(self):
        return self._contains_interval(Interval(4))

    def is_power_chord(self):
        return not self.is_minor() and not self.is_major()

    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self.main_tone, *self.secondary_tones, other)
        elif isinstance(other, Chord):
            return Chord(self.main_tone, *self.secondary_tones, *other.tones)

    def __sub__(self, tone_to_remove):
        if str(tone_to_remove) not in [str(tone) for tone in self.tones]:
            raise TypeError(f'Cannot remove tone {str(tone_to_remove)} from chord {str(self)}')

        if len(self.tones) <= MIN_TONES_COUNT_IN_CHORD:
            raise TypeError(TONES_COUNT_ERROR_MESSAGE)

        if str(self.main_tone) == str(tone_to_remove):
            return Chord(self.tones[1], *self.secondary_tones)

        updated_tones = [tone for tone in self.secondary_tones if str(tone) != str(tone_to_remove)]
        return Chord(self.main_tone, *updated_tones)

    def transposed(self, interval):
        if interval.is_direction_forward:
            shifted_secondary_tones = [tone + interval for tone in self.secondary_tones]
            return Chord(self.main_tone + interval, *shifted_secondary_tones)

        shifted_secondary_tones = [tone - interval for tone in self.secondary_tones]
        return Chord(self.main_tone - interval, *shifted_secondary_tones)