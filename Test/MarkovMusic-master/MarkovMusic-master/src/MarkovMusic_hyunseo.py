import pysynth
import numpy as np
from .MarkovBuilder_hyunseo import MarkovBuilder


class MusicMatrix:
    def __init__(self, song=None):
        self._previous_note = None

        if song is not None:
            notes = np.array(song, dtype=int)[:, 0]
            durations = np.array(song, dtype=int)[:, 1]

        self._markov = MarkovBuilder(np.unique(notes).tolist())
        self._timings = MarkovBuilder(np.unique(durations).tolist())

        for note in song:
            self.add(note)

        self._markov.display()
        self._timings.display()

    def add(self, to_note):
        to_note = list(to_note)

        if(self._previous_note is None):
            self._previous_note = to_note
            return
        from_note = self._previous_note
        # add previous note and current note to matrix
        self._markov.add(from_note[0], to_note[0])
        # add previous duration and current duration to matrix
        self._timings.add(from_note[1], to_note[1])
        self._previous_note = to_note

    # 2022-07-29

    def next_note(self, from_note):
        from_note = list(from_note)
        # self._markov.next_value(from_note[0])
        # self._timings.next_value(from_note[1])
        return [self._markov.next_value(from_note[0]), self._timings.next_value(from_note[1])]
