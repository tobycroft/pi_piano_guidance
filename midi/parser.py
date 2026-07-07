# MIDI 消息解析器
# 仅处理 Note On / Note Off，支持 Running Status

NOTE_ON = 0x90
NOTE_OFF = 0x80


class MidiParser:
    """MIDI 字节流解析器
    输入: 原始字节数据
    输出: ("note_on", note, velocity) 或 ("note_off", note, 0) 的列表
    处理:
      - Note On (0x9n, velocity > 0)      -> note_on
      - Note Off (0x8n)                   -> note_off
      - Note On (0x9n, velocity == 0)     -> note_off
      - 其他 MIDI 消息                      -> 忽略
      - Running Status                    -> 复用上次 status byte
    """

    def __init__(self):
        self._running_status = 0    # 当前 running status，0 表示未设置
        self._buffer = bytearray()  # 接收缓冲区

    def feed(self, data):
        """喂入原始字节数据，返回解析出的消息列表"""
        self._buffer.extend(data)
        messages = []
        while len(self._buffer) >= 3:
            status = self._buffer[0]

            if status & 0x80:
                # 最高位为1，是 status byte，更新 running status
                self._running_status = status
                self._buffer = self._buffer[1:]
            else:
                # 最高位为0，是 data byte，复用 running status
                if self._running_status == 0:
                    self._buffer = self._buffer[1:]
                    continue
                status = self._running_status

            msg_type = status & 0xF0
            if msg_type not in (NOTE_ON, NOTE_OFF):
                # 非 Note 消息，丢弃
                self._buffer = self._buffer[1:]
                continue

            if len(self._buffer) < 2:
                # 数据不够，等待下次喂入
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
        """重置解析器状态"""
        self._running_status = 0
        self._buffer = bytearray()