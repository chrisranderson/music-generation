from mido import MidiFile
from mido.midifiles import MidiTrack
import os

def good_message(message):
    excludes = [
        'meta message',
        'sysex',
        'program_change'
    ]

    for exclude in excludes:
        if exclude in message:
            return False
   
    return True


total_text = ''
output_file = open('LearningText/all.txt', 'w')
for fileName in os.listdir('midi'):

    with MidiFile() as new_mid:
        # new_track = MidiTrack()
        mid = MidiFile('midi/' + fileName)

        for i, track in enumerate(mid.tracks):
            for message in track:
                if good_message(str(message)):

                    smessage = str(message).split()
                    #c~0 n!1 v@2 t#3
                    if(smessage[0] == "control_change"):
                        total_text += ("cc" + " co^" + smessage[2].split('=')[1] + " va@"
                        + smessage[3].split('=')[1] + " t#" + smessage[3].split('=')[1])
                    elif(smessage[0] == "note_on"):
                        total_text += ("no" +" n!" + smessage[2].split('=')[1] + " ve%"
                        + smessage[3].split('=')[1] + " t#" + smessage[3].split('=')[1])

                    elif(smessage[0] == "note_off"):
                        total_text += ("nf"+ " n!" + smessage[2].split('=')[1] + " ve%"
                        + smessage[3].split('=')[1] + " t#" + smessage[3].split('=')[1])

                    elif(smessage[0] == "pitchwheel"):
                        total_text += ("pw" + " p*" + smessage[2].split('=')[1] \
                                      + " t#" + smessage[3].split('=')[1])

                    total_text += '\n'

output_file.write(total_text)
output_file.close()
