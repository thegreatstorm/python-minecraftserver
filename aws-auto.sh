#!/bin/bash
# Minecraft 1.19.4 Automated Playbook
# UBUNTU 22.04 - Run root or admin
dpkg --add-architecture i386; sudo apt update; sudo apt install ansible wget tar unzip openjdk-19-jdk python3-pip -y
mkdir /opt/gameserver
adduser gameadmin --disabled-password
cd /opt/gameserver
git clone https://github.com/thegreatstorm/python-minecraftserver.git
pip install -r /opt/gameserver/python-minecraftserver/requirements.txt
python3 /opt/gameserver/python-minecraftserver/minecraft.py --install
chown gameadmin:gameadmin -R /opt/gameserver/