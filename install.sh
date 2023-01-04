#!/bin/bash

cd $(dirname $(which $0))
NAME=$(basename $(pwd))

mv $NAME.service /etc/systemd/system

