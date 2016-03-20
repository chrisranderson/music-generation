from mido import MidiFile
from mido.midifiles import MidiTrack

class Song:

    def __init__(self):
        self.notes = []

    def read_file(self, file):
        new_track = MidiTrack()

        mid = MidiFile(file)

        for i, track in enumerate(mid.tracks):
            for message in track:
                new_track.append(message)

        new_mid.tracks.append(new_track)
