import urllib2
import cPickle as pickle
import socket
import sys
import time
import numpy as np


# Local Configuration ------------------------------------------------
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
        return "http://{0}:{1}/{2}?{3}={4}&{5}={6}&{7}={8}&{9}={10}&{11}={12}"\
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
                        DataRepositorySetting.get_node_name())

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


# Feature Creation ---------------------------------------------------


def check_arrays(data):
    a_len = data.shape[1]
    for i, a in enumerate(data):
        if np.count_nonzero(a) == 0:
            idx = np.random.randint(0, a_len)
            a[idx] = 1
            data[i] = a
    return data


def g2(result_species):
    import time as t
    import numpy as np

    def burstiness(y):
        """
        % DN_Burstiness
        %
        % Returns the 'burstiness' statistic from:
        %
        % Goh and Barabasi, 'Burstiness and memory in complex systems' Europhys. Lett.
        % 81, 48002 (2008)
        %
        % INPUTS:
        % y, the input time series """

        return (np.std(y) - np.mean(y))/(np.std(y) + np.mean(y))

    def skewness(y):
        """
        % Estimates custom skewness measures, the Pearson skewnesses.
        %
        % INPUTS:
        % y, the input time series """

        return (3*np.mean(y)-np.median(y))/np.std(y)

    def CV(x, k=1):
        """
        % Calculates the coefficient of variation, sigma^k / mu^k, of order k
        %
        % INPUTS:
        %
        % x, the input time series
        %
        % k, the order of coefficient of variation (k = 1 is usual) """

        return (np.std(x))**k / (np.mean(x))**k

    def autocorrelations(y ,k=10):
        """
        % Computes the autocorrelation of an input time series, y, at a time-lag up to k
        %
        % INPUTS:
        % y, a scalar time series column vector
        %
        % Output is the autocorrelation for every time lag as an array """

        N = len(y)
        return [np.sum((y[0:N-i] - np.mean(y[0:N-i])) * (y[i:N] - np.mean(y[i:N]))/N/np.std(y[0:N-i])/np.std(y[i:N])) for i in range(1,k)]

    '''
    Move to server side

    def check_if_zero(v):
        if np.count_nonzero(v) == 0:
            return True
        else: return False

    def check_arrays(data):
        a_len = data.shape[1]
        t_data = []
        for i,a in enumerate(data):
            if np.count_nonzero(a) == 0:
                idx = np.random.randint(0,a_len)
                a[idx] = 1
                data[i] = a
        return data
    '''

    def fft_norm(x):
        # remove dc bias
        x -= np.mean(x)
        return np.linalg.norm(abs(np.fft.fft(x)))

    t0 = t.time()

    mapped ={}

    '''
    Move to server side
    parameters = result.model.get_all_parameters()
    mapped['parameters'] = zip(parameters.keys(),(v.expression for v in parameters.values()))
    mapped['D'] = result.model.get_species('mRNA').diffusion_constant
    mapped['tspan'] = result.model.tspan

    result_species = []
    for species in result.model.get_all_species():
        if species == 'protein' or species == 'mRNA':
            #get result
            matrix = result.get_species(species)

            #Check for zero vectors and replace one random element to 1
            matrix = check_arrays(matrix)

            #Transpose the result, should make this matrix.T
            matrixT = np.asarray([list(matrix[:,i]) for i in range(matrix.shape[1])])

            matrixT = check_arrays(matrixT)

            result_species.append((matrix, matrixT))
    '''

    # Sums all CP in each snapshot(m) and per voxel(mT)
    total_sum = []
    for m, mT in result_species:
        m_sum = [np.sum(v) for v in m]
        mt_sum = [np.sum(v) for v in mT]
        # total_sum.append((scipy.signal.savgol_filter(m_sum, 51, 3), scipy.signal.savgol_filter(m_sum, 51, 3)))
        total_sum.append((m_sum, mt_sum))
    # feature vector
    f_vector = []

    # Total CP
    for c, (Sm, SmT) in enumerate(total_sum):
        f_vector.append(np.mean(Sm))
        f_vector.append(burstiness(Sm))
        f_vector.append(burstiness(SmT))
        f_vector.append(skewness(Sm))
        # f_vector.append(skewness(SmT)) remove
        f_vector.append(CV(Sm, 1))
        f_vector.append(CV(SmT, 1))
        f_vector.append(np.linalg.norm(autocorrelations(Sm,len(Sm)/2)))
        # f_vector.append(np.linalg.norm(autocorrelations(SmT,len(SmT)/2))) remove
        f_vector.append(fft_norm(Sm))
        f_vector.append(fft_norm(SmT))
        if c < len(total_sum)-1:                                         ### CHECK IF IT'S CORRECT! 03/18
            for i in range(1, len(total_sum)-c):
                # Correlations of total CP in volume
                f_vector.append(np.corrcoef(Sm,total_sum[c+i][0])[0][1])
                # f_vector.append(np.corrcoef(SmT,total_sum[c+i][1])[0][1]) remove

    for c, (m, mT) in enumerate(result_species):
        bm, bmT, sm, smT, CVm, CVmT, ACm, ACmT = [],[],[],[],[],[],[],[]
        for v in m:
            bm.append(burstiness(v))
            sm.append(skewness(v))
            CVm.append(CV(v, 1))
            # ACm.append(numpy.linalg.norm(f.autocorrelations(v, len(v)/2)))
        for v in mT:
            bmT.append(burstiness(v))
            smT.append(skewness(v))
            CVmT.append(CV(v,1))
            # ACmT.append(numpy.linalg.norm(f.autocorrelations(v, len(v)/2)))
        if c < len(result_species):
            for i in range(1, len(result_species)-c):
                nm, nmT = result_species[c+i]
                corr1 = [np.corrcoef(v, nm[e])[0][1] for e, v in enumerate(m)]
                corr2 = [np.corrcoef(v, nmT[e])[0][1] for e, v in enumerate(mT)]
                f_vector.append(np.linalg.norm(corr1))
                f_vector.append(np.linalg.norm(corr2))
                f_vector.append(np.var(corr1))
                f_vector.append(np.var(corr2))

        for var in [bm, bmT, sm, smT, CVm, CVmT]:
            f_vector.append(np.linalg.norm(var))
            f_vector.append(np.mean(var))
            f_vector.append(np.var(var))

    mapped['features'] = f_vector

    mapped['time for mapper (s)'] = t.time() - t0

    return mapped


# Main --------------------------------------------------------------------


def push_feature_to_repo(url, features):
    method = "POST"
    handler = urllib2.HTTPHandler()
    opener = urllib2.build_opener(handler)

    # Extract Id
    _id = None
    for item in url.split("&"):
        if "id=" in item:
            _id = item.replace("id=","")

    # from .configuration import DataRepositorySetting
    url = DataRepositorySetting.get_push_request_string(_id,
                                                        "HDFS",
                                                        "_")

    def send_data_to_repo(_features):
        import json
        json_feature = json.dumps(_features)
        request = urllib2.Request(url, data=json_feature)

        request.add_header("Content-Type", 'application/json')
        request.get_method = lambda: method

        try:
            connection = opener.open(request)
        except urllib2.HTTPError, e:
            connection = e

        if connection.code == 200:
            return True

        return False

    import time
    while not send_data_to_repo(features):
        time.sleep(5)

# handle the error case. connection.read() will still contain data
# if any was returned, but it probably won't be of any use


def main(argv):
    url = argv[0]

    items = ('localhost', 9999, "http://localhost:8080/request?id=0&token=None")

    ip, port, message = items

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(message)

    try:
        content = bytearray()
        response = sock.recv(2048)

        while response != b"":
            content += response
            response = sock.recv(2048)

        print("Content Length:", len(content))

        sock.close()
    finally:
        sock.close()
        # break

    print "Socket Client Complete."

    """
    raw_object = pickle.loads(tmp)
    # print "Fetching a request from", url

    feature_vectors = g2(raw_object)
    # print str(feature_vectors)

    # Push content
    push_feature_to_repo(url, feature_vectors)
    """
if __name__ == '__main__':
    main(sys.argv[1:])
