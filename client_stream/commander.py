import subprocess
import time


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
        from .configuration import Setting

        """Size of the worker nodes refer from the global setting in configuration file."""
        self.thread_pool = concurrent.futures.ProcessPoolExecutor(max_workers=Setting.ExternalProcess.get_max_worker())

    def get_object(self, host, object_name, token):
        """
        This function is called when we want to get an object by calling another process to deal with it.
        """

        from server_stream.configuration import Definition as ss_d
        from .configuration import Definition as cs_d
        url = "http://{0}:{1}/{2}?{3}={4}&{5}={6}".format(host,
                                                          8090,
                                                          ss_d.get_string_data_is_ready(),
                                                          ss_d.ObjectDefinition.get_string_object_id(),
                                                          object_name,
                                                          cs_d.get_string_request_token(),
                                                          token)
        self.thread_pool.map(get_object_pipeline, (url,))

def get_object_pipeline(items):
    """
    This is a function that we throw into a process pool for parallel processing.
    """
    url = items
    # print("Invoke external process with parameters:", url)
    # Capture start processing time
    start_time = time.time()
    from .configuration import Definition
    cmd = Definition.ExternalProcess.get_external_process() + [url]
    return_code = subprocess.call(cmd)

    # Check for return code
    if return_code != Definition.ExternalProcess.get_success_return_code():
        raise Exception("Unsuccessful exit code received.")
    else:
        import datetime
        start_time_string = str(datetime.datetime.now().time())
        elapsed_time = time.time() - start_time
        # print("Process completes in {0} seconds".format(elapsed_time))

        # Skip this part for now! -----------------------------------------
        # Push it into the record system
        # from .subprocess_processing_time import ProcessingTimeCollector
        # ProcessingTimeCollector.add_info(start_time_string, elapsed_time)

