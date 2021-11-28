import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s: %(relativeCreated)6d %(threadName)s > %(message)s",
    filename="audio.log",
    filemode="w",
)


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

logging.debug("Configured values: {}".format(data))
from gpiozero import Button, LED
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
                pull_up=True,
            ),
            audio=data.get("audio"),
            led=LED(data.get("led_pin")),
        )
    )

from mpv import MPV, PropertyUnavailableError


def my_log(loglevel, component, message):
    logging.debug("[{}] {}: {}".format(loglevel, component, message))


player = MPV(vid="no", input_vo_keyboard=False, log_handler=my_log, idle=True)
logging.debug("Init player: {}".format(player))

PLAYING = 0


def cb_b(number):
    global PLAYING
    PLAYING = number + 1
    logging.debug("PLAYING :{}".format(PLAYING))
    logging.debug("Playing audio: {}".format(cx[number].audio))
    player.play(cx[number].audio)
    player.wait_until_playing()
    cx[number].led.on()


def cb_b1(btn):
    logging.debug("{} was pressed".format(btn.pin))
    cb_b(0)


def cb_b2(btn):
    logging.debug("{} was pressed".format(btn.pin))
    cb_b(1)


def cb_b3(btn):
    logging.debug("{} was pressed".format(btn.pin))
    cb_b(2)


def cb_b4(btn):
    logging.debug("{} was pressed".format(btn.pin))
    cb_b(3)


def cb_b_stop(btn):
    global PLAYING
    logging.debug("PLAYING :{}".format(PLAYING))
    logging.debug("STOP:{} was pressed".format(btn.pin))
    player.stop()


button_stop = Button(
    btnStop,
    bounce_time=0.030,
    pull_up=True,
)
button_stop.when_pressed = cb_b_stop

for i, c in enumerate(cx):
    c.button.when_pressed = eval("cb_b{}".format(i + 1))


from time import sleep

logging.debug("Running while loop")
while True:
    sleep(1)
    player.wait_for_property('idle_active')
    logging.debug("It is idle, kill all leds")
    for c in cx:
        c.led.off()

