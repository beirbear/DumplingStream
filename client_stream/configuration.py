class Setting(object):
    __node_name = 'Node1'
    __node_address = 'localhost'
    __com_addr = '127.0.0.1'
    __com_port = 8080
    __dynamic_token = "None"
    __processing_time_max_record = 200

    class ExternalProcess(object):
        __process_command = ['python', '/Users/beir/PycharmProjects/DumplingStream/client_stream/computational/feature_creation.py']
        __success_return_code = 0
        __max_worker = 8

        @staticmethod
        def get_external_process():
            return Setting.ExternalProcess.__process_command

        @staticmethod
        def get_success_return_code():
            return Setting.ExternalProcess.__success_return_code

        @staticmethod
        def get_max_worker():
            return Setting.ExternalProcess.__max_worker

        @staticmethod
        def read_configuration_from_file():
            # Check that the configuration file exist or not
            import os.path
            if not os.path.exists("client_stream/configuration.json"):
                raise Exception("configuration.json doesn't exist.")

            with open('client_stream/configuration.json', 'rt') as t:
                data = eval(t.read())

            if 'node_name' in data and \
               'node_addr' in data and \
               'server_addr' in data and \
               'server_port' in data and \
               'token' in data and \
               'external_process' in data and \
               'ext_command' in data['external_process'] and \
               'success_code' in data['external_process'] and \
               'max_worker' in data['external_process']:

                try:
                    Setting.__node_name = data['node_name']
                    Setting.__node_address = data['node_addr']
                    Setting.__com_addr = data['server_addr']
                    Setting.__com_port = data['server_port']
                    Setting.__dynamic_token = data['token']
                    Setting.ExternalProcess.__process_command = data['external_process']['ext_command']
                    Setting.ExternalProcess.__success_return_code = data['external_process']['success_code']
                    Setting.ExternalProcess.__max_worker = data['external_process']['max_worker']

                except Exception as e:
                    raise Exception(e)
            else:
                raise Exception("There are somethings wrong with configuration.json")

    @staticmethod
    def read_configuration_from_file():
        Setting.ExternalProcess.read_configuration_from_file()

    @staticmethod
    def get_node_name():
        return Setting.__node_name

    @staticmethod
    def get_node_address():
        return Setting.__node_address

    @staticmethod
    def set_node_name(new_name):
        Setting.__node_name = new_name

    @staticmethod
    def get_local_com_addr():
        return Setting.__com_addr

    @staticmethod
    def get_local_com_port():
        return Setting.__com_port

    @staticmethod
    def get_token():
        return Setting.__dynamic_token

    @staticmethod
    def get_max_processing_time_record():
        return Setting.__processing_time_max_record


class Definition:

    @staticmethod
    def get_string_request_token():
        return 'token'

    @staticmethod
    def get_string_command():
        return 'command'

    @staticmethod
    def get_string_current_load():
        return 'current_load'

    @staticmethod
    def get_cpu_load_command():
        return ['uptime', '|', 'awk', '{ print $8 $9 $10}']

