
class Setting(object):
    __com_addr = "localhost"
    __com_port = 8080
    __data_addr = "localhost"
    __data_port = 9999
    __update_client_status_latency = 60
    __standard_idle_time = 5
    __dynamic_token = "None"

    @staticmethod
    def read_configuration_from_file():
        import os.path
        if not os.path.exists("server_stream/configuration.json"):
            raise Exception("configuration.json does not exist!")

        with open("server_stream/configuration.json", "rt") as t:
            data = eval(t.read())

        # check for the parameters
        if "com_addr" in data and \
           "com_port" in data and \
           "data_addr" in data and \
           "data_port" in data and \
           "standard_idle_time" in data and \
           "update_client_status_latency" in data and \
           "token" in data:

            try:
                # Data preparation
                com_addr = data["com_addr"].strip()
                data_addr = data["data_addr"].strip()
                token = data["token"].strip()
                com_port = int(data["com_port"])
                data_port = int(data["data_port"])
                std_idle_time = int(data["standard_idle_time"])
                client_update_latency = int(data["update_client_status_latency"])

                Setting.__com_addr = com_addr
                Setting.__com_port = com_port
                Setting.__data_addr = data_addr
                Setting.__data_port = data_port
                Setting.__update_client_status_latency = client_update_latency
                Setting.__standard_idle_time = std_idle_time
                Setting.__dynamic_token = token

            except:
                raise Exception("Invalid type in configuration.")
        else:
            print("ERR-Conf: Invalid parameter in configuration file.")

    @staticmethod
    def get_data_port():
        return Setting.__data_port

    @staticmethod
    def get_data_addr():
        return Setting.__data_addr

    @staticmethod
    def is_running(new_value):
        Setting.__is_running = new_value

    @staticmethod
    def get_update_latency():
        return Setting.__update_client_status_latency

    @staticmethod
    def get_com_addr():
        return Setting.__com_addr

    @staticmethod
    def get_com_port():
        return Setting.__com_port

    @staticmethod
    def get_idle_time():
        return Setting.__standard_idle_time

    @staticmethod
    def get_token():
        return Setting.__dynamic_token


class Definition(object):

    @staticmethod
    def get_string_data_is_ready():
        return 'request'

    @staticmethod
    def get_client_definition():
        return Definition.ClientList()

    class ObjectDefinition(object):

        @staticmethod
        def get_string_object_id():
            return 'id'

        @staticmethod
        def get_string_object_token():
            return 'token'

        @staticmethod
        def get_object_item(req_input):
            """
            Input request format: http://localhost:8080/request?id=0&token=None
            return: Dictionary of paramers
            """
            params = req_input.split("?")[1].split("&")
            params_dict = {Definition.ObjectDefinition.get_string_object_id(): None,
                           Definition.ObjectDefinition.get_string_object_token(): None}

            for line in params:
                values = line.split("=")
                if values[0] == Definition.ObjectDefinition.get_string_object_id():
                    params_dict[Definition.ObjectDefinition.get_string_object_id()] = int(values[1])
                elif values[0] == Definition.ObjectDefinition.get_string_object_token():
                    params_dict[Definition.ObjectDefinition.get_string_object_token()] = values[1]

            return params_dict

    class ClientList(object):

        @staticmethod
        def get_string_update():
            return 'status'

        @staticmethod
        def get_string_client_name():
            return 'name'

        @staticmethod
        def get_string_client_addresss():
            return 'address'

        @staticmethod
        def get_string_client_last_update():
            return 'last_update'

        @staticmethod
        def get_string_client_load1():
            return 'last_load1'

        @staticmethod
        def get_string_client_load5():
            return 'last_load5'

        @staticmethod
        def get_string_client_load15():
            return 'last_load15'

        @staticmethod
        def get_string_client_average_time():
            return 'average_time'
