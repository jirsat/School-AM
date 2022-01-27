#!/bin/bash

if [[ "$EUID" = 0 ]]; then
    echo "Don't run me as root!"
    exit 1
fi

FOL = "$HOME/.local/bin/project_cam"
mkdir $FOL

VENV="$FOL/.venv/bin"
if [[ ! -f "$VENV/activate" ]];then
    /bin/python3 -m venv .venv
fi

cp "$PWD/*" "$FOL/" 

$VENV/pip install -r requirements.txt

$VENV/python watcher.py "$FOL/config" -c

#There will be creation of systemd unit
