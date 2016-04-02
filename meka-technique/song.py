from mido import MidiFile
from mido.midifiles import MidiTrack

from note import Note

class Song:

    def __init__(self):
        self.notes = []

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
                # the elapsed time sincde the last note
                if message.type != "note_on":

                    elapsed_time += message.time


    def write_file(self, file_name = None):

        with open(file_name) as file:
            current_time = 0


song = Song()
song.read_file("../Rollinginthedeep.mid")
