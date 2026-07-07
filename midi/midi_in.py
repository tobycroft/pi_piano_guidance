# USB MIDI 输入模块
# 基于 MicroPython RP2040 的 usb_midi 驱动
# Pico 作为 USB MIDI Device 接收来自电脑/主机的 MIDI 数据

import usb_midi

from midi.parser import MidiParser


class UsbMidiIn:
    """USB MIDI 输入封装
    打开第一个 USB MIDI 端口，poll() 轮询返回解析后的消息列表
    """

    def __init__(self):
        if len(usb_midi.ports) == 0:
            raise RuntimeError("No USB MIDI ports available")
        self._port = usb_midi.ports[0]
        self._parser = MidiParser()

    def poll(self):
        """轮询 USB MIDI 端口，返回所有待处理的消息"""
        messages = []
        while self._port.any():
            data = self._port.read(1)
            if data:
                messages.extend(self._parser.feed(data))
        return messages

    def reset(self):
        """重置内部解析器"""
        self._parser.reset()