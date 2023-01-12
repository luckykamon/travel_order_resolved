import sys

sys.path.append('..')

from functions_common.common import common_f


def index(departure, destination, timestamp):
    result_common_f = common_f(departure, destination, timestamp)
    return result_common_f
