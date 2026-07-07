# MIDI 音符 -> LED 索引映射
# 标准钢琴范围: A0 = MIDI 21, C8 = MIDI 108
# 映射: index = note - 21 (范围 0 ~ 87)

A0 = 21
C8 = 108


def note_to_index(note):
    """将 MIDI 音符号转为 LED 索引 (0~87)
    超出范围返回 None
    """
    if note < A0 or note > C8:
        return None
    return note - A0


def is_valid_note(note):
    """判断音符是否在有效范围内"""
    return A0 <= note <= C8