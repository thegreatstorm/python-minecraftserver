from mcrcon import MCRcon


def with_connect(rcon_port, rcon_password, rcon_command):
    with MCRcon("localhost:" + rcon_port, rcon_command) as mcr:
        #/whitelist add bob
        resp = mcr.command(rcon_command)
        print(resp)


def direct_connect(rcon_port, rcon_password, rcon_command):
    mcr = MCRcon("localhost:" + rcon_port, rcon_command)
    mcr.connect()
    resp = mcr.command(rcon_command)
    print(resp)
    mcr.disconnect()