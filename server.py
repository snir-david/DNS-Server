import socket
import time


# preparing file for using it in the future
def prepare_file(ips_file_lines):
    line_array = []
    # converting lines (by using split) to array, adding timestamp (in 3 cell)
    for line in ips_file_lines:
        if line.__contains__('\n'):
            line = line.replace('\n', '')
        line_split = line.split(',')
        if len(line_split) < 4:
            line_split.append('-1')
        line_array.append(line_split)
    return line_array


# checking if the ips file has the address that the client asking for
def check_address(ips_file_lines, address):
    for line in ips_file_lines:
        if line[0] == address:
            return line
    return None


# if we found the address, sending answer to the client
def send_to_client(socket_c, line, address):
    # convert list to string for encoding
    ips_string = ",".join(line)
    ip_bytes = str.encode(ips_string)
    # sending the answer to client
    socket_c.sendto(ip_bytes, address)


# if we haven't found the address - sending request to parent server
def parent_server(socket_p, parent_ip, parent_port, data, line_array, current_time, ips_file):
    # sending request for parent server
    socket_p.sendto(data, (parent_ip, int(parent_port)))
    ip_back_from_server, addr = socket_p.recvfrom(1024)
    # decoding answer from server
    data_decode = ip_back_from_server.decode()
    # converting to array using split
    data_decode_split = data_decode.split(',')
    # adding current time (using to check TTL), convert to string and adding to array
    time_string = str(current_time)
    data_decode_split[3] = time_string
    data_string = ",".join(data_decode_split)
    line_array.append(data_string.split(','))
    # writes the new information in the file
    ip_file_append = open(ips_file, "a")
    ip_file_append.write("\n")
    ip_file_append.write(data_string)
    ip_file_append.close()
    # sending the answer to the client
    socket_p.sendto(ip_back_from_server, addr)


def checking_ttl(ips_file_array, ips_file_lines, current_time):
    for index, line in enumerate(ips_file_array):
        # if time stamp equal -1 - the address was here from the start. else, check TTL
        if line[3] != '-1':
            # if TTL smaller then current time - timestamp - forget line
            line_2_float = float(line[2])
            line_3_float = float(line[3])
            current_ttl = current_time - line_3_float
            if line_2_float < current_ttl:
                ips_file_array.remove(line)
                del ips_file_lines[index]


def main(my_port, parent_ip, parent_port, ips_file_name):
    # open ips file, read lines and convert to array by using prepare_file function
    ips_file = open(ips_file_name, "r")
    ips_file_lines = ips_file.readlines()
    ips_file_array = prepare_file(ips_file_lines)
    # open a socket for communication
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', int(my_port)))
    while True:
        # time stamp for using later
        current_time = time.time()
        # checking TTL
        checking_ttl(ips_file_array, ips_file_lines, current_time)
        # getting a request from client and decoding it from byte to string
        data, addr = s.recvfrom(1024)
        address = data.decode()
        # checking if we have the ip of this address
        line = check_address(ips_file_array, address)
        # if we do, send client answer
        if line is not None:
            send_to_client(s, line, addr)
        # else, send a request to parent server
        else:
            parent_server(s, parent_ip, parent_port, data, ips_file_array, current_time, ips_file_name)


if __name__ == "__main__":
    my_port_in, parent_ip_in, parent_port_in, ips_file_name_in = input().split()
    main(my_port_in, parent_ip_in, parent_port_in, ips_file_name_in)
