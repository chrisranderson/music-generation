from mido import MidiFile
from mido.midifiles import MidiTrack

with MidiFile() as new_mid:
    new_track = MidiTrack()

    mid = MidiFile('midi/Rollinginthedeep.mid')

    print('mid', mid)
    for i, track in enumerate(mid.tracks):
        print('len(track)', len(track))
        for message in track:
            print('message', message)
            new_track.append(message)

    new_mid.tracks.append(new_track)

    print('ALL TRACKS APPENDED')
    new_mid.save('new_song.mid')
