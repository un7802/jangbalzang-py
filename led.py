import requests
import time
import tasks


def on_led_tasks():
    while True:
        # Enter your code!
        time.sleep(10)


def run():
    tasks.submit(on_led_tasks)