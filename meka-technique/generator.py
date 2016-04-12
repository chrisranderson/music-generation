import os

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

from music import Music
from note import Note
import numpy as np
from song import Song
import random


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
        
        self.transform_instrument = preprocessing.OneHotEncoder(categorical_features=[0,1,2,5,6,7,10,11,12,15,16,17,20,21,22])
        self.transform_instrument.fit(instrument_data[:, :-1])

        self.transform_note = preprocessing.OneHotEncoder(categorical_features=[0,1,2,5,6,7,10,11,12,15,16,17,20,21,22])
        self.transform_note.fit(note_data[:, :-1])

        self.transform_duration = preprocessing.OneHotEncoder(categorical_features=[0,1,2,5,6,7,10,11,12,15,16,17,20,21,22])
        self.transform_duration.fit(duration_data[:, :-1])

        self.transform_time_delta = preprocessing.OneHotEncoder(categorical_features=[0,1,2,5,6,7,10,11,12,15,16,17,20,21,22])
        self.transform_time_delta.fit(time_delta_data[:, :-1])

        print "training instruments"
        self.instrument_clf = RandomForestClassifier(n_estimators=10)
        self.instrument_clf = self.instrument_clf.fit(
            self.transform_instrument.transform(instrument_data[:, :-1]), instrument_data[:, -1:])
        print "training notes"
        self.note_clf = RandomForestRegressor(n_estimators=10)
        print note_data[:, :-1]
        self.note_clf = self.note_clf.fit(self.transform_note.transform(note_data[:, :-1]), note_data[:, -1:])
        print "training velocity"
        self.velocity_clf = RandomForestClassifier(n_estimators=10)
        self.velocity_clf = self.velocity_clf.fit(
            velocity_data[:, :-1], velocity_data[:, -1:])
        print "training duration"
        self.duration_clf = RandomForestClassifier(n_estimators=10)
        self.duration_clf = self.duration_clf.fit(
            self.transform_duration.transform(duration_data[:, :-1]), duration_data[:, -1:])
        print "training time_delta"
        self.time_delta_clf = RandomForestClassifier(n_estimators=10)
        self.time_delta_clf = self.time_delta_clf.fit(
            self.transform_time_delta.transform(time_delta_data[:, :-1]), time_delta_data[:, -1:])

    def generate_song(self, filename):
        self.song = Song()

        self.song.add_note(self.get_seed_note())
        self.song.add_note(self.get_seed_note())

        print "generating new song"
        for _ in range(5000):
            notes = self.song.get_last_notes()
            notes = np.array(notes).reshape(1, -1)
            instrument = self.instrument_clf.predict(self.transform_instrument.transform(notes))[0]
            note = self.note_clf.predict(self.transform_note.transform(notes))[0]
            velocity = self.velocity_clf.predict(notes)[0]
            note_duration = self.duration_clf.predict(self.transform_duration.transform(notes))[0] * 2
            time_delta = self.time_delta_clf.predict(self.transform_time_delta.transform(notes))[0] * 0.75

            self.song.add_note(Note(int(instrument), int(note), int(
                velocity), int(time_delta), duration=int(note_duration)))

        print "writing song to " + filename
        self.song.write_file(filename)

    def get_seed_note(self):
        return Note(0, random.randrange(0, 126), 100, 0, duration=random.randrange(1, 10) * 10)

generator = Generator()
generator.write_arffs()
generator.train()
generator.generate_song("generated.mid")
