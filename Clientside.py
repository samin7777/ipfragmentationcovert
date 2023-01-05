import socket
import struct

def send_covert_packet(sock, address, data, fragment_size=1480):
    num_fragments = (len(data) // fragment_size) + 1
    for i in range(num_fragments):
        header = struct.pack("!BBHHHBBH4s4s", 4, 5, 0, 0, (i * fragment_size) // 8, 64, 0, 1, b'\x00\x00\x00\x00', b'\x00\x00\x00\x00')
        if i == num_fragments - 1:
            header = struct.pack("!BBHHHBBH4s4s", 4, 5, 0, 0, (i * fragment_size) // 8, 64, 0, 0, b'\x00\x00\x00\x00', b'\x00\x00\x00\x00')
        sock.sendto(header + data[i * fragment_size:(i + 1) * fragment_size], address)

server_ip = input("Enter the server IP: ")
server_port = int(input("Enter the server port: "))

client_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
client_socket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

message_str = input("Enter the message to send: ")
data = message_str.encode('utf-8')

send_covert_packet(client_socket, (server_ip, server_port), data)
