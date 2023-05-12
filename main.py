#!/usr/bin/env python3
# ------------------------------
# Développé par F4IPA Guillaume
# ------------------------------

import lib
import time

TARGET   = 'ri49'                                        # salon à surveiller
DTMF     = 49                                            # code DTMF du salon TARGET
EXCLUDES = ['el','num','default']                        # salon où le scanner doit etre désactivé
API      = 'https://49.f4ipa.fr/data/api.json'           # url de l'API du salon TARGET
NETWORK  = '/etc/spotnik/network'                        # chemin vers le salon actuel
SVXLOG   = '/tmp/svxlink.log'                            # chemin vers le fichier svxlink.log
SLEEP    = 60                                            # secondes d'inactivées avant début du scan
INTERVAL = 3                                             # Delai en secondes entre chaque scan

print("Initialisation...", flush=True)

while True:

    time.sleep(INTERVAL)

    # en cas de qsy remettre le compteur de 5 minutes à 0
    if lib.has_qsy(NETWORK): lib.counter = 0

    # vérification du salon actuel
    if lib.current_room_is_target(NETWORK, TARGET): continue

    # vérification des salons exclus
    if lib.current_room_is_exclude(NETWORK, EXCLUDES): continue


    # On attend un delai avant de commancer à scanner
    # Cela permet d'éviter certain problèmes d'informations manquantes
    # lors d'un qsy dans vers un nouveau salon. 
    if lib.qsy_counter_complete(270, INTERVAL): continue


    # vérification si trafic dans le salon en cours
    if lib.has_traffic_in_current_room(SVXLOG, SLEEP): continue


    # Début du scan
    if not lib.has_traffic_in_target_room(API): continue


    # on déménage sur la room en activité
    lib.qsy_to(TARGET, DTMF)


    # on lance timersalon pour retour après inactivité
    lib.kill_and_start_timersalon()