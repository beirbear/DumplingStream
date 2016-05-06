"""
Application entry point.
"""

from .commander import Commander
from .configuration import Setting


def main():
    """
    The main routine.
    """
    print("Running Client Stream")
    print("Node name: ", Setting.get_node_name())

    # Create thread for handling REST Service
    from concurrent.futures import ThreadPoolExecutor
    pool = ThreadPoolExecutor()

    # Create commander for handling tasks
    commander = Commander()

    # Binding commander to the rest service and enable REST service
    pool.submit(run_rest_service, commander)


def run_rest_service(commander):
    """
    Run rest as in a thread function
    """
    from .rest_service import RESTService
    rest = RESTService(commander)
    rest.run()


if __name__ == "__main__":

    # Read configuration from file
    Setting.read_configuration_from_file()

    # Run the application
    main()
