import subprocess
import time
from .configuration import Setting


class Commander(object):
    """
    Commander class is equivalent to TaskManager in the document. It control the micro batch of the system by
    create a sub-process to invoke with everternal process.
    """

    def __init__(self):
        """
        Initialization: define size of the worker node in the process pool
        """
        import concurrent.futures
        """Size of the worker nodes refer from the global setting in configuration file."""
        self.thread_pool = concurrent.futures.ProcessPoolExecutor(max_workers=Setting.ExternalProcess.get_max_worker())

    def get_object(self, host, object_name, token):
        """
        This function is called when we want to get an object by calling another process to deal with it.
        """

        from server_stream.configuration import Definition as ss_d
        from .configuration import Definition as cs_d
        url = "/{0}?{1}={2}&{3}={4}".format(ss_d.get_string_data_is_ready(),
                                            ss_d.ObjectDefinition.get_string_object_id(),
                                            object_name,
                                            cs_d.get_string_request_token(),
                                            token)
        self.thread_pool.map(get_object_pipeline, (url,))


def get_object_pipeline(item):
    """
    This is a function that we throw into a process pool for parallel processing.
    """
    def call_ext_process():
        from .configuration import Setting
        cmd = Setting.ExternalProcess.get_external_process() + [item, Setting.get_server_addr(), Setting.ExternalProcess.get_data_port(),
                                                                Setting.get_node_name(), Setting.get_token()]
        return_code = subprocess.call(cmd)

        # Check for return code
        if return_code != Setting.ExternalProcess.get_success_return_code():
            return False

        return True

    while not call_ext_process():
        time.sleep(Setting.ExternalProcess.get_idle_time())
