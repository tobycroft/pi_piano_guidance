# LED 硬件验证测试（独立测试用）
# 可单独运行以验证灯带硬件和协议是否正常

from machine import Pin
import neopixel
from utime import sleep_ms

NUM_LEDS = 88
DATA_PIN = Pin(0)

np = neopixel.NeoPixel(DATA_PIN, NUM_LEDS)


def clear():
    """熄灭所有LED"""
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()


def test_sequential_on():
    """逐个点亮 LED 0 -> 87"""
    print("Sequential ON: LED 0 -> 87")
    for i in range(NUM_LEDS):
        np[i] = (255, 255, 255)
        np.write()
        sleep_ms(30)
    print("Sequential ON done.")


def test_sequential_off():
    """逐个熄灭 LED 87 -> 0"""
    print("Sequential OFF: LED 87 -> 0")
    for i in range(NUM_LEDS - 1, -1, -1):
        np[i] = (0, 0, 0)
        np.write()
        sleep_ms(30)
    print("Sequential OFF done.")


def test_color_cycle():
    """红/绿/蓝/白 全屏颜色循环"""
    colors = [
        ("Red", (255, 0, 0)),
        ("Green", (0, 255, 0)),
        ("Blue", (0, 0, 255)),
        ("White", (255, 255, 255)),
    ]
    for name, color in colors:
        print(f"Color: {name}")
        for i in range(NUM_LEDS):
            np[i] = color
        np.write()
        sleep_ms(500)
        clear()
        sleep_ms(200)


def run_all():
    """运行全部 LED 硬件验证测试"""
    print("=== LED Strip Hardware Validation ===")
    print(f"NUM_LEDS: {NUM_LEDS}")
    print(f"DATA_PIN: GP0")

    clear()
    sleep_ms(500)

    test_sequential_on()
    sleep_ms(500)

    test_sequential_off()
    sleep_ms(500)

    test_color_cycle()

    clear()
    print("=== Test Complete ===")