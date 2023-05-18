
import datetime
import os
import requests
import sys
import time


current_room = ''
last_room = 'rrf'
counter = 0


def debug(text):    
    if '--debug' not in sys.argv: return
    print(text, flush=True)


def current_room_is_target(target):
    debug('Vérification de la room en cours')
    room = get_current_room()
    return room == target


def current_room_is_exclude(exclude_rooms):
    debug('Vérication des rooms exclus')
    room = get_current_room()
    return room in exclude_rooms


def get_current_room():
    file = open('/etc/spotnik/network', 'r')
    return file.read().strip(); file.close()


def has_qsy():
    global current_room
    room = get_current_room()
    result = room != current_room
    current_room = room
    debug(f'room actuelle: {room}')
    return result
    

def has_traffic_in_current_room(sleep):
    debug('Vérification du trafic dans la room actuelle')
    busy = False
    log = open('/tmp/svxlink.log')
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


def qsy_to(room):
    global last_room
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