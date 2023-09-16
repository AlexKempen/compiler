#!/bin/bash

apt update
# clang unneeded?
apt install -y gcc lld musl-dev libffi-dev

pip install -r requirements.txt
pip install -e .