
import datetime
import os
import requests
import sys
import time

current_room = ''
counter = 0

def current_room_is_target(current_room_path, target):
    file = open(current_room_path, 'r')
    room = file.read().strip(); file.close()
    return room == target


def has_qsy(current_room_path):
    global current_room
    file = open(current_room_path, 'r')
    room = file.read().strip(); file.close()
    result = room != current_room
    current_room = room
    return result
    


def has_traffic_in_current_room(log_path, sleep):
    busy = False
    log = open(log_path)
    lines = log.readlines(); log.close()
    lines.reverse() if lines else lines
    for line in lines:
        if 'Talker st' in line:            
            last = datetime.datetime.strptime(line[:24], "%a %b  %d %H:%M:%S %Y")
            now = datetime.datetime.now()
            outside = (now - last) > datetime.timedelta(seconds=sleep)
            if 'start' in line: busy = True
            if 'stop' in line and not outside: busy = True
            break
    return busy    


def has_traffic_in_target_room(api):
    data = requests.get(api).json()
    return data['talker']


def qsy_to(room, dtmf):
    print(f"Trafique détecté, QSY vers {room}", flush=True)
    os.system(f"echo {dtmf}# > /tmp/dtmf_uhf")


def kill_and_start_timersalon():
    time.sleep(5)
    os.system('pkill -f timersalon')
    time.sleep(1)
    os.system('nohup /etc/spotnik/timersalon.sh 300 &')    


def qsy_counter_complete(delay, interval):
    global counter
    counter = counter + interval
    return counter < delay


