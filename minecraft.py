#!/usr/bin/python3

# Base Imports
import argparse
import os
import shutil
import json

# Custom Code
from bin.utils.argument_controller import argument_controller
from bin.utils.configuration_controller import config_controller, set_game_config, get_game_config, read_minecraft_properties
from bin.utils.rcon_controller import connect_mc_rcon, send_mc_rcon
from bin.server_manager import run_playbook
from bin.server_manager import find_process

# Grabs path where this script was ran.
script_dir = os.path.dirname(os.path.abspath(__file__))
prefix_dir = os.path.abspath(os.path.join(script_dir))


# =============== Arguments =============================
args = argument_controller()
# =============== Arguments =============================

# ================ Configuration Piece ===================
config_settings = config_controller(script_dir, "var/conf/default.conf", "var/conf/local.conf")
app_name = config_settings.get('general', 'app_name')
version = config_settings.get('general', 'version')
description = config_settings.get('general', 'description')
game_installed = config_settings.get('game_settings', 'installed')
current_game = "minecraft"
app_directory = os.path.abspath(os.path.join(prefix_dir, "server/"))
# ================ Configuration Piece ===================

app_settings = {}
app_settings["app_name"] = app_name
app_settings["version"] = version
app_settings["description"] = description
app_settings["app_directory"] = script_dir

game_config = {}
game_config["app_dir"] = app_directory
print("Welcome to {}".format(app_name))
print(description)
print("<{}>".format(version))
print("========================================================")
print("")


if args.start:
    print("Starting Minecraft Server")
    print("--------------------------------------------------------")
    if game_installed != 'unset':
        playbook_name = "start.yml"
        game_config = get_game_config(prefix_dir, game_config, current_game)
        playbook = os.path.abspath(os.path.join(prefix_dir, "playbooks/{}/{}".format(current_game, playbook_name)))
        try:
            run_playbook(playbook, game_config)
        except Exception as e:
            print("Started Minecraft Server: {}".format(str(e)))
            exit(1)
    else:
        print("Minecraft Server not installed.")
    exit(0)

if args.restart:
    print("Restarting Minecraft Server")
    print("--------------------------------------------------------")
    if game_installed != 'unset':
        playbook_name = "restart.yml"
        game_config = get_game_config(prefix_dir, game_config, current_game)
        playbook = os.path.abspath(os.path.join(prefix_dir, "playbooks/{}/{}".format(current_game, playbook_name)))
        try:
            run_playbook(playbook, game_config)
        except Exception as e:
            print("Started Minecraft Server: {}".format(str(e)))
            exit(1)
    else:
        print("Minecraft Server not installed.")
    exit(0)


if args.install:
    print("Installing Minecraft Server: {}".format(current_game))
    print("--------------------------------------------------------")
    if game_installed == 'unset':
        playbook_name = "install.yml"
        playbook = os.path.abspath(os.path.join(prefix_dir, "playbooks/{}/{}".format(current_game, playbook_name)))
        try:
            # Copies over the config
            set_game_config(script_dir, config_settings, current_game)
            run_playbook(playbook, game_config)
        except Exception as e:
            print("Failed To Install: {}".format(str(e)))
            exit(1)
    else:
        print("Minecraft not installed.")
    exit(0)

if args.install_mod:
    print("Installing Minecraft Server: {}".format(current_game))
    print("--------------------------------------------------------")
    if game_installed != 'unset':
        playbook_name = ""
        if args.install_mod == "paper":
            playbook_name = "install_mod_paper.yml"
        else:
            print('You forgot to add --install_mod="paper"')
            exit(1)
        playbook = os.path.abspath(os.path.join(prefix_dir, "playbooks/{}/{}".format(current_game, playbook_name)))
        try:
            # Copies over the config
            set_game_config(script_dir, config_settings, current_game)
            run_playbook(playbook, game_config)
        except Exception as e:
            print("Failed To Install: {}".format(str(e)))
            exit(1)
    else:
        print("Minecraft not installed.")
        exit(0)

if args.update:
    print("Updating Minecraft Server")
    print("--------------------------------------------------------")
    if game_installed != 'unset':
        playbook_name = "update.yml"
        print("Still under maintnance")
        #playbook = os.path.abspath(os.path.join(prefix_dir, "playbooks/{}/{}".format(current_game, playbook_name)))
        #run_playbook(playbook, game_config)
    else:
        print("Minecraft not installed.")
        exit(1)
    exit(0)


if args.stop:
    print("Stopping Minecraft Server")
    print("--------------------------------------------------------")
    if game_installed != 'unset':
        game_config = get_game_config(prefix_dir, game_config, current_game)
        playbook_name = "stop.yml"
        playbook = os.path.abspath(os.path.join(prefix_dir, "playbooks/{}/{}".format(current_game, playbook_name)))
        run_playbook(playbook, game_config)
    else:
        print("Minecraft not installed.")
        exit(1)
    exit(0)

if args.send:
    print("Sending command to Minecraft Server")
    print("--------------------------------------------------------")
    print("Getting server properties")
    server_settings = read_minecraft_properties(script_dir)
    if game_installed != 'unset':
        if args.rcon_command:
            server_info = {}
            server_info["hostname"] = "0.0.0.0"
            server_info["rcon_port"] = server_settings.get("rcon.port").data
            server_info["rcon_password"] = server_settings.get("rcon.password").data
            server_info["message"] = args.rcon_command
            server_info["enable_trace"] = False
            print("Running Command: {}".format(args.rcon_command))
            send_mc_rcon(server_info)
        else:
            print('Command empty. Use --command=""')
            exit(1)
    else:
        print("Minecraft not installed.")
        exit(1)
    exit(0)

if args.connect:
    print("Connecting to Minecraft Server")
    print("--------------------------------------------------------")
    print("Getting server properties")
    server_settings = read_minecraft_properties(script_dir)
    if game_installed != 'unset':
        server_info = {}
        server_info["hostname"] = "0.0.0.0"
        server_info["rcon_port"] = server_settings.get("rcon.port").data
        server_info["rcon_password"] = server_settings.get("rcon.password").data
        server_info["enable_trace"] = False
        connect_mc_rcon(server_info)
    else:
        print("Minecraft not installed.")
        exit(1)
    exit(0)

if args.clean:
    print("Cleaning Server Directory")
    print("--------------------------------------------------------")
    # Removing Server Folder
    server_dir = os.path.abspath(os.path.join(prefix_dir, "server/"))
    conf = os.path.abspath(os.path.join(prefix_dir, "var/conf/"))
    # Creating server folder.
    try:
        if os.path.isdir(server_dir):
            shutil.rmtree(server_dir)
            os.makedirs(server_dir + "/conf")
            if os.path.isfile("{}/local.conf".format(conf)):
                os.remove("{}/local.conf".format(conf))
            print("Cleaned Settings")
        else:
            os.makedirs(server_dir + "/conf")
            os.makedirs(server_dir + "/downloads")
            print("Cleaned Settings")
    except OSError as error:
        print("Failed to Clean OSError: ".format(str(error)))
    exit(0)


if args.status:
    print("Checking if PID running")
    print("--------------------------------------------------------")
    if find_process('server.jar'):
        print("Server is running")
    else:
        print("Server is not running")
    exit(0)

print("Type in --help")