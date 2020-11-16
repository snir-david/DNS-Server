import socket


def main(server_ip, server_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    address: str = input()
    address_in_bytes = str.encode(address)
    s.sendto(address_in_bytes, (server_ip, int(server_port)))
    ip_back_from_server, addr = s.recvfrom(1024)
    ip = ip_back_from_server.decode()
    print(ip)
    s.close()


if __name__ == '__main__':
    server_ip_in, server_port_in = input().split()
    main(server_ip_in, server_port_in)
