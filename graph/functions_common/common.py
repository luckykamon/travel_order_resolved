import pandas as panda
import os
from tqdm import tqdm


def common_f(departure, destination, timestamp):
    data = load_data()

    # On va récupérer les données des stops là où la gare à le même nom que la gare de départ
    df_filtered = get_stops_from_gare_departure(data, departure)

    if df_filtered is None:
        return None

    # On va récupérer la liste des stop_times qui contiennent au moins un stop_id de la liste passée en paramètre
    value_stop_times = get_list_stop_times_from_list_stop_id(data, df_filtered["stop_id"])

    print(type(value_stop_times))

    # On va récupérer les éléments associés à chacun des stop_times qui sont situés dans les fichiers trips, routes, calendar & calendar_dates
    # trips_from_value_stip_times = get_trips_from_value_stip_times(data, value_stop_times)
    # La fonction ci-dessus est beaucoup trop lente, il faudrait faire ce travail en amont et stocker les résultats dans un fichier pickle
    create_csv_of_stop_times_with_infos_match_with_stop_id(data)

    json_list = []
    for df in value_stop_times:
        json_list.append(df.to_json())

    # print(json_list)

    return json_list


def create_csv_of_stop_times_with_infos_match_with_stop_id(data):
    data_stop_times = data["stop_times"].astype(str)
    data_trips = data["trips"].astype(str)

    i = 0
    trips_list = []
    for index_stop_times, row_stop_times in tqdm(data_stop_times.iterrows()):
        i += 1

        trip_id = row_stop_times["trip_id"]
        trips = get_trips_from_trip_id(data, trip_id)

        index_trips = trips.index[0]

        stop_id = row_stop_times["stop_id"]
        trips.at[index_trips, "stop_id"] = stop_id



        for index_trips, row_trips in trips.iterrows():

            route_id = row_trips['route_id']
            routes = get_routes_from_route_id(data, route_id)
            for index_route, row_route in routes.iterrows():
                for index_row_route in row_route.index:
                    trips.at[index_trips, index_row_route] = row_route[index_row_route]
                break

            service_id = row_trips['service_id']
            calendar = get_calendar_from_service_id_id(data, service_id)
            for index_calendar, row_calendar in calendar.iterrows():
                for index_row_calendar in row_calendar.index:
                    trips.at[index_trips, index_row_calendar] = row_calendar[index_row_calendar]
                break

            calendar_dates = get_calendar_dates_from_service_id_id(data, service_id)
            for index_calendar_dates, row_calendar_dates in calendar_dates.iterrows():
                for index_row_calendar_dates in row_calendar_dates.index:
                    trips.at[index_trips, index_row_calendar_dates] = row_calendar_dates[index_row_calendar_dates]
                break

            break

        trips_list.append(trips)
        # if i == 10:
        #     break
    if (len(trips_list) > 0):
        trips_to_csv = panda.concat(trips_list, ignore_index=True)
        panda.DataFrame(trips_to_csv).to_csv("../Project_data/data_sncf/build_csv/stop_times_with_infos_match_with_stop_id.csv")


def get_calendar_dates_from_service_id_id(data, service_id):
    data_calendar_dates = data["calendar_dates"].astype(str)
    df_filtered = data_calendar_dates[data_calendar_dates["service_id"].str.contains(service_id, case=False)]
    return df_filtered

def get_calendar_from_service_id_id(data, service_id):
    data_calendar = data["calendar"].astype(str)
    df_filtered = data_calendar[data_calendar["service_id"].str.contains(service_id, case=False)]
    return df_filtered

def get_routes_from_route_id(data, value_route_id):
    data_routes = data["routes"].astype(str)
    df_filtered = data_routes[data_routes["route_id"].str.contains(value_route_id, case=False)]
    return df_filtered

def get_trips_from_value_stip_times(data, value_stop_times):
    trips_list_list = []
    for value_stop_time in tqdm(value_stop_times):
        trips_list = []
        for element in tqdm(value_stop_time["trip_id"]):
            trips_list.append(get_trips_from_trip_id(data, element))
        trips_list_list.append(trips_list)
    return trips_list_list


def get_trips_from_trip_id(data, trip_id):
    data_trips = data["trips"].astype(str)
    df_filtered = data_trips[data_trips["trip_id"].str.contains(trip_id, case=False)]
    return df_filtered
    # trips_list = []
    # for element_id in range(len(data_trips)):
    #     print(element_id)
    #     if data_trips["trip_id"][element_id] == trip_id_to_find:
    #         trips_list.append(data_trips[element_id])
    # return trips_list


def get_stops_from_gare_departure(data, gare_departure):
    data_stops = data["stops"].astype(str)
    df_filtered = data_stops[data_stops["stop_name"].str.contains(gare_departure, case=False)]
    # Si df_filtered est vide, alors on renvoie None
    if df_filtered.empty:
        return None
    return df_filtered


def get_list_stop_times_from_list_stop_id(data, list_stop_id):
    data_stop_times = data["stop_times"].astype(str)

    list_df_filtered = []
    for stop_id in list_stop_id:
        df_filtered = data_stop_times[data_stop_times["stop_id"].str.contains(stop_id, case=False)]
        if not df_filtered.empty:
            list_df_filtered.append(df_filtered)
    return list_df_filtered


def load_data():
    # compress data to pickle
    compress_data_to_pickle()

    # load all data from pickle
    agency = panda.read_pickle("../Project_data/data_sncf/pickle/agency.pkl")
    calendar = panda.read_pickle("../Project_data/data_sncf/pickle/calendar.pkl")
    calendar_dates = panda.read_pickle("../Project_data/data_sncf/pickle/calendar_dates.pkl")
    routes = panda.read_pickle("../Project_data/data_sncf/pickle/routes.pkl")
    stop_times = panda.read_pickle("../Project_data/data_sncf/pickle/stop_times.pkl")
    stops = panda.read_pickle("../Project_data/data_sncf/pickle/stops.pkl")
    transfers = panda.read_pickle("../Project_data/data_sncf/pickle/transfers.pkl")
    trips = panda.read_pickle("../Project_data/data_sncf/pickle/trips.pkl")
    return {"agency": agency, "calendar": calendar, "calendar_dates": calendar_dates, "routes": routes,
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
