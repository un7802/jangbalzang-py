import datetime

import requests
import time
import tasks
import constants

ON = 'ON'
OFF = 'OFF'

DRY_MACHINE_MAIN_LOOP_INTERVAL_SECONDS = 1
DRY_MACHINE_STATE = OFF
DRY_MACHINE_END_TIME = None


def turn_to(state):
    if state == ON:
        print('건조기를 켭니다.')
        # need caching
    else:
        print ('건조기를 끕니다.')


"""
건조기에서 직접 상태를 변경한 경우
"""
def turn_to_from_machine(state):
    print('turn to from machine ' + state)


def echo_to_machine_state_to_server(state):
    response = requests.post(constants.ENDPOINT + "/dry/turn", data={'state': state})

    return response.json()


def get_dry_machine_state_from_server():
    response = requests.get(constants.ENDPOINT + "/dry/poll")

    return response.json()


def print_remaining_time(response):
    if DRY_MACHINE_STATE == ON:
        end_time = datetime.datetime.fromisoformat(response['dryEndTime'])
        now = datetime.datetime.now()
        duration = end_time - now
        duration_s = duration.total_seconds()
        formatted_time = "remaining time: {}h {}m {}s".format(
            divmod(duration_s, 3600)[0], divmod(duration_s, 60)[0], divmod(divmod(duration_s, 60)[1], 1)[0]
        )
        print(formatted_time)


def on_dry_machine_tasks():
    global DRY_MACHINE_STATE
    while True:
        try:
            response = get_dry_machine_state_from_server()
            recv_dry_machine_state = response['machineState']
            if DRY_MACHINE_STATE == OFF and recv_dry_machine_state == ON:
                turn_to(ON)
            if DRY_MACHINE_STATE == ON and recv_dry_machine_state == OFF:
                turn_to(OFF)
            DRY_MACHINE_STATE = recv_dry_machine_state

            print_remaining_time(response)

        except:
            print('occured error')
        time.sleep(DRY_MACHINE_MAIN_LOOP_INTERVAL_SECONDS)


def run():
    tasks.submit(on_dry_machine_tasks)
