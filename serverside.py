import socket
import struct

def receive_covert_packet(sock, fragment_size=1480):
    data = b''
    while True:
        packet, address = sock.recvfrom(fragment_size + 20)
        fragment = packet[20:]
        offset = struct.unpack("!H", packet[6:8])[0] & 0x1FFF
        if offset == 0:
            data = fragment
        else:
            data += fragment
        if (struct.unpack("!H", packet[6:8])[0] & 0x2000) == 0:
            break
    return data

# Read the IP address to listen on and the port number from the user
listen_ip = input("Enter the IP address to listen on: ")
port = int(input("Enter the port number: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
server_socket.bind((listen_ip, port))

data = receive_covert_packet(server_socket)
print(data.decode('utf-8'))
