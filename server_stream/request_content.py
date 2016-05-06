from .configuration import Setting
from .configuration import Definition


class RequestContent(object):
    def __init__(self, _id, client_addr, token=None):
        self.__id = _id
        self.__token = token
        self.__command = Definition.get_string_data_is_ready()
        self.__client_addr = client_addr

    def __str__(self):
        return "http://{0}:{1}/{2}?id={3}&token={4}".format(self.__client_addr,
                                                            Setting.get_com_port(),
                                                            self.__command,
                                                            self.__id,
                                                            self.__token)

    def get_url_string(self):
        """
        Get a URL string for making a request
        """
        return self.__str__()


class RequestClientStatus(object):
    def __init__(self, name, address, last_update=None, load1=None, load5=None, load15=None, token=None):
        self.__name = name
        self.__address = address
        self.__last_update = last_update
        self.__load1 = load1
        self.__load5 = load5
        self.__load15 = load15
        self.__token = token

    def __str__(self):
        return "http://{0}:{1}/{2}?token={3}".format(self.__address,
                                                     Setting.get_com_port(),
                                                     Definition.ClientList.get_string_update(),
                                                     self.__token)

    def get_url_string(self):
        return self.__str__()