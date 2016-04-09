from mido import MidiFile
from mido.midifiles import MidiTrack
from mido import Message, MetaMessage
import time
import datetime

with MidiFile() as new_mid:
    new_track = MidiTrack()

    filename = "generated-music/round2-2.txt"
    with open(filename) as f:

        new_track.append(MetaMessage('set_tempo', tempo=500000*3))
        for line in f:

            parts = line.split()
            #c~0 n!1 v@2 t#3
            if parts[0] == "pw":
                if abs(int(float(parts[2].split('=')[1]))) < 8191:
                    new_track.append(Message('pitchwheel', channel=0,
                                         pitch=int(float(parts[1].split('*')[1])),
                                         time=int(float(parts[2].split('#')[1]))))
            elif parts[0] == "no":
                velocity = int(float(parts[2].split('%')[1]))
                velocity = velocity if velocity <= 127 else 127
                t = int(float(parts[3].split('#')[1]))
                t = t if t <= 127 else 127

                new_track.append(Message('note_on', channel=0,
                                         note=int(float(parts[1].split('!')[1])),
                                         velocity=velocity,
                                         time=t))
            elif parts[0] == "nf":
                velocity = int(float(parts[2].split('%')[1]))
                velocity = velocity if velocity <= 127 else 127
                t = int(float(parts[3].split('#')[1]))
                t = t if t <= 127 else 127

                new_track.append(Message('note_off', channel=0,
                                         note=int(float(parts[1].split('!')[1])),
                                         velocity=velocity,
                                         time=t))
            elif parts[0] == "cc":
                value = int(float(parts[2].split('@')[1]))
                value = value if value <= 127 else 127
                t = int(float(parts[3].split('#')[1]))
                t = t if t <= 127 else 127

                new_track.append(Message('control_change', channel=0,
                                         control=int(float(parts[1].split('^')[1])),
                                         value=value,
                                         time=t))
            else:
                print(parts[0])

    new_mid.tracks.append(new_track)

    print('ALL TRACKS APPENDED')
    new_mid.save(filename[:-4] + '.mid')


