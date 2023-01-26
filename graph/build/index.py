import json
import random

import sys

sys.path.append("../")
from reformat.index import index as reformat_index

from tqdm import tqdm
import pandas as panda
import os


def index():
    delete_data()
    reformat_index()
    data = load_data()
    get_graph_routes(data)
    return "Build succeded"


def delete_data():
    if os.path.exists("../Project_data/graph/graph_routes.json"):
        os.remove("../Project_data/graph/graph_routes.json")
    if os.path.exists("../Project_data/data_sncf/pickle/agency.pkl"):
        os.remove("../Project_data/data_sncf/pickle/agency.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/calendar.pkl"):
        os.remove("../Project_data/data_sncf/pickle/calendar.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/calendar_dates.pkl"):
        os.remove("../Project_data/data_sncf/pickle/calendar_dates.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/routes.pkl"):
        os.remove("../Project_data/data_sncf/pickle/routes.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/routes_parses.pkl"):
        os.remove("../Project_data/data_sncf/pickle/routes_parses.pkl")
    if os.path.exists("../Project_data/data_sncf/routes_parses.csv"):
        os.remove("../Project_data/data_sncf/routes_parses.csv")
    if os.path.exists("../Project_data/data_sncf/pickle/stop_times.pkl"):
        os.remove("../Project_data/data_sncf/pickle/stop_times.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/stops.pkl"):
        os.remove("../Project_data/data_sncf/pickle/stops.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/transfers.pkl"):
        os.remove("../Project_data/data_sncf/pickle/transfers.pkl")
    if os.path.exists("../Project_data/data_sncf/pickle/trips.pkl"):
        os.remove("../Project_data/data_sncf/pickle/trips.pkl")
    if os.path.exists("../Project_data/data_sncf/all_city.txt"):
        os.remove("../Project_data/data_sncf/all_city.txt")


def get_graph_routes(data = None):
    if data is None:
        data = load_data()
    if not os.path.exists("../Project_data/graph/graph_routes.json"):
        print("graph_routes.json not found, creating it...")
        data_routes = data["routes_parses"].astype(str)
        graph = []
        for index, row in tqdm(data_routes.iterrows()):
            route_id = row["route_id"]
            route_long_name = row["route_long_name_parse"]
            if type(route_long_name) == str:
                route_long_name_split = route_long_name.split(";")
                if len(route_long_name_split) > 2:
                    for nb_arrete in range(len(route_long_name_split) - 1):
                        graph.append(
                            {"route_id": route_id + ";" + str(nb_arrete), "departure": route_long_name_split[nb_arrete], "destination": route_long_name_split[nb_arrete + 1],
                             "poids": random.random()})

        # write graph to json file
        with open("../Project_data/graph/graph_routes.json", "w") as outfile:
            json.dump(graph, outfile)
    else:
        print("graph_routes.json already exist")
        with open("../Project_data/graph/graph_routes.json", "r") as outfile:
            graph = json.load(outfile)

    return graph


def load_data():
    # compress data to pickle
    compress_data_to_pickle()

    # load all data from pickle
    agency = panda.read_pickle("../Project_data/data_sncf/pickle/agency.pkl")
    calendar = panda.read_pickle("../Project_data/data_sncf/pickle/calendar.pkl")
    calendar_dates = panda.read_pickle("../Project_data/data_sncf/pickle/calendar_dates.pkl")
    routes = panda.read_pickle("../Project_data/data_sncf/pickle/routes.pkl")
    routes_parses = panda.read_pickle("../Project_data/data_sncf/pickle/routes_parses.pkl")
    stop_times = panda.read_pickle("../Project_data/data_sncf/pickle/stop_times.pkl")
    stops = panda.read_pickle("../Project_data/data_sncf/pickle/stops.pkl")
    transfers = panda.read_pickle("../Project_data/data_sncf/pickle/transfers.pkl")
    trips = panda.read_pickle("../Project_data/data_sncf/pickle/trips.pkl")
    return {"agency": agency, "calendar": calendar, "calendar_dates": calendar_dates, "routes": routes, "routes_parses": routes_parses,
            "stop_times": stop_times, "stops": stops, "transfers": transfers, "trips": trips}


def compress_data_to_pickle():
    if not os.path.exists("../Project_data/data_sncf/pickle/agency.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/agency.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/agency.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/calendar.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/calendar.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/calendar.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/calendar_dates.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/calendar_dates.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/calendar_dates.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/routes.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/routes.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/routes.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/routes_parses.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/routes_parses.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/routes_parses.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/stop_times.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/stop_times.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/stop_times.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/stops.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/stops.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/stops.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/transfers.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/transfers.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/transfers.pkl")
    if not os.path.exists("../Project_data/data_sncf/pickle/trips.pkl"):
        data = panda.read_csv("../Project_data/data_sncf/trips.csv")
        data.to_pickle("../Project_data/data_sncf/pickle/trips.pkl")
