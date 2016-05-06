import falcon
import subprocess
from .configuration import Setting
from .configuration import Definition


class RequestStream(object):
    def __init__(self, commander):
        # Commander need to be passed to every sub-client action for stream task handler
        self.__commander = commander

    def on_get(self, req, res):
        """
        GET: /request?id={object_id}$token={None}
        """
        if req.params[Definition.get_string_request_token()] == Setting.get_token():
            # Import request string from another project, for consistency change and update
            from server_stream.configuration import Definition as ss_d
            obj_name = req.params[ss_d.ObjectDefinition.get_string_object_id()].strip()
            if len(req.remote_addr) == 0:
                res.body = "Invalid requester address."
                res.content_type = "String"
                res.status = falcon.HTTP_401
            else:
                self.__commander.get_object(req.remote_addr, obj_name, Setting.get_token())
                res.body = "In queue."
                res.content_type = "String"
                res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class ReportStat(object):
    def on_get(self, req, res):
        """
        GET: /report
        """
        from .subprocess_processing_time import ProcessingTimeCollector
        res.body = str(ProcessingTimeCollector.get_sum_report())
        res.content_type = "String"
        res.status = falcon.HTTP_200


class RequestStatusUpdate(object):
    def __init__(self):
        # No commander is needed for binding this task
        pass

    def get_machine_status(self):
        """
        Get machine status by calling a unix command and fetch for load average
        """
        res = subprocess.check_output(Setting.get_cpu_load_command())
        *_, load1, load5, load15 = res.split(b" ")
        # print("Load1: {0}, Load5: {1}, Load15: {2}".format(load1, load5, load15))

        return load1, load5, load15

    def on_get(self, req, res):
        """
        GET: /status?token={None}
        """
        if req.params[Definition.get_string_request_token()] == Setting.get_token():
            if Definition.get_string_command() in req.params and \
               req.params[Definition.get_string_command()] == Definition.get_string_current_load():

                load1, load5, load15 = self.get_machine_status()
                res.body = "Load 1: {0}, Load 5: {1}, Load 15: {2}".format(float(load1), float(load5), float(load15), end='')
                res.content_type = "String"
                res.status = falcon.HTTP_200
            elif Definition.get_string_command() not in req.params:
                result = self.get_machine_status()
                from .subprocess_processing_time import ProcessingTimeCollector
                from server_stream.configuration import Definition as ss_d
                import datetime
                res_obj = {
                    ss_d.ClientList.get_string_client_name(): Setting.get_node_name(),
                    ss_d.ClientList.get_string_client_addresss(): Setting.get_node_address(),
                    ss_d.ClientList.get_string_client_last_update(): str(datetime.datetime.now()),
                    ss_d.ClientList.get_string_client_load1(): float(result[0]),
                    ss_d.ClientList.get_string_client_load5(): float(result[1]),
                    ss_d.ClientList.get_string_client_load15(): float(result[2]),
                    ss_d.ClientList.get_string_client_average_time(): ProcessingTimeCollector.get_avg_processing_time()
                }
                import json
                res.body = json.dumps(res_obj)
                res.content_type = "String"
                res.status = falcon.HTTP_200
        else:
            res.body = "Invalid token ID."
            res.content_type = "String"
            res.status = falcon.HTTP_401


class RESTService(object):
    def __init__(self, commander):
        # Initialize REST Services
        from wsgiref.simple_server import make_server
        from .configuration import Setting
        api = falcon.API()

        # Add route for getting request command
        from server_stream.configuration import Definition as ss_d
        api.add_route('/' + ss_d.get_string_data_is_ready(), RequestStream(commander))

        # Add route for getting status update
        api.add_route('/' + ss_d.ClientList.get_string_update(), RequestStatusUpdate())

        # Add report stat for experiment
        api.add_route('/report', ReportStat())

        # Establishing a REST server
        self.__server = make_server(Setting.get_local_com_addr(), Setting.get_local_com_port(), api)
        self.__commander = commander

    def run(self):
        print("Client REST Service Enable")
        print("Ready.....\n\n")
        self.__server.serve_forever()
