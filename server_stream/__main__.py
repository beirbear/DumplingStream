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

    print("REST Services is running...")
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
    print("Client Status Updater Enabled.")
    while Setting.is_running:
        time.sleep(Setting.get_update_latency())
        from .client_active_list import ClientActivity
        for key, value in ClientActivity.get_all_clients():
            res = str(get_client_status(str(value)))
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

                if len(client_name) > 0 and len(client_address) > 0 and len(client_last_update) > 0 \
                        and client_load1 > 0 and client_load5 > 0 and client_load15 > 0:

                    # Create object structure for client_list
                    from .request_content import RequestClientStatus
                    client_info = RequestClientStatus(name=client_name,
                                                      address=client_address,
                                                      last_update=client_last_update,
                                                      load1=client_load1,
                                                      load5=client_load5,
                                                      load15=client_load15)

                    from .client_active_list import ClientActivity
                    ClientActivity.set_client_activity(client_address, client_info)

        # Update new master node
        ClientActivity.update_master()


def parallel_request(attributes):
    """
    This function will send a message to inform the client that the data is ready to be retrieved.
    """
    file_id, target_client = attributes

    def submit_request(url):
        # Sending request to server
        try:

            req = urllib.request.Request(url=url, data=b"", method='GET')
            # print(req)
            ret = urllib.request.urlopen(req)
            # print("ret", ret)
            if ret.status != 200:
                print("Found non 200 status.")
                return False

        except Exception as e:
            print("Exception:", e)
            return False

        return True

    # Prepare for REST string
    from .request_content import RequestContent
    url_string = RequestContent(file_id, target_client)

    print("Callback to {0}: {1}".format(target_client, str(url_string)))

    while not submit_request(url_string):
        time.sleep(5)


def run_server_socket(data_source):
    """
    This function initialize the server socket for handl;e request from client
    """
    from .server_socket import ThreadedTCPServer, ThreadedTCPRequestHandler
    server = ThreadedTCPServer((Setting.get_data_addr(), Setting.get_data_port()),
                               ThreadedTCPRequestHandler(data_source), bind_and_activate=True)

    # Start a thread with the server -- that thread will then start one
    server_thread = threading.Thread(target=server.serve_forever)

    # Exit the server thread when the main thread terminates
    # server_thread.daemon = True
    server_thread.start()

    """ Have to test for graceful termination. """
    # server.shutdown()
    # server.server_close()

    print("Server Socket is running...")


def main():
    """
    This is the main code of the application. Entry point function.
    """

    print("Running... Server Stream")

    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()

    # Prepare data source
    from .data_source import LocalFileDataSource
    data_source = LocalFileDataSource(source_folder='/Users/beir/Desktop/tmp/samples_data/')

    # Start Server Socket
    pool.submit(run_server_socket(data_source))

    # Start REST Service
    pool.submit(run_rest_server)

    # Start monitoring client workload
    """ Experiment """
    # global client_activity
    # pool.submit(update_client_status)
    """ Experiment """

    # Start MixinServer

    # Wait until the system get registered by client
    while not clientList.has_client:
        time.sleep(Setting.get_idle_time())

    # Start sending call back
    while not data_source.is_done:
        target_client = clientList.get_client_addr()
        pool.submit(parallel_request, (data_source.get_next_file_id(), target_client))


if __name__ == "__main__":
    main()
