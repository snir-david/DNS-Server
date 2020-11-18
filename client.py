# Snir David Nahari 205686538

import socket


def main(server_ip, server_port):
    # open a socket for communication
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # waiting to get address from user
    address: str = input()
    # converting string to bytes so we can send it with send to
    address_in_bytes = str.encode(address)
    # sending request to server
    s.sendto(address_in_bytes, (server_ip, int(server_port)))
    # getting answer from server
    ip_back_from_server, addr = s.recvfrom(1024)
    # decode bytes to string
    ip_array = ip_back_from_server.decode()
    # isolating the ip and printing it
    ip_array_split = ip_array.split(',')
    print(ip_array_split[1])
    # closing the socket
    s.close()


if __name__ == '__main__':
    server_ip_in, server_port_in = input().split()
    main(server_ip_in, server_port_in)
