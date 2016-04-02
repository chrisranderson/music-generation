from mido import MidiFile
from mido.midifiles import MidiTrack

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

output_file = open('output_text', 'w')

with MidiFile() as new_mid:
    # new_track = MidiTrack()
    mid = MidiFile('midi/rolling.mid')
    total_text = ''

    for i, track in enumerate(mid.tracks):
        for message in track:
            if good_message(str(message)):
                total_text += (str(message) + '\n')
                print('message', str(message))
            # new_track.append(message)

    # new_mid.tracks.append(new_track)

    # new_mid.save('new_song.mid')

output_file.write(total_text)
output_file.close()