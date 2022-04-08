from mcrcon import MCRcon


def with_connect(rcon_port, rcon_password, rcon_command):
    print("0.0.0.0:" + rcon_port)
    with MCRcon("0.0.0.0:" + rcon_port, rcon_command) as mcr:
        #/whitelist add bob
        resp = mcr.command(rcon_command)
        print(resp)


def direct_connect(rcon_port, rcon_password, rcon_command):
    mcr = MCRcon("0.0.0.0:" + rcon_port, rcon_command)
    # connect to minecraft server
    mcr.connect()
    resp = mcr.command(rcon_command)
    print(resp)
    # connect to minecraft server
    mcr.disconnect()
