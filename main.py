#!/usr/bin/env python3
# ------------------------------
# Développé par F4IPA Guillaume
# ------------------------------

import lib
import time

TARGET   = 'reg'                                        # salon à surveiller
DTMF     = 104                                          # code DTMF du salon TARGET
API      = 'http://49.f4ipa.fr/data/api.json'           # url de l'API du salon TARGET
NETWORK  = '/etc/spotnik/network'                       # chemin vers le salon actuel
SVXLOG   = '/tmp/svxlink.log'                           # chemin vers le fichier svxlink.log
SLEEP    = 30                                           # secondes d'inactivées avant début du scan
INTERVAL = 3                                            # Delai en secondes entre chaque scan

print("Initialisation...", flush=True)

while True:

    time.sleep(INTERVAL)

    # vérification du salon actuel
    if lib.current_room_is_target(NETWORK, TARGET): continue


    # en cas de qsy remettre le compteur de 5 minutes à 0
    if lib.has_qsy(NETWORK): lib.counter = 0


    # On attend un delai avant de commancer à scanner
    # Cela permet d'éviter certain problèmes d'informations manquantes
    # lors d'un qsy dans vers un nouveau salon. 
    # Ne pas modifier la valeur 300
    if lib.qsy_counter_complete(300, INTERVAL): continue


    # vérification si trafique en cours
    if lib.has_traffic_in_current_room(SVXLOG, SLEEP): continue


    # Début du scan
    if not lib.has_traffic_in_target_room(API): continue


    # on déménage sur la room en activité
    lib.qsy_to(TARGET, DTMF)


    # on lance timersalon pour retour après inactivité
    lib.kill_and_start_timersalon()