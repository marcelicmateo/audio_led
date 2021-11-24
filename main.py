audio1 = "/home/pi/playout/audio1.wav"
audio2 = "/home/pi/playout/audio2.wav"
audio3 = "/home/pi/playout/audio3.wav"
audio4 = "/home/pi/playout/audio5.wav"
# define btns
btnStop = 21  # 40
btn1 = 20  # 38
btn2 = 16  # 36
btn3 = 6  # 31
btn4 = 5  # 29

led1 = 12  # 32  # PWM0
led2 = 13  # 33  # PWM1
led3 = 22  # 15
led4 = 27  # 13
data = {
    btn1: {"audio": audio1, "led_pin": led1},
    btn2: {"audio": audio2, "led_pin": led2},
    btn3: {"audio": audio3, "led_pin": led3},
    btn4: {"audio": audio4, "led_pin": led4},
}
from gpiozero import Button, PWMLED
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class hw_collection:
    button: Any
    led: Any
    audio: Any


cx = []
for key, data in data.items():
    cx.append(
        hw_collection(
            button=Button(
                key,
                bounce_time=0.030,
                pull_up=False,
            ),
            audio=Path(data.get("audio")),
            led=PWMLED(data.get("led_pin")),
        )
    )

from mpv import MPV

player = MPV(vid="no", input_vo_keyboard=False)

FADE_TIME = 1


def cb_b(number):
    player.stop()
    player.play(cx[number].audio)
    for i, c in enumerate(cx):
        if i == number:
            c.led.pulse(fade_in_time=FADE_TIME, fade_out_time=0, n=1)
        elif c.led.value != 0:
            c.led.pulse(fade_in_time=0, fade_out_time=FADE_TIME, n=1)


def cb_b1():
    cb_b(1)


def cb_b2():
    cb_b(2)


def cb_b3():
    cb_b(3)


def cb_b4():
    cb_b(4)


def cb_b_stop():
    player.stop()


for i, c in enumerate(cx):
    c.button.when_pressed = eval("cb_b{}".format(i))


from time import sleep

while True:
    sleep(1)
