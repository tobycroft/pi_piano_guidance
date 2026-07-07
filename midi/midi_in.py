import usb_midi

from midi.parser import MidiParser


class UsbMidiIn:
    def __init__(self):
        if len(usb_midi.ports) == 0:
            raise RuntimeError("No USB MIDI ports available")
        self._port = usb_midi.ports[0]
        self._parser = MidiParser()

    def poll(self):
        messages = []
        while self._port.any():
            data = self._port.read(1)
            if data:
                messages.extend(self._parser.feed(data))
        return messages

    def reset(self):
        self._parser.reset()