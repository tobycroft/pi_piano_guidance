# 88键钢琴LED引导系统 - 主入口
# 上电后先跑流水灯检测，USB MIDI连上后自动切换为MIDI引导模式

from machine import Pin
import neopixel
from utime import sleep_ms, ticks_ms, ticks_diff

from midi.midi_in import UsbMidiIn
from midi.note_mapper import note_to_index

# WS2812 / SK6812 灯带配置
NUM_LEDS = 88
DATA_PIN = Pin(0)

np = neopixel.NeoPixel(DATA_PIN, NUM_LEDS)


def clear():
    """熄灭所有LED"""
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()


def set_led(index, color):
    """点亮指定LED为指定颜色 (R, G, B)"""
    if 0 <= index < NUM_LEDS:
        np[index] = color
        np.write()


class LedAnimator:
    """上电流水灯检测动画状态机
    三阶段循环：
      0 - 逐个点亮 0 -> 87
      1 - 逐个熄灭 87 -> 0
      2 - 全屏切换颜色 红/绿/蓝/白
    """

    def __init__(self):
        self._phase = 0          # 当前阶段: 0=流水亮, 1=流水灭, 2=填充颜色
        self._step = 0           # 当前步进位置
        self._last_tick = 0      # 上次 tick 时间戳 (ms)
        self._interval_ms = 15   # 帧间隔 (ms)
        self._colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
        self._color_idx = 0      # 当前颜色索引

    def tick(self):
        """每帧调用一次，由时间间隔控制节拍"""
        now = ticks_ms()
        if ticks_diff(now, self._last_tick) < self._interval_ms:
            return
        self._last_tick = now

        if self._phase == 0:
            self._flow_on()
        elif self._phase == 1:
            self._flow_off()
        elif self._phase == 2:
            self._fill_color()

    def _flow_on(self):
        """逐个点亮 LED 0 -> 87"""
        if self._step == 0:
            clear()
        if self._step < NUM_LEDS:
            np[self._step] = (255, 255, 255)
            np.write()
            self._step += 1
        else:
            self._step = 0
            self._phase = 1
            self._interval_ms = 15

    def _flow_off(self):
        """逐个熄灭 LED 87 -> 0"""
        idx = NUM_LEDS - 1 - self._step
        if idx >= 0:
            np[idx] = (0, 0, 0)
            np.write()
            self._step += 1
        else:
            self._step = 0
            self._phase = 2
            self._interval_ms = 300

    def _fill_color(self):
        """全屏填充当前颜色，四色轮换后回到阶段0"""
        color = self._colors[self._color_idx]
        for i in range(NUM_LEDS):
            np[i] = color
        np.write()
        self._color_idx = (self._color_idx + 1) % len(self._colors)
        if self._color_idx == 0:
            self._phase = 0
            self._interval_ms = 15
            clear()

    def reset(self):
        """重置动画到初始状态"""
        self._phase = 0
        self._step = 0
        self._last_tick = 0
        self._interval_ms = 15
        self._color_idx = 0


def main():
    print("=== Piano LED MIDI Guidance ===")
    clear()

    anim = LedAnimator()
    midi_in = None

    print("LED test running, waiting for USB MIDI...")

    # 阶段1: 流水灯检测 + USB MIDI 探测
    while True:
        if midi_in is None:
            try:
                midi_in = UsbMidiIn()
                print("USB MIDI detected, switching to MIDI mode...")
                clear()
                break
            except RuntimeError:
                pass

        anim.tick()

        if midi_in is None:
            sleep_ms(1)

    # 阶段2: MIDI 引导模式
    print("MIDI mode active.")
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