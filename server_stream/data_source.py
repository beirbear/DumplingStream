from abc import ABCMeta, abstractmethod


class DataSource(metaclass=ABCMeta):
    """
    This is ab an abstract that wrap the inherited data sources, (Local, Swift Bucket, Actual Simulation).
    """
    @abstractmethod
    def get_data(self, byte_object, file_idx):
        pass


class LocalFileDataSource(DataSource):
    """
    This class use data from local files as data source.
    -----------------------------------------------------------------------------------------
    CAUTION: The implementation of method in this class doesn't prevent from race condition.
    We implement this way because we rely on Thread in Python that is controlled by GIL.
    When, you change from Thread to Process Pool. You must implement some kind of lock to
    make the synchronization correct.
    -----------------------------------------------------------------------------------------
    """

    def __init__(self, source_folder='/', file_extension='*'):
        # Check that folder is exist or not, if not throw exception
        import os
        if not os.path.isdir(source_folder):
            raise Exception("Input folder in data source does not exist!")

        if source_folder[-1] != '/':
            source_folder += '/'

        import glob
        self.__source_files = glob.glob(source_folder + '*.' + file_extension)
        self.__source_folder = source_folder
        self.__index = 0
        print("{0} local files register.".format(len(self.__source_files)))
        if len(self.__source_files) == 0:
            raise Exception("ERR-SrcFiles: There is no file in the folder with a specified extension.")

    def get_data(self, byte_object, file_idx):
        """
        Get data from file and remove file from list.
        """
        if isinstance(byte_object, bytearray):
            with open(self.__source_files[file_idx], 'rb') as t:
                byte_object += t.read()
        else:
            raise Exception("Function requires bytes array.")

    def get_next_file_id(self):
        if self.__index < len(self.__source_files):
            tmp = self.__index
            self.__index += 1
            return tmp
        return None

    def is_valid_file_id(self, object_id):
        if object_id < len(self.__source_files):
            return True

        return False

    @property
    def is_done(self):
        """
        Purpose: To check that do we still have some data to be stream.
        This function is only apply to finite data set. So, I not put it in the DataSource.
        :return: True or False
        """
        if self.__index < len(self.__source_files):
            return False

        return True
