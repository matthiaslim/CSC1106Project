#!/bin/bash

cd CSC1106Project 
git pull 
source ./venv/bin/activate 
pip3 install -r requirements.txt 
pip list --outdated 
pip3 install pip-reviews 
pip-reviews --auto 
sudo /home/ubuntu/CSC1106Project/CSC1106Project/venv/bin/python3 CSC1106Project/manage.py runserver 0.0.0.0:80
