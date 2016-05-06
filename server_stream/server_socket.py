import socketserver
from .data_source import DataSource


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    Definition class
    """
    pass


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """
    This class is the main class that handle with requests from clients.
    the actual mechanism that pass the data to clients.
    """
    def __init__(self, data_source):
        """
        Purpose: initialize the request handler.
        :param data_source: the data source object that can access to the data source
        """
        if not isinstance(data_source, DataSource):
            raise Exception("Invalid DataSource")

        self.__data_source = data_source

    def handle(self):
        # Receive and interpret the request data
        # 2048 is the standard size of the TCP
        data = str(self.request.recv(2048), 'utf-8')

        """ Send content back to the client

        content = None
        m = hashlib.md5()
        m.update(contents[int(data)])
        print("{0}:{1}".format(data, m.hexdigest()))

        cur_thread = threading.current_thread()
        # response = bytes("{}: {}".format(cur_thread.name, data), 'utf-8')
        #print("Send file content {0} back".format(data))
        #print("Current Thread", cur_thread.name)
        self.request.sendall(contents[int(data)])
        # self.request.send(b"")
        """


