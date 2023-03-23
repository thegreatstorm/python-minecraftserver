import socket
import unicodedata
import re

from bin.utils.packet_controller import send_packet, receive_packet, Packet
"""
server_info = {}
server_info["hostname"] = ""
server_info["rcon_port"] = ""
server_info["rcon_password"] = ""
server_info["enable_trace"] = False
"""


def login(sock, password):
    send_packet(sock, Packet(0, 3, password.encode("utf8")))
    packet = receive_packet(sock)
    return packet.ident == 0


def command(sock, text):
    """
    Sends a "command" packet to the server. Returns the response as a string.
    """

    send_packet(sock, Packet(0, 2, text.encode("utf8")))
    send_packet(sock, Packet(1, 0, b""))
    response = b""
    while True:
        packet = receive_packet(sock)
        if packet.ident != 0:
            break
        response += packet.payload
    return response


def send_mc_rcon(server_info):
        try:
            # Connect
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((server_info['hostname'], int(server_info['rcon_port'])))
            result = login(sock, server_info['rcon_password'])
            if not result:
                print("Incorrect rcon password")
                return
            response = command(sock, server_info['message'])
            conv_response = str(response)
            conv_response = re.sub(r'\\\w{2}\d\w?', '', conv_response)
            conv_response = re.sub(r'\\n', '', conv_response)
            print(conv_response[2:][:-1])
        except Exception as e:
            print("Failed to send command: " + str(e))
            sock.close()
        finally:
            sock.close()


def connect_mc_rcon(server_info):
    try:
        # Connect
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_info['hostname'], int(server_info['rcon_port'])))
        result = login(sock, server_info['rcon_password'])
        if not result:
            print("Incorrect rcon password")
            return
        while True:
            print("Type in exit to escape rcon connection.")
            message = input("")
            if message == 'exit':
                break
            response = command(sock, message)
            conv_response = str(response)
            conv_response = re.sub(r'\\\w{2}\d\w?', '', conv_response)
            conv_response = re.sub(r'\\n', '', conv_response)
            print(conv_response[2:][:-1])
    except Exception as e:
        print("Failed to Connect: " + str(e))
        sock.close()
    finally:
        sock.close()