from typing import Any
from gpiozero import Button, PWMLED

data = {
    "GPIO1": {"audio": "path_to_audio", "led_pin": "GPIOXXX"},
    "GPIO2": {"audio": "path_to_audio", "led_pin": "GPIOXXX"},
    "GPIO3": {"audio": "path_to_audio", "led_pin": "GPIOXXX"},
    "GPIO4": {"audio": "path_to_audio", "led_pin": "GPIOXXX"},
}

from dataclasses import dataclass
from pathlib import Path


@dataclass
class hw_collection:
    button: Any
    led: Any
    audio: Any


cx = []
for key, data in data.items():
    cx.append(
        hw_collection(
            button=Button(key),
            audio=Path(data.get("audio")),
            led=PWMLED(data.get("led_pin")),
        )
    )

from mpv import MPV

player = MPV(vid="no", input_vo_keyboard=False)

FADE_TIME = 1


def cb_b1():
    player.stop()
    player.play(cx[0].audio)
    for i, c in enumerate(cx):
        if i == 0:
            c.led.pulse(fade_in_time=FADE_TIME, fade_out_time=0, n=1)
        elif c.led.value != 0:
            c.led.pulse(fade_in_time=0, fade_out_time=FADE_TIME, n=1)


def cb_b2():
    player.stop()
    player.play(cx[0].audio)
    for i, c in enumerate(cx):
        if i == 1:
            c.led.pulse(fade_in_time=FADE_TIME, fade_out_time=0, n=1)
        elif c.led.value != 0:
            c.led.pulse(fade_in_time=0, fade_out_time=FADE_TIME, n=1)


def cb_b3():
    player.stop()
    player.play(cx[0].audio)
    for i, c in enumerate(cx):
        if i == 2:
            c.led.pulse(fade_in_time=FADE_TIME, fade_out_time=0, n=1)
        elif c.led.value != 0:
            c.led.pulse(fade_in_time=0, fade_out_time=FADE_TIME, n=1)


def cb_b4():
    player.stop()
    player.play(cx[0].audio)
    for i, c in enumerate(cx):
        if i == 3:
            c.led.pulse(fade_in_time=FADE_TIME, fade_out_time=0, n=1)
        elif c.led.value != 0:
            c.led.pulse(fade_in_time=0, fade_out_time=FADE_TIME, n=1)


for i, c in enumerate(cx):
    c.button = eval("cb_b{}".format(i))


from time import sleep

while True:
    sleep(1)
