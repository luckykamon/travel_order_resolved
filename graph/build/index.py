import json
import sys
import datetime
from tqdm import tqdm
import pandas as panda
import os
import difflib


sys.path.append("../")
from reformat.index import index as reformat_index
from reformat.index import reformat_string

new_tab= []


def index():
    # delete_data()
    reformat_index()
    stop_times_with_stop_name()
    data = load_data()
    get_graph_routes(data)
    save_changes_stop_times_parses()
    apply_changes_stop_times_parses()

    # test_parse_name_cities(data)

    return "Build succeded"


def test_parse_name_cities(data):
    data_stop_times_parses = data["stop_times_parses"]
    # Execute the function parse_name_cities on all the cities in the column "stop_name"
    data_stop_times_parses["stop_name_parsed"] = data_stop_times_parses["stop_name"].apply(lambda x: parse_name_cities(x))
    # Print the result of all stop_name_parsed
    print(data_stop_times_parses["stop_name_parsed"])

def parse_name_cities(city):
    data_cities = load_data()["cities"]

    city_index = data_cities[data_cities["city"] == city].index.tolist()

    if len(city_index) == 0:
        city_index = data_cities[data_cities["city_bis"] == city].index.tolist()
    if len(city_index) == 0:
        city_index = data_cities[data_cities["city_nospace"] == city].index.tolist()
    if len(city_index) == 0:
        city_index = data_cities[data_cities["city_nospace_bis"] == city].index.tolist()


    if len(city_index) == 0:
        print("city not found: " + city)
        return city

    return data_cities.iloc[city_index[0]]["city_formatted"]

def get_graph_routes(data=None):
    if data is None:
        data = load_data()
    if not os.path.exists("../Project_data/graph/graph_routes.json"):
        print("graph_routes.json not found, creating it...")
        data_routes = data["routes_parses"].astype(str)
        graph = []
        nb_success = 0
        nb_fail = 0
        for index, row in tqdm(data_routes.iterrows()):
            route_id = row["route_id"]
            route_long_name = row["route_long_name_parse"]
            if type(route_long_name) == str:
                route_long_name_split = route_long_name.split(";")
                if len(route_long_name_split) >= 2:
                    for nb_arrete in range(len(route_long_name_split) - 1):

                        # Calcul du poids
                        trips = get_trips_from_route_id(data, route_id)
                        min_duration = None
                        element_to_graph = None
                        for index_trip, row_trip in trips.iterrows():
                            trip_id = row_trip["trip_id"]
                            service_id = row_trip["service_id"]
                            duration_infos = get_duration_timestamp_from_trip_id_with_departure_arrival(data, trip_id, route_long_name_split[nb_arrete], route_long_name_split[nb_arrete + 1])
                            if duration_infos != None:
                                duration = abs(duration_infos["arrival_sec"] - duration_infos["departure_sec"])
                                change_element_to_graph = False
                                if min_duration == None:
                                    change_element_to_graph = True
                                elif duration < min_duration:
                                    change_element_to_graph = True
                                if change_element_to_graph:
                                    min_duration = duration
                                    element_to_graph = {"route_id": route_id + ";" + str(nb_arrete), "departure": route_long_name_split[nb_arrete], "destination": route_long_name_split[nb_arrete + 1], "service_id": service_id, "poids": duration, "departure_time": duration_infos["departure_sec"], "arrival_time": duration_infos["departure_sec"], "trip_id": trip_id, "departure_stop_id": duration_infos["departure_stop_id"], "arrival_stop_id": duration_infos["arrival_stop_id"]}

                        if element_to_graph != None:
                            nb_success += 1
                            graph.append(element_to_graph)
                        else:
                            nb_fail += 1
                            print("No duration found for route_id: " + route_id + " and nb_arrete: " + str(nb_arrete) + " and departure: " + route_long_name_split[nb_arrete] + " and destination: " + route_long_name_split[nb_arrete + 1])

            # if len(graph) >= 3:
            #     break
        print("nb_success: " + str(nb_success) + " and nb_fail: " + str(nb_fail))
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


def is_available_a_day_from_service_id(data, service_id, timestamp_day):
    # day in timestamp
    calendar = get_day_from_calendar(data, service_id)
    if calendar.empty:
        return True
    else:
        datetime_day = datetime.datetime.fromtimestamp(timestamp_day).date()
        for i in range(len(calendar)):
            start_date = convert_date_from_calendar(str(calendar.iloc[i]["start_date"]))
            end_date = convert_date_from_calendar(str(calendar.iloc[i]["end_date"]))
            if start_date <= datetime_day <= end_date:
                if calendar.iloc[i][datetime_day.strftime("%A").lower()] == 1:
                    return True
        return False

def get_day_from_calendar(data, service_id):
    calendar = data["calendar"]
    calendar = calendar[calendar["service_id"] == service_id]
    return calendar

def convert_date_from_calendar(date):
    return datetime.datetime.strptime(date, "%Y%m%d").date()


def get_stop_times_from_trip_id(data, trip_id):
    stop_times = data["stop_times_parses"]
    stop_times = stop_times[stop_times["trip_id"] == trip_id]
    return stop_times


def get_duration_timestamp_from_trip_id_with_departure_arrival(data, trip_id, departure, arrival):
    stop_times = get_stop_times_from_trip_id(data, trip_id)
    # departure_sec = None
    # arrival_sec = None
    # departure_stop_id = None
    # arrival_stop_id = None
    ratio_departure = []
    ratio_arrival = []
    for i in range(len(stop_times)):
        stop_time = stop_times.iloc[i]
        if type(stop_time["stop_name"]) != str or type(departure) != str or type(arrival) != str:
            continue
        ratio_departure.append(difflib.SequenceMatcher(None, stop_time["stop_name"], departure).ratio())
        ratio_arrival.append(difflib.SequenceMatcher(None, stop_time["stop_name"], arrival).ratio())
        # if difflib.SequenceMatcher(None, stop_time["stop_name"], departure).ratio() >= 0.5:
        #     departure_sec = time_to_seconds(stop_time["departure_time"])
        #     departure_stop_id = stop_time["stop_id"]
        # if difflib.SequenceMatcher(None, stop_time["stop_name"],arrival).ratio() >= 0.5:
        #     arrival_sec = time_to_seconds(stop_time["arrival_time"])
        #     arrival_stop_id = stop_time["stop_id"]
    # get index of the max ratio
    index_departure = ratio_departure.index(max(ratio_departure))
    index_arrival = ratio_arrival.index(max(ratio_arrival))
    # check if the index is the same
    if index_departure == index_arrival:
        return None
    else:
        stop_times_departure = stop_times.iloc[index_departure]
        stop_times_arrival = stop_times.iloc[index_arrival]
        # On met à jour le fichier stop_times_parses avec le nom de l'arrêt
        change_stop_name_from_stop_id_and_ratio(stop_times_departure["stop_id"], departure, ratio_departure[index_departure])
        change_stop_name_from_stop_id_and_ratio(stop_times_arrival["stop_id"], arrival, ratio_arrival[index_arrival])
        # On récupère les bonnes données
        departure_sec = time_to_seconds(stop_times_departure["departure_time"])
        arrival_sec = time_to_seconds(stop_times_arrival["arrival_time"])
        departure_stop_id = stop_times_departure["stop_id"]
        arrival_stop_id = stop_times_arrival["stop_id"]
        return {"departure_sec": departure_sec, "arrival_sec": arrival_sec, "departure_stop_id": departure_stop_id, "arrival_stop_id": arrival_stop_id}
    # if departure_sec is None or arrival_sec is None:
    #     return None
    # else:
    #     return {"departure_sec": departure_sec, "arrival_sec": arrival_sec, "departure_stop_id": departure_stop_id, "arrival_stop_id": arrival_stop_id}


def time_to_seconds(time):
    h, m, s = time.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def change_stop_name_from_stop_id_and_ratio(stop_id, new_stop_name, ratio):
    # file_path = "../Project_data/data_sncf/changes_stop_times_parses.json"
    json_to_add = {"stop_id": stop_id, "stop_name": new_stop_name, "ratio": ratio}
    # if os.path.exists(file_path):
    #     with open(file_path, "r") as f:
    #         tab = json.load(f)
    is_json_to_add_in_tab = False
    for i in range(len(new_tab)):
        if new_tab[i]["stop_id"] == stop_id:
            if new_tab[i]["ratio"] < ratio:
                new_tab[i] = json_to_add
                break
            is_json_to_add_in_tab = True
    if not is_json_to_add_in_tab:
        new_tab.append(json_to_add)
    #     with open(file_path, "w") as f:
    #         json.dump(new_tab, f)
    # else:
    #     with open(file_path, "w") as f:
    #         json.dump([json_to_add], f)


def save_changes_stop_times_parses():
    file_path = "../Project_data/data_sncf/changes_stop_times_parses.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump(new_tab, f)

def apply_changes_stop_times_parses():
    file_path = "../Project_data/data_sncf/changes_stop_times_parses.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            tab = json.load(f)
        data = load_data()
        data_stop_times_parses = data["stop_times_parses"]
        for i in range(len(tab)):
            # in data_stop_times_parses change the stop_name by tab[i]["stop_name"] with use pandas
            data_stop_times_parses.loc[data_stop_times_parses["stop_id"] == tab[i]["stop_id"], "stop_name"] = tab[i]["stop_name"]
        # save the data_stop_times_parses
        data_stop_times_parses.to_csv("../Project_data/data_sncf/stop_times_parses.csv", index=False)








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
        "cities": load_a_data("cities"),
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
    compress_one_data_to_pickle("cities")
    compress_one_data_to_pickle("routes")
    compress_one_data_to_pickle("routes_parses")
    compress_one_data_to_pickle("stop_times")
    compress_one_data_to_pickle("stop_times_parses")
    compress_one_data_to_pickle("stops")
    compress_one_data_to_pickle("transfers")
    compress_one_data_to_pickle("trips")
