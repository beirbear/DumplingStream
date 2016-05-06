from .configuration import Definition


class ClientActivity(object):
    # Make it static
    __client_list = {}

    @staticmethod
    def set_client_activity(client_address, client_activities):
        ClientActivity.__client_list[client_address] = client_activities

    @staticmethod
    def remove_client(client_address):
        del ClientActivity.__client_list[client_address]

    @staticmethod
    def get_all_client_keys():
        return str(ClientActivity.__client_list.keys())

    @staticmethod
    def get_all_clients():
        return ClientActivity.__client_list.items()

    @staticmethod
    def update_master():
        """
        Update who is the new master node
        """

        def get_time_criteria(list_item):
            """
            Calculate which load to be used for consideration

            """

            def avg_time(list_items):
                """
                Find average processing time
                """
                total = 0
                for item in list_items:
                    total += item
                return total / len(list_items)

            # Actual Code ------------
            _avg_time = avg_time(list_item)

            if _avg_time > 15:      # 15 is a standard OS load time (constant)
                return Definition.ClientList.get_string_client_load15()
            elif _avg_time > 5:    # 5 is a standard OS load time (constant)
                return Definition.ClientList.get_string_client_load5()
            else:
                return Definition.ClientList.get_string_client_load1()

        # Actual Code -----------
        from .configuration import Setting
        if len(ClientActivity.__client_list) == 1:
            print("New client master node:", next(iter(ClientActivity.__client_list.keys())))
            Setting.set_com_addr(next(iter(ClientActivity.__client_list.keys())))
        elif len(ClientActivity.__client_list) > 1:
            avg_time = [x[Definition.ClientList.get_string_client_average_time()]
                        for x in ClientActivity.__client_list]
            criteria_string = get_time_criteria(avg_time)

            min_name = ""
            min_value = -1

            for name, value in ClientActivity.__client_list.items():
                if value < min_value:
                    min_value = value[criteria_string]
                    min_name = name

            print("New client master node:", min_name)
            Setting.set_com_addr(min_name)
