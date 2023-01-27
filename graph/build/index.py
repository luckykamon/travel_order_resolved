import json
import random
import sys
import datetime
from tqdm import tqdm
import pandas as panda
import os

sys.path.append("../")
from reformat.index import index as reformat_index
from reformat.index import reformat_string


def index():
    delete_data()
    reformat_index()
    stop_times_with_stop_name()
    data = load_data()
    get_graph_routes(data)
    return "Build succeded"


def get_graph_routes(data=None):
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
                            {"route_id": route_id + ";" + str(nb_arrete), "departure": route_long_name_split[nb_arrete],
                             "destination": route_long_name_split[nb_arrete + 1],
                             "poids": random.random()})

        # write graph to json file
        with open("../Project_data/graph/graph_routes.json", "w") as outfile:
            json.dump(graph, outfile)
    else:
        print("graph_routes.json already exist")
        with open("../Project_data/graph/graph_routes.json", "r") as outfile:
            graph = json.load(outfile)

    return graph


def get_trips_from_route_id(data, route_id):
    trips = data["trips"]
    trips = trips[trips["route_id"] == route_id]
    return trips


def get_day_from_calendar(data, service_id):
    calendar = data["calendar"]
    calendar = calendar[calendar["service_id"] == service_id]
    return calendar


def is_available_a_day_from_service_id(data, service_id, timestamp_day):
    # day in timestamp
    calendar = get_day_from_calendar(data, service_id)
    if calendar.empty:
        return False
    else:
        datetime_day = datetime.datetime.fromtimestamp(timestamp_day).date()
        for i in range(len(calendar)):
            start_date = convert_date_from_calendar(calendar.iloc[i]["start_date"])
            end_date = convert_date_from_calendar(calendar.iloc[i]["end_date"])
            if start_date <= datetime_day <= end_date:
                if calendar.iloc[i][datetime_day.strftime("%A").lower()] == 1:
                    return True
        return False


def convert_date_from_calendar(date):
    return datetime.datetime.strptime(date, "%Y%m%d").date()


def get_stop_times_from_trip_id(data, trip_id):
    stop_times = data["stop_times"]
    stop_times = stop_times[stop_times["trip_id"] == trip_id]
    return stop_times


def get_duration_timestamp_from_trip_id_with_departure_arrival(data, trip_id, departure, arrival):
    stop_times = get_stop_times_from_trip_id(data, trip_id)
    departure_sec = None
    arrival_sec = None
    for i in range(len(stop_times)):
        if stop_times[i]["stop_name"] == departure:
            departure_sec = time_to_seconds(stop_times[i]["departure_time"])
        if stop_times[i]["stop_name"] == arrival:
            arrival_sec = time_to_seconds(stop_times[i]["arrival_time"])
    if departure_sec is None or arrival_sec is None:
        return None
    else:
        return json.dumps({"departure_sec": departure_sec, "arrival_sec": arrival_sec})


def time_to_seconds(time):
    h, m, s = time.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


def removeGare(txt: str):
    if (type(txt) == str):
        txt = txt.lower()
        txt = txt.replace('"', '')

        if (txt.find("gare d") == 0):
            if txt.find("gare de ") == 0:
                txt = txt.replace("gare de ", "")
            elif txt.find("\"gare d'") == 0:
                txt = txt.replace("gare d'", "")
            else:
                print(f"Cannot find pattern in {txt}")
        txt = reformat_string(txt)
        return (txt)
    else:
        return (txt)

def stop_times_with_stop_name():
    file_path = "../Project_data/data_sncf/stop_times_parses.csv"
    if not os.path.exists(file_path):
        print("stop_times_parses.csv not found, creating it...")
        data = load_data()
        data_stops = data["stops"]
        data_stop_times = data["stop_times"]
        data_stop_times_parses = panda.merge(data_stop_times, data_stops[['stop_id', 'stop_name']], on='stop_id', how='left')
        # data_stop_times_parses = data_stop_times.merge(data_stops, on='stop_id')
        data_stop_times_parses['stop_name'] = data_stop_times_parses['stop_name'].apply(removeGare)
        data_stop_times_parses.to_csv(file_path, index=False)
    else:
        print("stop_times_parses.csv already exist")


def delete_one_data(path_file):
    if os.path.exists(path_file):
        os.remove(path_file)


def delete_data():
    delete_one_data("../Project_data/graph/graph_routes.json")
    delete_one_data("../Project_data/data_sncf/pickle/agency.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/calendar.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/calendar_dates.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/routes.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/routes_parses.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/stop_times.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/stop_times_parses.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/stops.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/transfers.pkl")
    delete_one_data("../Project_data/data_sncf/pickle/trips.pkl")
    delete_one_data("../Project_data/data_sncf/routes_parses.csv")
    delete_one_data("../Project_data/data_sncf/stop_times_parses.csv")


def load_a_data(name):
    if os.path.exists(f"../Project_data/data_sncf/pickle/{name}.pkl"):
        return panda.read_pickle(f"../Project_data/data_sncf/pickle/{name}.pkl")
    else:
        return None


def load_data():
    compress_data_to_pickle()
    return {
        "agency": load_a_data("agency"),
        "calendar": load_a_data("calendar"),
        "calendar_dates": load_a_data("calendar_dates"),
        "routes": load_a_data("routes"),
        "routes_parses": load_a_data("routes_parses"),
        "stop_times": load_a_data("stop_times"),
        "stop_times_parses": load_a_data("stop_times_parses"),
        "stops": load_a_data("stops"),
        "transfers": load_a_data("transfers"),
        "trips": load_a_data("trips")
    }


def compress_one_data_to_pickle(csv_name):
    if not os.path.exists("../Project_data/data_sncf/pickle/" + csv_name + ".pkl"):
        if not os.path.exists("../Project_data/data_sncf/" + csv_name + ".csv"):
            print("Error: " + csv_name + ".csv not found")
            return
        else:
            data = panda.read_csv("../Project_data/data_sncf/" + csv_name + ".csv")
            data.to_pickle("../Project_data/data_sncf/pickle/" + csv_name + ".pkl")


def compress_data_to_pickle():
    compress_one_data_to_pickle("agency")
    compress_one_data_to_pickle("calendar")
    compress_one_data_to_pickle("calendar_dates")
    compress_one_data_to_pickle("routes")
    compress_one_data_to_pickle("routes_parses")
    compress_one_data_to_pickle("stop_times")
    compress_one_data_to_pickle("stop_times_parses")
    compress_one_data_to_pickle("stops")
    compress_one_data_to_pickle("transfers")
    compress_one_data_to_pickle("trips")
