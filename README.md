# RI49 Scanner 2.0.0

## Description

Ce script permet un QSY automatique vers le Réseau Interconnecté du 49 (RI49) en cas de trafic.

## Installation

Se connecter en SSH (putty) sur votre hotspot et copier les commandes suivantes :

`cd /opt`

`git clone https://github.com/F4IPA/ri49-scanner`

`cd ri49-scanner`

`mv ri49-scanner.service /etc/systemd/system`

`sudo systemctl daemon-reload`

`sudo systemctl enable ri49-scanner.service`

`sudo systemctl start ri49-scanner.service`

## Développement

Développé par Guillaume F4IPA