from random import choice
from time import sleep, time


class NoteSelector:

    all_strings = 'E A D G B e'.split()
    natural_notes = 'A B C D E F G'.split()
    sharp_notes = 'A# C# D# F# G#'.split()
    flat_notes = 'Ab Bb Db Eb Gb'.split()

    def __init__(self, n_strings=6, natural=True, sharp=True, flat=True):
        self.strings = self.all_strings[:n_strings]
        self.notes = []
        if natural:
            self.notes += self.natural_notes
        if sharp:
            self.notes += self.sharp_notes
        if flat:
            self.notes += self.flat_notes

    def run_exercise(self, beats_per_minute, practice_time):
        seconds_per_beat = 60 / beats_per_minute

        last_position = None
        next_position = None

        start_time = time()

        while (time() - start_time) < practice_time:
            while next_position == last_position:
                next_note = choice(self.notes)
                next_string = choice(self.strings)
                next_position = (next_string, next_note)
            print(f'\r({next_string}) {next_note}')
            last_position = next_position
            sleep(seconds_per_beat)


def main():
    note_selector = NoteSelector(n_strings=2, natural=True, sharp=False, flat=False)
    note_selector.run_exercise(30, 60)


if __name__ == '__main__':
    main()
