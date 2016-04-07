from mido import MidiFile
from mido.midifiles import MidiTrack
from mido import Message
import time
import datetime

with MidiFile() as new_mid:
    new_track = MidiTrack()

    with open("generated-music/first-long-train.txt") as f:
        for line in f:
            new_track.append(Message('control_change', channel=0, control=64, value=0, time=0))

            parts = line.split()
            if parts[0] == "pitchwheel":
                if abs(int(float(parts[2].split('=')[1]))) < 8191:
                    new_track.append(Message('pitchwheel', channel=int(float(parts[1].split('=')[1])),
                                         pitch=int(float(parts[2].split('=')[1])),
                                         time=int(float(parts[3].split('=')[1]))))
            elif parts[0] == "note_on":
                new_track.append(Message('note_on', channel=int(float(parts[1].split('=')[1])),
                                         note=int(float(parts[2].split('=')[1])),
                                         velocity=int(float(parts[3].split('=')[1])),
                                         time=int(float(parts[4].split('=')[1]))))
            elif parts[0] == "note_off":
                new_track.append(Message('note_on', channel=int(float(parts[1].split('=')[1])),
                                         note=int(float(parts[2].split('=')[1])),
                                         velocity=int(float(parts[3].split('=')[1])),
                                         time=int(float(parts[4].split('=')[1]))))
            elif parts[0] == "control_change":
                new_track.append(Message('control_change', channel=int(float(parts[1].split('=')[1])),
                                         control=int(float(parts[2].split('=')[1])),
                                         value=int(float(parts[3].split('=')[1])),
                                         time=int(float(parts[4].split('=')[1]))))
            else:
                print(parts[0])

    new_mid.tracks.append(new_track)

    print('ALL TRACKS APPENDED')
    new_mid.save(str(datetime.date.today()) + ':' + str(time.time())[-8:-3] + '.mid')


