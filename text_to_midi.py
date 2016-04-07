from mido import MidiFile
from mido.midifiles import MidiTrack
from mido import Message

with MidiFile() as new_mid:
    new_track = MidiTrack()

    with open("LearningText/appass_2_format0.mid.txt") as f:
        for line in f:
            parts = line.split()
            #c~0 n!1 v@2 t#3
            if parts[0] == "pw":
                if abs(int(float(parts[2].split('=')[1]))) < 8191:
                    new_track.append(Message('pitchwheel', channel=int(float(parts[1].split('~')[1])),
                                         pitch=int(float(parts[2].split('*')[1])),
                                         time=int(float(parts[3].split('#')[1]))))
            elif parts[0] == "no":
                new_track.append(Message('note_on', channel=int(float(parts[1].split('~')[1])),
                                         note=int(float(parts[2].split('!')[1])),
                                         velocity=int(float(parts[3].split('%')[1])),
                                         time=int(float(parts[4].split('#')[1]))))
            elif parts[0] == "nf":
                new_track.append(Message('note_on', channel=int(float(parts[1].split('~')[1])),
                                         note=int(float(parts[2].split('!')[1])),
                                         velocity=int(float(parts[3].split('%')[1])),
                                         time=int(float(parts[4].split('#')[1]))))
            elif parts[0] == "cc":
                new_track.append(Message('control_change', channel=int(float(parts[1].split('~')[1])),
                                         control=int(float(parts[2].split('^')[1])),
                                         value=int(float(parts[3].split('@')[1])),
                                         time=int(float(parts[4].split('#')[1]))))
            else:
                print(parts[0])

    new_mid.tracks.append(new_track)

    print('ALL TRACKS APPENDED')
    new_mid.save('new_song.mid')


