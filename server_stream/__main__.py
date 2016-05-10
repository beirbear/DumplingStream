"""
Application entry point.
"""

import urllib.request
import urllib.error
import time
import threading
from .configuration import Setting
from .configuration import Definition

# Define an active client class for deal with multiple client
from .active_clients import ActiveClients
clientList = ActiveClients()


def run_rest_server():
    """
    This function is used for running REST service by throwing it into a thread pool.
    """
    from .web_server import WebServer

    print("Enabling REST Services")
    web_server = WebServer()
    web_server.run()


def update_client_status():
    """
    This function will update client by send a request to clients repeatedly
    """

    def get_client_status(address):
        print("Request for client status update: ", address)
        res = None
        req = urllib.request.Request(url=address, data=b"", method='GET')
        try:
            # nonlocal res
            res = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print("{0}: Cannot reach the client: {1}".format(e.code, address))

        return res.read().decode()

    # Actual Code -----
    while Setting.is_running:
        time.sleep(Setting.get_update_latency())
        for item in clientList.client_list:
            res = str(get_client_status(str(item)))
            if len(res) > 0:
                # Update
                import json
                json_respond = json.loads(res)
                client_name = json_respond[Definition.ClientList.get_string_client_name()].strip()
                client_address = json_respond[Definition.ClientList.get_string_client_addresss()].strip()
                client_last_update = json_respond[Definition.ClientList.get_string_client_last_update()].strip()
                client_load1 = json_respond[Definition.ClientList.get_string_client_load1()]
                client_load5 = json_respond[Definition.ClientList.get_string_client_load5()]
                client_load15 = json_respond[Definition.ClientList.get_string_client_load15()]

                clientList.register_client(client_name, client_address, client_last_update, client_load1, client_load5, client_load15)


def parallel_request(attributes):
    """
    This function will send a message to inform the client that the data is ready to be retrieved.
    """
    file_id, target_client = attributes

    def submit_request(url):
        # Sending request to server
        try:
            req = urllib.request.Request(url=url, data=b"", method='GET')
            ret = urllib.request.urlopen(req)
            if ret.status != 200:
                print("ERR: Request for stream error with non 200 status.")
                return False

        except Exception as e:
            print("ERR: Request for stream error by the program.\n" + str(e))
            return False

        return True

    """ Prepare the request command and REST string """
    from .request_content import RequestContent
    url_string = RequestContent(file_id, target_client)

    print("STD: Sending request for stream with content \"{1}\" to {0}.".format(target_client, str(url_string)))

    while not submit_request(url_string):
        print("ERR: Sending request for stream with content \"{1}\" to {0} error! Try again in {2}.".format(target_client,
                                                                                                            str(url_string),
                                                                                                            Setting.get_idle_time()))
        time.sleep(Setting.get_idle_time())


def run_server_socket(data_source):
    """
    This function initialize the server socket for handl;e request from client
    """
    from .server_socket import ThreadedTCPServer, ThreadedTCPRequestHandler
    server = ThreadedTCPServer((Setting.get_data_addr(), Setting.get_data_port()),
                               ThreadedTCPRequestHandler, bind_and_activate=True)

    # Bind data source to the mixin server
    server.mycustomdata = data_source

    # Start a thread with the server -- that thread will then start one
    server_thread = threading.Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()

    """ Have to test for graceful termination. """
    # server.shutdown()
    # server.server_close()

    print("Enabling Server Socket")


def main():
    """
    This is the main code of the application. Entry point function.
    """

    print("Running... Server Stream")

    # Read configuration from file
    Setting.read_configuration_from_file()

    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()

    # Prepare data source
    from .data_source import LocalFileDataSource
    data_source = LocalFileDataSource(source_folder='/home/ubuntu/data_source', file_extension='p')

    # Start Server Socket
    pool.submit(run_server_socket(data_source))

    # Start REST Service
    pool.submit(run_rest_server)

    # Start monitoring client workload
    pool.submit(update_client_status)

    """ Start Streaming """

    # Wait until the system get registered by client
    while not clientList.has_client:
        time.sleep(Setting.get_idle_time())

    # Start sending call back
    while not data_source.is_done:
        target_client = clientList.get_client_addr()
        pool.submit(parallel_request, (data_source.get_next_file_id(), target_client))

if __name__ == "__main__":
    main()
