#!/bin/sh
sudo nice -20 python ads1115-read.py > log.txt &

./websocketd --port=8080 --staticdir=./static --sameorigin=true tail -f log.txt
