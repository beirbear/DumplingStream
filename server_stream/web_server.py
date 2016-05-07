import falcon
import os.path
import datetime
from .configuration import Setting
from .configuration import Definition


class RequestObject(object):
    def __init__(self):
        pass

    def on_get(self, req, res):
        """
        GET: /request?id={object_id}&token=None
        """
        if req.params[Definition.ObjectDefinition.get_string_object_token()] == Setting.get_token():
            res.body = "No longer support for this services."
            res.content_type = "String"
            res.status = falcon.HTTP_404
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class ClientsUpdate(object):
    def __init__(self):
        pass

    def on_get(self, req, res):
        """
        GET: /status?token=None
        """
        """
        if req.params[Definition.ObjectDefinition.get_string_object_token()] == Setting.get_token():
            from .client_active_list import ClientActivity
            res.body = ClientActivity.get_all_client_keys()
            res.content_type = "String"
            res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401
        """

    def on_post(self, req, res):
        """
        Purpose: Register client
        POST: /status?name={client_name}&address={client_address}&last_update={last_update}&
                last_load1={number}&last_load5={number}&last_load15={number}&token=None
        """
        if req.params[Definition.ObjectDefinition.get_string_object_token()] == Setting.get_token():
            # Unpack request parameters
            client_name = req.params[Definition.ClientList.get_string_client_name()].strip()
            client_address = req.params[Definition.ClientList.get_string_client_addresss()].strip()
            client_last_update = req.params[Definition.ClientList.get_string_client_last_update()].strip()
            client_load1 = req.params[Definition.ClientList.get_string_client_load1()].strip()
            client_load5 = req.params[Definition.ClientList.get_string_client_load5()].strip()
            client_load15 = req.params[Definition.ClientList.get_string_client_load15()].strip()

            if len(client_name) > 0 and len(client_address) > 0 and len(client_last_update) > 0 \
               and len(client_load1) > 0 and len(client_load5) > 0 and len(client_load15) > 0:
                # convert string to number
                try:
                    client_load1 = float(client_load1)
                    client_load5 = float(client_load5)
                    client_load15 = float(client_load15)
                    client_last_update = eval(client_last_update)

                    # Add node to a list and calculate a new master node
                    from .__main__ import clientList
                    rCode = clientList.register_client(client_name,
                                                       client_address,
                                                       client_last_update,
                                                       client_load1,
                                                       client_load5,
                                                       client_load15)

                    if rCode == 1:
                        res.body = "Add new client completed."
                        res.content_type = "String"
                        res.status = falcon.HTTP_200
                    elif rCode == 2:
                        res.body = "Update client completed."
                        res.content_type = "String"
                        res.status = falcon.HTTP_200
                    elif rCode == -2:
                        res.body = "Obsolete request."
                        res.content_type = "String"
                        res.status = falcon.HTTP_400
                    else:
                        res.body = "Error in registering new client."
                        res.content_type = "String"
                        res.status = falcon.HTTP_400
                except TypeError:
                    print("Invalid number type in load's variables.")
                    res.body = "Invalid number type in load's variables."
                    res.status = falcon.HTTP_400
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class WebServer(object):
    def __init__(self):
        # Initializing REST Service
        from wsgiref.simple_server import make_server
        api = falcon.API()

        # Bind request object command
        api.add_route('/' + Definition.get_string_data_is_ready(), RequestObject())
        # Bind request update/register client node
        api.add_route('/' + Definition.ClientList.get_string_update(), ClientsUpdate())

        # Need to change to this code when we run on the actual server
        # self.__server = make_server(Setting.get_com_addr(), 8090, api)
        self.__server = make_server(Setting.get_com_addr(), Setting.get_com_port(), api)

    def run(self):
        print("Server REST Service Enable")
        print("Ready.....\n\n")
        self.__server.serve_forever()
