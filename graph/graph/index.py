import sys

sys.path.append('..')

from dijkstra.dijkstra import dijkstra


def index(departure, destination, timestamp):
    result_dijkstra = dijkstra(departure, destination, timestamp)
    return result_dijkstra
