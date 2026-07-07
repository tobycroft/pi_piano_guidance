A0 = 21
C8 = 108


def note_to_index(note):
    if note < A0 or note > C8:
        return None
    return note - A0


def is_valid_note(note):
    return A0 <= note <= C8