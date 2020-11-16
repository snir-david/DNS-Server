import socket
import time


def main(my_port, parent_ip, parent_port, ips_file_name):
    found_ip = False
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(my_port)))
    while True:
        current_time = time.time()
        data, addr = s.recvfrom(1024)
        address = data.decode()
        with open(ips_file_name) as file:
            for line in file.readlines():
                line_array = line.split(',')
                if line_array[0] == address:
                    found_ip = True
                    break
        if found_ip:
            ip_array = line.split(',')
            ip_bytes = str.encode(ip_array[1])
            s.sendto(ip_bytes, addr)
            found_ip = False
        else:
            found_ip = False
            s.sendto(data, (parent_ip, int(parent_port)))
            ip_back_from_server, addr = s.recvfrom(1024)
            data = ips_file_name.decode()
            data.appened(current_time)
            file.writelines(data)
            s.sendto(ip_back_from_server, addr)
        with open(ips_file_name) as file:
            for line in file.readlines():
                line_split = line.split(',')
                if line_split[3] != 0:
                    if line_split[2] < current_time - line_split[3]:
                        del line


if __name__ == "__main__":
    my_port_in, parent_ip_in, parent_port_in, ips_file_name_in = input().split()
    main(my_port_in, parent_ip_in, parent_port_in, ips_file_name_in)
