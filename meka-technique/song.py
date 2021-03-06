import mido
from mido import MidiFile
from mido.midifiles import MidiTrack

from note import Note


class Song:

    def __init__(self):
        self.notes = []
        self.counter = 0

    def read_file(self, filename):
        mid = MidiFile(filename)

        # An internal clock that keeps track of current time based on the
        # cumulative elapsed time delta of each note
        current_time = 0

        elapsed_time = 0

        for _, track in enumerate(mid.tracks):
            for message in track:
                # Increment internal clock
                current_time += message.time

                current_time

                if message.type == 'note_on':
                    # Create a new note for this note_on (no time information
                    # yet)
                    note = Note(
                        message.channel, message.note, message.velocity, elapsed_time, current_time)

                    self.notes.append(note)

                    elapsed_time = 0

                elif message.type == 'note_off':
                    end_note = Note(
                        message.channel, message.note, message.velocity)

                    for note in reversed(self.notes):
                        if note == end_note and note.duration == None:
                            note.add_duration(current_time)
                            break

                # If we haven't started a new note, we need to increment
                # the elapsed time since the last note
                if message.type != 'note_on':

                    elapsed_time += message.time

    def write_file(self, filename=None):
        with MidiFile() as midi_song:
            unused_notes = []
            current_time = 0
            new_track = MidiTrack()
            new_track.append(mido.Message('program_change', channel=1, program=29, time=5))
            new_track.append(mido.Message('program_change', channel=2, program=30, time=5))
            new_track.append(mido.Message('program_change', channel=3, program=31, time=5))
            new_track.append(mido.Message('program_change', channel=4, program=32, time=5))
            new_track.append(mido.Message('program_change', channel=5, program=33, time=5))
            new_track.append(mido.Message('program_change', channel=6, program=34, time=5))
            new_track.append(mido.Message('program_change', channel=7, program=35, time=5))
            new_track.append(mido.Message('program_change', channel=8, program=36, time=5))
            new_track.append(mido.Message('program_change', channel=9, program=37, time=5))

            for note in self.notes:
                note.absolute_start = current_time + note.time_delta
                note_start = note.absolute_start

                best_end = float('inf')
                best_end_note = None

                for unused_note in unused_notes:
                    this_end = unused_note.get_absolute_end()

                    if this_end < best_end:
                        best_end = this_end
                        best_end_note = unused_note

                if best_end < note_start:
                    new_track.append(
                        best_end_note.get_note_off(best_end - current_time))
                    unused_notes.remove(note)
                    current_time = best_end
                else:
                    new_track.append(note.get_note_on())
                    unused_notes.append(note)
                    current_time = note_start

            midi_song.tracks.append(new_track)
            midi_song.save(filename)

    def has_next_note(self):
        return self.counter < len(self.notes)

    def get_next_note_as_arff(self, n=5):
        """
        Get the next n notes as a line in an arff file
        """

        array = []

        # Bug - This assumes that there are more than n notes
        number_notes = n - max(n - self.counter, 0)

        for _ in range(max(n - self.counter, 0)):
            array += [1000, 1000, 1000, -1, -1]

        for note_index in reversed(range(number_notes)):
            array += self.notes[self.counter - note_index].get_note_array()

        self.counter += 1

        return array, self.notes[self.counter].get_note_array()

    def get_last_notes(self, n=5):

        array = []

        if n < len(self.notes):
            number_notes = n
        else:
            number_notes = len(self.notes)

        for _ in range(n - number_notes):
            array += [1000, 1000, 1000, -1, -1]

        for note_index in range(len(self.notes) - number_notes, len(self.notes)):
            array += self.notes[note_index].get_note_array()

        return array

    def get_arff_arrays(self):

        # TODO: Convert these all to numpy arrays.
        array_instrument = []
        array_note = []
        array_velocity = []
        array_duration = []
        array_time_delta = []

        for _ in range(len(self.notes) - 1):
            next_line, output = self.get_next_note_as_arff()
            array_instrument.append(next_line + [output[0]])
            array_note.append(next_line + [output[1]])
            array_velocity.append(next_line + [output[2]])
            array_duration.append(next_line + [output[3]])
            if output[4] != 0:
                array_time_delta.append(next_line + [output[4]])

        return array_instrument, array_note, array_velocity, array_duration, array_time_delta

    def add_note(self, note):
        self.notes.append(note)

# song = Song()
# song.read_file('../Rollinginthedeep.mid')
# song.write_file('../Rollinginthedeep2.mid')
