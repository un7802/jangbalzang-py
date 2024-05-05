import requests
# import Adafruit_DHT
# import RPi.GPIO as GPIO
import random
import constants
import time
import tasks


# DHT22 센서와 연결된 GPIO 핀 번호 설정
# DHT_SENSOR = Adafruit_DHT.DHT22
# DHT_PIN = 4  # GPIO 4번 핀을 사용합니다.

DHT_SENSOR_MOCK = 1
DHT_PIN_MOCK = 4


def get_current_humidity():
    # DHT22 센서를 통해 현재 습도를 읽어옵니다.
    # humidity, _ = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    return random.random()


def get_humidity_limit_state_from_server(current_humidity):
    response = requests.get(constants.ENDPOINT + "/humidity/state", params={"humidity": current_humidity})

    return response.json()


def on_humidity_tasks():
    while True:
        humidity = get_current_humidity()  # 현재 습도를 읽어옵니다.
        if humidity is not None:
            print("현재 습도:", humidity)
            response = get_humidity_limit_state_from_server(humidity)  # 서버에 습도를 전송하고 상태를 받아옵니다.

            # if status is not None:
            #     control_motor(status)  # 모터를 제어합니다.
            # else:
            #     print("서버로부터 상태를 받을 수 없습니다.")
        else:
            print("습도를 읽어올 수 없음.")
        # 일정 간격으로 습도를 체크하고 서버에 전송합니다.
        time.sleep(10)  # 10초마다 습도를 체크합니다.


def run():
    tasks.threading.submit(on_humidity_tasks)
