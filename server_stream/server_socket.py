import socketserver
from .configuration import Definition, Setting

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

    def handle(self):
        # Receive and interpret the request data
        # 2048 is the standard size of the TCP
        data = str(self.request.recv(2048), 'utf-8')

        # Read the request and extract parameter
        params = Definition.ObjectDefinition.get_object_item(data)

        # Check for token
        if params[Definition.ObjectDefinition.get_string_object_token()] == Setting.get_token():
            print("STD: Sending data (id: {0}) to {1}.".format(params[Definition.ObjectDefinition.get_string_object_id()],
                                                                      self.client_address[0]))

            if self.server.mycustomdata.is_valid_file_id(params[Definition.ObjectDefinition.get_string_object_id()]):
                content = bytearray()
                content = self.server.mycustomdata.get_data(content, params[Definition.ObjectDefinition.get_string_object_id()])
                self.request.sendall(content)
                self.request.send(b"")

            else:
                print("ERR: Invalid Token.")
                self.request.sendall("Invalid token.")
                self.request.send(b"")

        else:
            print("ERR: Invalid.")
            self.request.sendall("Invalid token.")
            self.request.send(b"")
