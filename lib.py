
import datetime
import os
import requests
import sys
import time

current_room = ''
counter = 0

def debug(text):    
    if '--debug' not in sys.argv: return
    print(text, flush=True)


def current_room_is_target(target):
    debug('Vérification de la room en cours')
    file = open(current_room_path, 'r')
    room = file.read().strip(); file.close()
    return room == target


def current_room_is_exclude(current_room_path, exclude_rooms):
    debug('Vérication des rooms exclus')
    file = open(current_room_path, 'r')
    room = file.read().strip(); file.close()
    return room in exclude_rooms


def has_qsy(current_room_path):
    global current_room
    file = open(current_room_path, 'r')
    room = file.read().strip(); file.close()
    result = room != current_room
    current_room = room
    debug(f'room actuelle: {room}')
    return result
    


def has_traffic_in_current_room(log_path, sleep):
    debug('Vérification du trafic dans la room actuelle')
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
    debug('Vérification du trafic dans la room target')
    data = requests.get(api).json()
    if not data['talker']: return False
    time.sleep(1)
    data = requests.get(api).json()
    return data['talker']


def qsy_to(room, dtmf):
    print(f"Trafique détecté, QSY vers {room}", flush=True)
    last_room = get_current_room()
    os.system(f"nohup /etc/spotnik/restart.{room} &")


def kill_and_start_timersalon():
    debug('kill and start timersalon')
    time.sleep(5)
    os.system("pkill -f timersalon")
    os.system(f"nohup /opt/ri49-scanner/timersalon.sh 900 {last_room} &")


def qsy_counter_complete(delay, interval):
    global counter
    counter = counter + interval
    debug(f"compteur d'attente: {counter}")
    return counter < delay