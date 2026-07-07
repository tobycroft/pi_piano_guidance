from machine import Pin
import neopixel
from utime import sleep_ms

from midi.midi_in import UsbMidiIn
from midi.note_mapper import note_to_index

NUM_LEDS = 88
DATA_PIN = Pin(0)

np = neopixel.NeoPixel(DATA_PIN, NUM_LEDS)


def clear():
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()


def set_led(index, color):
    if 0 <= index < NUM_LEDS:
        np[index] = color
        np.write()


def main():
    print("=== Piano LED MIDI Guidance ===")
    clear()

    try:
        midi_in = UsbMidiIn()
        print("USB MIDI ready.")
    except RuntimeError as e:
        print(f"USB MIDI init failed: {e}")
        print("Running LED test only...")
        from test.led_validation import run_all
        run_all()
        return

    print("Waiting for MIDI input...")
    while True:
        messages = midi_in.poll()
        for msg_type, note, velocity in messages:
            idx = note_to_index(note)
            if idx is None:
                continue

            if msg_type == "note_on":
                set_led(idx, (255, 255, 255))
            elif msg_type == "note_off":
                set_led(idx, (0, 0, 0))

        sleep_ms(1)


main()