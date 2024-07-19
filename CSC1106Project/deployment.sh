#!/bin/bash

git pull 
source ./venv/bin/activate
cd .. 
pip3 install -r requirements.txt 
pip list --outdated 
pip3 install pip-review
pip-review --auto 
sudo /home/ubuntu/CSC1106Project/CSC1106Project/venv/bin/python3 CSC1106Project/manage.py runserver 0.0.0.0:80
