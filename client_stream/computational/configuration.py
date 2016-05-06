class DataRepositorySetting:
    __data_repository_address = 'localhost'
    __service_path = 'dataRepository'
    __data_repository_port = 8100
    __token = "None"
    __node_name = "Subprocess1"

    @staticmethod
    def get_repo_addr():
        return DataRepositorySetting.__data_repository_address

    @staticmethod
    def get_repo_port():
        return DataRepositorySetting.__data_repository_port

    @staticmethod
    def get_repo_token():
        return DataRepositorySetting.__token

    @staticmethod
    def get_node_name():
        return DataRepositorySetting.__node_name

    @staticmethod
    def get_push_request_string(_id, _realization, _label):
        return "http://{0}:{1}/{2}?{3}={4}&{5}={6}&{7}={8}&{9}={10}&{11}={12}&{13}={14}&"\
                .format(DataRepositorySetting.__data_repository_address,
                        DataRepositorySetting.__data_repository_port,
                        DataRepositorySetting.__service_path,
                        Definitions.get_string_request_token(),
                        DataRepositorySetting.__token,
                        Definitions.get_string_id(),
                        _id,
                        Definitions.get_string_realization(),
                        _realization,
                        Definitions.get_string_label(),
                        _label,
                        Definitions.get_string_maker(),
                        DataRepositorySetting.__node_name)

class Definitions:
    __token = 'token'
    __id = 'id'
    __realization = 'realizations'
    __label = 'label'
    __created_by = 'created_by'

    @staticmethod
    def get_string_request_token():
        return Definitions.__token

    @staticmethod
    def get_string_id():
        return Definitions.__id

    @staticmethod
    def get_string_realization():
        return Definitions.__realization

    @staticmethod
    def get_string_label():
        return Definitions.__label

    @staticmethod
    def get_string_maker():
        return Definitions.__created_by