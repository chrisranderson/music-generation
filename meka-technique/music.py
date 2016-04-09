import copy

import arff

import numpy as np
from song import Song


arff_format = {
    'description': u'',
    'relation': 'instrument',
    'attributes': [
        ('instrument', 'REAL'),
        ('note_1', 'REAL'),
        ('velocity_1', 'REAL'),
        ('duration_1', 'REAL'),
        ('time_delta_1', 'REAL'),
        ('instrument', 'REAL'),
        ('note_2', 'REAL'),
        ('velocity_2', 'REAL'),
        ('duration_2', 'REAL'),
        ('time_delta_2', 'REAL'),
        ('instrument', 'REAL'),
        ('note_3', 'REAL'),
        ('velocity_3', 'REAL'),
        ('duration_3', 'REAL'),
        ('time_delta_3', 'REAL'),
        ('instrument', 'REAL'),
        ('note_4', 'REAL'),
        ('velocity_4', 'REAL'),
        ('duration_4', 'REAL'),
        ('time_delta_4', 'REAL'),
        ('instrument', 'REAL'),
        ('note_5', 'REAL'),
        ('velocity_5', 'REAL'),
        ('duration_5', 'REAL'),
        ('time_delta_5', 'REAL'),
        ('output_channel', 'REAL')
    ],
    'data': [
    ],
}


class Music:

    def __init__(self):
        self.songs = []

    def load_song(self, filename):
        song = Song()
        song.read_file(filename)

        self.songs.append(song)

    def write_arff(self, filename):
        instrument_arff = copy.deepcopy(arff_format)
        note_arff = copy.deepcopy(arff_format)
        velocity_arff = copy.deepcopy(arff_format)
        duration_arff = copy.deepcopy(arff_format)
        time_delta_arff = copy.deepcopy(arff_format)

        with open(filename + "_instrument.arff", 'w') as instrument_file, \
                open(filename + "_note.arff", 'w') as note_file, \
                open(filename + "_velocity.arff", 'w') as velocity_file, \
                open(filename + "_duration.arff", 'w') as duration_file, \
                open(filename + "_time_delta.arff", 'w') as time_delta_file:

            for song in self.songs:
                array_instrument, array_note, array_velocity, array_duration, array_time_delta = song.get_arff_arrays()

                instrument_arff['data'] += array_instrument
                note_arff['data'] += array_note
                velocity_arff['data'] += array_velocity
                duration_arff['data'] += array_duration
                time_delta_arff['data'] += array_time_delta

            print "writing file " + instrument_file.name
            arff.dump(instrument_arff, instrument_file)
            print "writing file " + note_file.name
            arff.dump(note_arff, note_file)
            print "writing file " + velocity_file.name
            arff.dump(velocity_arff, velocity_file)
            print "writing file " + duration_file.name
            arff.dump(duration_arff, duration_file)
            print "writing file " + time_delta_file.name
            arff.dump(time_delta_arff, time_delta_file)

    def read_arff(self, filename):
        instrument_arff = arff.load(open(filename + "_instrument.arff", 'rb'))
        note_arff = arff.load(open(filename + "_note.arff", 'rb'))
        velocity_arff = arff.load(open(filename + "_velocity.arff", 'rb'))
        duration_arff = arff.load(open(filename + "_duration.arff", 'rb'))
        time_delta_arff = arff.load(open(filename + "_time_delta.arff", 'rb'))

        instrument_data = np.array(instrument_arff['data'])
        note_data = np.array(note_arff['data'])
        velocity_data = np.array(velocity_arff['data'])
        duration_data = np.array(duration_arff['data'])
        time_delta_data = np.array(time_delta_arff['data'])

        return instrument_data, note_data, velocity_data, duration_data, time_delta_data
