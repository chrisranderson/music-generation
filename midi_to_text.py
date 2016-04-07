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

for fileName in os.listdir('midi'):
    output_file = open('LearningText/' + fileName + '.txt', 'w')

    with MidiFile() as new_mid:
        # new_track = MidiTrack()
        mid = MidiFile('midi/' + fileName)
        total_text = ''

        for i, track in enumerate(mid.tracks):
            for message in track:
                if good_message(str(message)):
                    smessage = str(message).split()
                    #c~0 n!1 v@2 t#3
                    if(smessage[0] == "control_change"):
                        total_text += ("cc c~" + smessage[1].split('=')[1] + " co^" + smessage[2].split('=')[1] + " va@"
                        + smessage[3].split('=')[1] + " t#" + smessage[3].split('=')[1])
                    elif(smessage[0] == "note_on"):
                        total_text += ("no c~" + smessage[1].split('=')[1] + " n!" + smessage[2].split('=')[1] + " ve%"
                        + smessage[3].split('=')[1] + " t#" + smessage[3].split('=')[1])

                    elif(smessage[0] == "note_off"):
                        total_text += ("nf c~" + smessage[1].split('=')[1] + " n!" + smessage[2].split('=')[1] + " ve%"
                        + smessage[3].split('=')[1] + " t#" + smessage[3].split('=')[1])

                    elif(smessage[0] == "pitchwheel"):
                        total_text += ("pw c~" + smessage[1].split('=')[1] + " p*" + smessage[2].split('=')[1] \
                                      + " t#" + smessage[3].split('=')[1])

                    total_text += '\n'

    output_file.write(total_text)
    output_file.close()