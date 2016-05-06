'''
client_socket: send the data to the server_socket with a dedicate port
'''

import socket
import sys

class ClientSocket(object):
    def __init__(self, data_source, data_dest_addr, data_dest_port):
        self.__content = None
        self.__data_source = None
        self.__data_dest_addr = data_dest_addr
        self.__data_dest_port = data_dest_port

    def read_file(self):
        with open(self.__data_source) as f:
            self.__content = f.read()

    def run_from_input(self, content):
        self.__content = content
        self.__run()

    def run_from_file(self, data_source):
        self.__data_source = data_source
        self.read_file()
        self.__run()

    def __run(self):
        if not self.__content:
            raise RuntimeError("Empty content")

        s = None
        for res in socket.getaddrinfo(self.__data_dest_addr, self.__data_dest_port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            af, sock_type, proto, canonname, sa = res
            try:
                s = socket.socket(af, sock_type, proto)
            except OSError as msg:
                s = None
                continue

            try:
                s.connect(sa)
            except OSError as msg:
                s.close()
                s = None
                continue
            break

        if not s:
            print("Couldn't open socket")
            sys.exit(-1)

        print("Start sending file")
        s.sendall(self.__content.encode())

        s.sendall(b"")

        s.close()
        print("Send data complete")


