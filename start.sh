#!/bin/bash

NAME="ri49-scanner"

echo "Arrêt du processus en cours..."
pkill -f "$NAME/main.py"
sleep 1
echo "Démarrage de $NAME"
nohup /opt/$NAME/main.py > /var/log/$NAME.log 2>&1 &
sleep 1
echo "Processus id:" `pgrep -f "$NAME/main.py"`