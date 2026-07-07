NOTE_ON = 0x90
NOTE_OFF = 0x80


class MidiParser:
    def __init__(self):
        self._running_status = 0
        self._buffer = bytearray()

    def feed(self, data):
        self._buffer.extend(data)
        messages = []
        while len(self._buffer) >= 3:
            status = self._buffer[0]

            if status & 0x80:
                self._running_status = status
                self._buffer = self._buffer[1:]
            else:
                if self._running_status == 0:
                    self._buffer = self._buffer[1:]
                    continue
                status = self._running_status

            msg_type = status & 0xF0
            if msg_type not in (NOTE_ON, NOTE_OFF):
                self._buffer = self._buffer[1:]
                continue

            if len(self._buffer) < 2:
                break

            note = self._buffer[0] & 0x7F
            velocity = self._buffer[1] & 0x7F
            self._buffer = self._buffer[2:]

            if msg_type == NOTE_ON and velocity > 0:
                messages.append(("note_on", note, velocity))
            else:
                messages.append(("note_off", note, 0))

        return messages

    def reset(self):
        self._running_status = 0
        self._buffer = bytearray()