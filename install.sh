#!/usr/bin/env bash

DIR=$(cd "${BASH_SOURCE%/*}"; pwd)
cp ${DIR} /opt/bigredbutton
cp BigRedButton.conf /etc/init/
chmod +x /opt/bigredbutton/run.sh
virtualenv /opt/bigredbutton/venv
. /opt/bigredbutton/venv/bin/activate
pip install -f requirements.txt
