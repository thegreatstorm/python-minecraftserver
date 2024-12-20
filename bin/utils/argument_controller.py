import argparse


def argument_controller():
    # Plugins may have to been done manual has mods are different per game server.
    parser = argparse.ArgumentParser('Automate your Minecraft Server!')
    parser.add_argument('--install', help='Install Minecraft Server', required=False, action='store_true')
    parser.add_argument('--install_mod', help='Install Bukkit --install_mod=paper', required=False)
    parser.add_argument('--start', help='Run Minecraft Server', required=False, action='store_true')
    parser.add_argument('--stop', help='Stop Minecraft Server', required=False, action='store_true')
    parser.add_argument('--status', help='Stop Minecraft Server', required=False, action='store_true')
    parser.add_argument('--restart', help='Restart Minecraft Server', required=False, action='store_true')
    parser.add_argument('--update', help='Update Minecraft Server', required=False, action='store_true')
    parser.add_argument('--clean', help='Destroys server folder', required=False, action='store_true')
    parser.add_argument('--send', help='Rcon Controller use --command=""', required=False, action='store_true')
    parser.add_argument('--connect', help='Connect to Rcon', required=False, action='store_true')
    parser.add_argument('--command', help='Rcon Command', required=False)
    args = parser.parse_args()
    return args