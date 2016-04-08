import os

from sklearn import tree

from music import Music
from note import Note
import numpy as np
from song import Song


class Generator:

    def __init__(self):
        self.music = Music()

    def write_arffs(self):
        for next_file in os.listdir("midi"):
            if os.path.isfile("midi/" + next_file):
                print "adding midi/" + next_file
                self.music.load_song("midi/" + next_file)

        print "generating arff files"
        self.music.write_arff("test")

    def train(self):
        print "loading arff files"
        instrument_data, note_data, velocity_data, duration_data, time_delta_data = self.music.read_arff(
            "test")

        print "training instruments"
        self.instrument_clf = tree.DecisionTreeClassifier()
        self.instrument_clf = self.instrument_clf.fit(
            instrument_data[:, :-1], instrument_data[:, -1:])
        print "training notes"
        self.note_clf = tree.DecisionTreeClassifier()
        self.note_clf = self.note_clf.fit(note_data[:, :-1], note_data[:, -1:])
        print "training velocity"
        self.velocity_clf = tree.DecisionTreeClassifier()
        self.velocity_clf = self.velocity_clf.fit(
            velocity_data[:, :-1], velocity_data[:, -1:])
        print "training duration"
        self.duration_clf = tree.DecisionTreeRegressor()
        self.duration_clf = self.duration_clf.fit(
            duration_data[:, :-1], duration_data[:, -1:])
        print "training time_delta"
        self.time_delta_clf = tree.DecisionTreeRegressor()
        self.time_delta_clf = self.time_delta_clf.fit(
            time_delta_data[:, :-1], time_delta_data[:, -1:])

    def generate_song(self, filename):
        self.song = Song()

        self.song.add_note(self.get_seed_note())

        print "generating new song"
        for _ in range(1000):
            notes = self.song.get_last_notes()
            notes = np.array(notes).reshape(1, -1)
            instrument = self.instrument_clf.predict(notes)[0]
            note = self.note_clf.predict(notes)[0]
            velocity = self.velocity_clf.predict(notes)[0]
            note_duration = self.duration_clf.predict(notes)[0]
            time_delta = self.time_delta_clf.predict(notes)[0]

            self.song.add_note(Note(int(instrument), int(note), int(
                velocity), int(time_delta), duration=int(note_duration)))

        print "writing song to " + filename
        self.song.write_file(filename)

    def get_seed_note(self):
        return Note(0, 3, 3, 0, duration=1000)

generator = Generator()
generator.write_arffs()
generator.train()
generator.generate_song("generated.mid")
