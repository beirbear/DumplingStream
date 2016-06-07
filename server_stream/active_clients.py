from .configuration import Setting, Definition
from datetime import datetime

class Singleton(type):
    """
    Singleton Design Pattern.
    """
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance


class ClientRecord(object):
    def __init__(self, name, address, last_update, load1, load5, load15):
        self.name = name
        self.address = address
        self.last_update = last_update
        self.load1 = load1
        self.load5 = load5
        self.load15 = load15

    @property
    def highest_load(self):
        load = self.load1
        if self.load5 > load:
            load = self.load5
        if self.load15 > load:
            load = self.load15

        return load

    def __str__(self):
        return "http://{0}:{1}/{2}?token={3}".format(self.address,
                                                     Setting.get_com_port(),
                                                     Definition.ClientList.get_string_update(),
                                                     Setting.get_token())


class ActiveClients(metaclass=Singleton):
    """
    This class is a class container that deal with client list and make a decision that which clients should get a request.
    """

    def __init__(self):
        self.__client_list = list()
        self.__client_index = 0
        self.__least_load_addr = None

    @property
    def has_client(self):
        if len(self.__client_list) > 0:
            return True

        return False

    @property
    def client_list(self):
        return self.__client_list

    def get_client_addr(self):
        if len(self.__client_list) == 0:
            raise Exception("No client registered.")

        return self.__client_list[self.__get_client_index()].address

    def get_least_load_client(self):
        return self.__least_load_addr

    def __get_client_index(self):
        self.__client_index += 1
        if self.__client_index >= len(self.__client_list):
            self.__client_index = 0

        return self.__client_index

    def __update_least_load_addr(self):
        if len(self.__client_list) == 0:
            return None

        candidate_client = {"id": -1, "load": 0}
        for i, item in enumerate(self.__client_list):
            max = item.load1
            if item.load5 > max:
                max = item.load5
            if item.load15 > max:
                max = item.load15

            if max > candidate_client.load:
                candidate_client.id = i
                candidate_client.load = max

        self.__least_load_addr = self.client_list[candidate_client.id].address

    def register_client(self, name, address, last_update, load1, load5, load15):

        # Check that is it empty list or not, if empty, just insert
        if len(self.__client_list) == 0:
            self.__client_list.append(ClientRecord(name, address, last_update, load1, load5, load15))
            return 1

        addr_list = [item.address for item in self.__client_list]
        idx = -1
        for i, addr in enumerate(addr_list):
            if addr == address:
                idx = i
                break

        if idx > -1:
            # Client already exist
            if not isinstance(last_update, datetime):
                return -2

            if self.__client_list[idx].last_update < last_update:
                # Update the new info
                self.__client_list[idx].last_update = last_update
                self.__client_list[idx].name = name
                self.__client_list[idx].load1 = load1
                self.__client_list[idx].load5 = load5
                self.__client_list[idx].load15 = load15
                self.__update_least_load_addr()

                return 2
            else:
                return -2
        else:
            # Client not exist in the list yet. Just insert it
            self.__client_list.append(ClientRecord(name, address, last_update, load1, load5, load15))
            return 1

