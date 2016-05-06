
class Setting(object):
    __com_addr = "localhost"
    __com_port = 8080
    __data_port = 9999
    __data_addr = "localhost"
    __update_client_status_latency = 60
    __standard_idle_time = 5
    __dynamic_token = "None"

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
