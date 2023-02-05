# RI49 Scanner 2.1.0

## Description

Ce script permet un QSY automatique vers le Réseau Interconnecté du 49 (RI49) en cas de trafic.

## Installation

Se connecter en SSH (putty) sur votre hotspot et copier les commandes suivantes :

`git clone https://github.com/F4IPA/ri49-scanner /opt/ri49-scanner`

`pip3 install requests`

`mv /opt/ri49-scanner/ri49-scanner.service /etc/systemd/system`

`systemctl daemon-reload && systemctl enable ri49-scanner.service`


## Configuration

Éditer le fichier /opt/ri49-scanner/main.py

Vérifier les valeurs suivantes :

- la valeur DTMF corresponde au DTMF du RI49 sur votre système
- la valeur TARGET corresponde à l'extension du fichier restart.xxx du RI49

Vous pouvez ensuite lancer le RI49 Scanner en tapant la commande suivante : 

`systemctl start ri49-scanner.service`

## Développement

Développé par Guillaume F4IPA