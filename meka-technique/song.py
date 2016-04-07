from mido import MidiFile
from mido.midifiles import MidiTrack

from note import Note

class Song:

    def __init__(self):
        self.notes = []
        self.counter = 0

    def read_file(self, file):
        mid = MidiFile(file)

        # An internal clock that keeps track of current time based on the
        # cumulative elapsed time delta of each note
        current_time = 0

        elapsed_time = 0

        for i, track in enumerate(mid.tracks):
            for message in track:
                # Increment internal clock
                current_time += message.time

                if message.type == "note_on":
                    elapsed_time = 0

                    # Create a new note for this note_on (no time information yet)
                    note = Note(message.channel, message.note, message.velocity, elapsed_time, current_time)

                    self.notes.append(note)

                elif message.type == "note_off":
                    end_note = Note(message.channel, message.note, message.velocity)

                    for note in self.notes:
                        if note == end_note:
                            note.add_duration(current_time)

                # If we haven't started a new note, we need to increment
                # the elapsed time since the last note
                if message.type != "note_on":

                    elapsed_time += message.time


    def write_file(self, file_name = None):
        with MidiFile() as midi_song:
            unused_notes = []
            current_time = 0
            new_track = MidiTrack()

            for note in self.notes:
                note_start = note.absolute_start

                best_end = float("inf")
                best_end_note = None

                for unused_note in unused_notes:
                    this_end = unusued_note.get_absolute_end()

                    if this_end < best_end:
                        best_end = this_end
                        best_end_note = unused_note

                if best_end < note_start:
                    pass
                    # some stuff
                else:
                    print("adding ", note.get_note_on(note_start - current_time))
                    new_track.append(note.get_note_on(note_start - current_time))
                    current_time = note_start

            midi_song.tracks.append(new_track)
            midi_song.save(file_name)

    def has_next_note(self):
        return self.counter < len(self.notes)

    def get_next_note_as_arff(self, n = 5):
        '''
        Get the next n notes as a line in an arff file
        '''

        array = []

        number_notes = n - max(n - self.counter, 0)

        for empty_note in range(max(n - self.counter, 0)):
            array += [-1, -1, -1, -1, -1]

        for note_index in range(number_notes):
            array += self.notes[self.counter - note_index].get_note_array()

        self.counter += 1

        return array, self.notes[self.counter].get_note_array()

    def get_arff_arrays(self):

        # TODO: Convert these all to numpy arrays.
        array_instrument = []
        array_note = []
        array_velocity = []
        array_duration = []
        array_time_delta = []

        for note_index in range(len(self.notes) - 1):
            next_line, output = self.get_next_note_as_arff()
            print next_line
            print output
            array_instrument.append(next_line + [ output[0] ])
            array_note.append(next_line + [ output[1] ])
            array_velocity.append(next_line + [ output[2] ])
            array_duration.append(next_line + [ output[3] ])
            array_time_delta.append(next_line + [ output[4] ])

        return array_instrument, array_note, array_velocity, array_duration, array_time_delta

# song = Song()
# song.read_file("../Rollinginthedeep.mid")
# song.write_file("../Rollinginthedeep2.mid")
