import pytest

from fretboard import Fretboard


@pytest.mark.parametrize(
    'n_frets,string_intervals,n_strings,note_offset',
    [
        (12, [5, 5, 5, 4, 5], None, 6),  # 6 string guitar with standard tuning
        (17, 5, 17, 0),  # 17 x 17 guitar tuned to perfect fourths
    ])
def test_fretboard_init(n_frets, string_intervals, n_strings, note_offset):
    Fretboard(
        n_frets=n_frets,
        string_intervals=string_intervals,
        n_strings=n_strings,
        note_offset=note_offset
    )
