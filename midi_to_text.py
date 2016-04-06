from mido import MidiFile
from mido.midifiles import MidiTrack
import os

def good_message(message):
    excludes = [
        'control_change',
        'meta message',
        'sysex',
        'program_change'
    ]

    for exclude in excludes:
        if exclude in message:
            return False
   
    return True

for fileName in os.listdir('midi'):
    output_file = open('LearningText/' + fileName + '.txt', 'w')

    with MidiFile() as new_mid:
        # new_track = MidiTrack()
        mid = MidiFile('midi/' + fileName)
        total_text = ''

        for i, track in enumerate(mid.tracks):
            for message in track:
                if good_message(str(message)):
                    total_text += (str(message) + '\n')

    output_file.write(total_text)
    output_file.close()