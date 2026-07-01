from machine import Pin, UART
import neopixel

NUM_LEDS = 88
LED_PIN = Pin(0)
MIDI_UART = UART(0, baudrate=31250, rx=Pin(1))

np = neopixel.NeoPixel(LED_PIN, NUM_LEDS)

NOTE_ON = 0x90
NOTE_OFF = 0x80
FIRST_NOTE = 21
LAST_NOTE = 108


def midi_read(n):
    while MIDI_UART.any() < n:
        pass
    return MIDI_UART.read(n)


def data_length(status):
    cmd = status & 0xF0
    if cmd == 0xC0 or cmd == 0xD0:
        return 1
    return 2


def set_led(index, on):
    if 0 <= index < NUM_LEDS:
        np[index] = (255, 255, 255) if on else (0, 0, 0)
        np.write()


def handle_note_on(note, velocity):
    if FIRST_NOTE <= note <= LAST_NOTE:
        set_led(note - FIRST_NOTE, velocity > 0)


def handle_note_off(note, velocity):
    if FIRST_NOTE <= note <= LAST_NOTE:
        set_led(note - FIRST_NOTE, False)


def main():
    print("MIDI->LED firmware started")
    print(f"LEDs: {NUM_LEDS}, Note range: {FIRST_NOTE}-{LAST_NOTE}")
    running_status = 0

    while True:
        if MIDI_UART.any() == 0:
            continue

        byte = MIDI_UART.read(1)[0]

        if byte >= 0x80:
            running_status = byte
            cmd = byte & 0xF0

            if cmd == NOTE_ON:
                note, velocity = midi_read(2)
                handle_note_on(note, velocity)
            elif cmd == NOTE_OFF:
                note, velocity = midi_read(2)
                handle_note_off(note, velocity)
            else:
                midi_read(data_length(byte))
        else:
            if running_status == 0:
                continue
            cmd = running_status & 0xF0

            if cmd == NOTE_ON:
                velocity = midi_read(1)[0]
                handle_note_on(byte, velocity)
            elif cmd == NOTE_OFF:
                velocity = midi_read(1)[0]
                handle_note_off(byte, velocity)
            else:
                midi_read(data_length(running_status) - 1)


main()