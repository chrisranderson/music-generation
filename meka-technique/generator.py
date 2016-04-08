import os
import arff
import numpy as np
from music import Music

from sklearn import tree

class Generator:

    def __init__(self):
        self.music = Music()

    def write_arffs(self):
        for file in os.listdir('midi'):
            if os.path.isfile('midi/' + file):
                print 'adding midi/' + file
                self.music.load_song('midi/' + file)

        print 'generating arff files'
        self.music.write_arff('test')

    def train(self):
        print 'loading arff files'
        instrument_data, note_data, velocity_data, duration_data, time_delta_data = self.music.read_arff('test')

        print 'training instruments'
        self.instrument_clf = tree.DecisionTreeClassifier()
        self.instrument_clf = self.instrument_clf.fit(instrument_data[:,:-1], instrument_data[:,-1:])
        print 'training notes'
        self.note_clf = tree.DecisionTreeClassifier()
        self.note_clf = self.note_clf.fit(note_data[:,:-1], note_data[:,-1:])
        print 'training velocity'
        self.velocity_clf = tree.DecisionTreeClassifier()
        self.velocity_clf = self.velocity_clf.fit(velocity_data[:,:-1], velocity_data[:,-1:])
        print 'training duration'
        self.duration_clf = tree.DecisionTreeClassifier()
        self.duration_clf = self.duration_clf.fit(duration_data[:,:-1], duration_data[:,-1:])
        print 'training time_delta'
        self.time_delta_clf = tree.DecisionTreeClassifier()
        self.time_delta_clf = self.time_delta_clf.fit(time_delta_data[:,:-1], time_delta_data[:,-1:])


    def generate_song(self):
        pass

generator = Generator()
generator.write_arffs()
generator.train()
