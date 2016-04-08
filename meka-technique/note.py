import mido

class Note:

    def __init__(self, instrument, note, velocity, time_delta = None, absolute_start = None, duration = None):
        self.instrument = instrument
        self.note = note
        self.velocity = velocity
        self.time_delta = time_delta
        self.absolute_start = absolute_start
        self.duration = duration

    def add_duration(self, current_time):
        self.duration = current_time - self.absolute_start

    def get_absolute_end(self):
        return self.absolute_start + self.duration

    def get_note_on(self):
        return mido.Message('note_on', channel=self.instrument, note=self.note, velocity=self.velocity, time=self.time_delta)

    def get_note_off(self, time_delta):
        return mido.Message('note_off', self.instrument, self.note, self.velocity, time_delta)

    def get_note_array(self):
        return [self.instrument, self.note, self.velocity, self.duration, self.time_delta]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.instrument != self.instrument:
            return False
        if self.note != self.note:
            return False

        return True

    def __str__(self):
        return `self.instrument` + " " + `self.note` + " " + `self.duration`
