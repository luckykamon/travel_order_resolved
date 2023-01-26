import sys

import deprecation

import pandas as panda
from tqdm import tqdm

sys.path.append('..')

from build.index import get_graph_routes

def dijkstra(departure, destination, timestamp):
    # data = load_data()

    # On va créer un graph afin d'implémenter digistra à partir du fichier routes.csv
    # graph = create_graph_routes(data)

    # print("graph created")

    graph_routes = get_graph_routes()

    result = dijkstra_from_graph(graph_routes, departure, destination)

    # On va récupérer les données des stops là où la gare à le même nom que la gare de départ
    # df_filtered = get_stops_from_gare_departure(data, departure)
    #
    # if df_filtered is None:
    #     return None

    # On va récupérer la liste des stop_times qui contiennent au moins un stop_id de la liste passée en paramètre
    # value_stop_times = get_list_stop_times_from_list_stop_id(data, df_filtered["stop_id"])

    # print(type(value_stop_times))

    # On va récupérer les éléments associés à chacun des stop_times qui sont situés dans les fichiers trips, routes, calendar & calendar_dates
    # trips_from_value_stip_times = get_trips_from_value_stip_times(data, value_stop_times)
    # La fonction ci-dessus est beaucoup trop lente, il faudrait faire ce travail en amont et stocker les résultats dans un fichier pickle
    # create_csv_of_stop_times_with_infos_match_with_stop_id(data)

    # json_list = []
    # for df in value_stop_times:
    #     json_list.append(df.to_json())

    # print(json_list)

    if result is None:
        return "Pas de trajets trouvés"

    return result


# {
#     "voisins":
#         [
#             {"route_id": "route_id_1", "departure": "ville1", "destination": "villa1", "poids": 2},
#             {"route_id": "route_id_2", "departure": "ville2", "destination": "villa2", "poids": 1,
#              "voisins": [
#                     {"route_id": "route_id_3", "departure": "ville3", "destination": "villa3", "poids": 1},
#                     {"route_id": "route_id_4", "departure": "ville4", "destination": "villa4", "poids": 3}
#              ]},
#             {"route_id": "route_id_3", "departure": "ville3", "destination": "villa3", "poids": 4}
#         ]
#  }
# {"poids": voisin["poids"], "destination": voisin["destination"], "parcours": [voisin["route_id"]]}

def dijkstra_from_graph(graph_data, departure, destination):
    sommet_actuel = departure
    graph_dijkstra = {"voisins": get_voisins(graph_data, sommet_actuel, None)}
    chemin_dijkstra = get_chemin_dijkstra_initial(graph_dijkstra)

    i = 0

    while True:
        if len(chemin_dijkstra) == 0:
            break
        elif chemin_dijkstra[0]["destination"] == destination:
            print("Chemin trouvé")
            break

        graph_dijkstra, chemin_dijkstra = update_graph_and_chemin_dijkstra(graph_data, graph_dijkstra, chemin_dijkstra)

        i += 1
        if i == 100:
            break

    if len(chemin_dijkstra) == 0:
        return None
    else:
        return chemin_dijkstra[0]


def update_graph_and_chemin_dijkstra(graph_data, graph_dijkstra, chemin_dijkstra):
    if len(chemin_dijkstra) == 0:
        return graph_dijkstra, chemin_dijkstra
    # On va récupérer le chemin le plus court actuel qui est le premier car la liste est triée
    chemin_court_actuel = chemin_dijkstra[0]
    # On va récupérer la destination de ce chemin
    destination_chemin_court_actuel = chemin_court_actuel["destination"]
    # On va récupérer les voisins de la destination du chemin le plus court actuel
    voisins_destination_chemin_court_actuel = get_voisins(graph_data, destination_chemin_court_actuel, chemin_court_actuel["parcours"])
    # On va ajouter les voisins de la destination du chemin le plus court actuel au graph_dijkstra
    new_chemins = add_voisins_from_chemin(graph_dijkstra, chemin_court_actuel, voisins_destination_chemin_court_actuel)
    # Supprimer le premier element de la liste chemin_dijkstra
    chemin_dijkstra.pop(0)
    # Ajouter les nouveaux chemins au chemin_dijkstra
    if new_chemins is not None:
        for new_chemin in new_chemins:
            chemin_dijkstra = ajout_chemin_dijkstra(chemin_dijkstra, new_chemin)

    return graph_dijkstra, chemin_dijkstra


def add_voisins_from_chemin(graph_dijkstra, chemin, voisins, new_chemin=None):
    if new_chemin is None:
        new_chemin = {"poids": 0, "destination": "", "parcours": []}
    if "parcours" not in chemin:
        return None
    if len(chemin["parcours"]) == 0:
        return None
    for voisin in graph_dijkstra["voisins"]:
        if voisin["route_id"] == chemin["parcours"][0]:
            new_parcours = new_chemin["parcours"] + [chemin["parcours"][0]]
            new_poids = new_chemin["poids"] + voisin["poids"]
            new_destination = voisin["destination"]
            new_chemin = {"poids": new_poids, "destination": new_destination, "parcours": new_parcours}
            if len(chemin["parcours"]) == 1:
                voisin["voisins"] = voisins
                new_chemins = []
                for new_voisin in voisins:
                    new_chemins.append(
                        {"poids": new_chemin["poids"] + new_voisin["poids"], "destination": new_voisin["destination"],
                         "parcours": new_chemin["parcours"] + [new_voisin["route_id"]]})
                return new_chemins
            else:
                return add_voisins_from_chemin(voisin, chemin["parcours"][1:], voisins, new_chemin)

    graph_dijkstra_voisins = graph_dijkstra
    for route_id in chemin["parcours"]:
        new_graph_dijkstra_voisins = None
        for voisin in graph_dijkstra_voisins["voisins"]:
            if voisin["route_id"] == route_id:
                if "voisins" in voisin:
                    new_graph_dijkstra_voisins = voisin
                else:
                    graph_dijkstra_voisins["voisins"] = voisins
                break
        if new_graph_dijkstra_voisins is not None:
            graph_dijkstra_voisins = new_graph_dijkstra_voisins
        else:
            break


def get_chemin_dijkstra_initial(graph_dijkstra):
    chemin_dijkstra = []
    for voisin in graph_dijkstra["voisins"]:
        chemin_dijkstra = ajout_chemin_dijkstra(chemin_dijkstra,
                                                {"poids": voisin["poids"], "destination": voisin["destination"],
                                                 "parcours": [voisin["route_id"]]})
    return chemin_dijkstra


def ajout_chemin_dijkstra(chemin_dijkstra, element):
    # ajouter dans cette liste triée par poids
    chemin_dijkstra.append(element)
    return trie_chemin_dijkstra(chemin_dijkstra)


def trie_chemin_dijkstra(chemin_dijkstra):
    chemin_dijkstra.sort(key=lambda x: x["poids"])
    return chemin_dijkstra


def get_voisins(graph, sommet_actuel, exclude_route_id=None):
    return [voisin for voisin in graph if voisin["departure"] == sommet_actuel and (
                exclude_route_id is None or voisin["route_id"] not in exclude_route_id)]





# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def create_csv_of_stop_times_with_infos_match_with_stop_id(data):
#     data_stop_times = data["stop_times"].astype(str)
#     data_trips = data["trips"].astype(str)
#
#     i = 0
#     trips_list = []
#
#     data_stop_times__trip_id = None
#
#     data_stop_times__trip_id = data_stop_times.columns.get_loc("trip_id") + 1
#
#     for row in data_stop_times.itertuples():
#         print(row[data_stop_times__trip_id])
#         break
#
#     for index_stop_times, row_stop_times in tqdm(data_stop_times.iterrows()):
#         i += 1
#
#         trip_id = row_stop_times["trip_id"]
#         trips = get_trips_from_trip_id(data, trip_id)
#
#         index_trips = trips.index[0]
#
#         stop_id = row_stop_times["stop_id"]
#         trips.at[index_trips, "stop_id"] = stop_id
#
#         for index_trips, row_trips in trips.iterrows():
#
#             route_id = row_trips['route_id']
#             routes = get_routes_from_route_id(data, route_id)
#             for index_route, row_route in routes.iterrows():
#                 for index_row_route in row_route.index:
#                     trips.at[index_trips, index_row_route] = row_route[index_row_route]
#                 break
#
#             service_id = row_trips['service_id']
#             calendar = get_calendar_from_service_id_id(data, service_id)
#             for index_calendar, row_calendar in calendar.iterrows():
#                 for index_row_calendar in row_calendar.index:
#                     trips.at[index_trips, index_row_calendar] = row_calendar[index_row_calendar]
#                 break
#
#             calendar_dates = get_calendar_dates_from_service_id_id(data, service_id)
#             for index_calendar_dates, row_calendar_dates in calendar_dates.iterrows():
#                 for index_row_calendar_dates in row_calendar_dates.index:
#                     trips.at[index_trips, index_row_calendar_dates] = row_calendar_dates[index_row_calendar_dates]
#                 break
#
#             break
#
#         trips_list.append(trips)
#         # if i == 10:
#         #     break
#     if (len(trips_list) > 0):
#         trips_to_csv = panda.concat(trips_list, ignore_index=True)
#         panda.DataFrame(trips_to_csv).to_csv(
#             "../Project_data/data_sncf/build_csv/stop_times_with_infos_match_with_stop_id.csv")
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def index_column(data_frame, column_name):
#     return data_frame.columns.get_loc(column_name) + 1
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_calendar_dates_from_service_id_id(data, service_id):
#     data_calendar_dates = data["calendar_dates"].astype(str)
#     df_filtered = data_calendar_dates[data_calendar_dates["service_id"].str.contains(service_id, case=False)]
#     return df_filtered
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_calendar_from_service_id_id(data, service_id):
#     data_calendar = data["calendar"].astype(str)
#     df_filtered = data_calendar[data_calendar["service_id"].str.contains(service_id, case=False)]
#     return df_filtered
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_routes_from_route_id(data, value_route_id):
#     data_routes = data["routes"].astype(str)
#     df_filtered = data_routes[data_routes["route_id"].str.contains(value_route_id, case=False)]
#     return df_filtered
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_trips_from_value_stip_times(data, value_stop_times):
#     trips_list_list = []
#     for value_stop_time in tqdm(value_stop_times):
#         trips_list = []
#         for element in tqdm(value_stop_time["trip_id"]):
#             trips_list.append(get_trips_from_trip_id(data, element))
#         trips_list_list.append(trips_list)
#     return trips_list_list
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_trips_from_trip_id(data, trip_id):
#     data_trips = data["trips"].astype(str)
#     df_filtered = data_trips[data_trips["trip_id"].str.contains(trip_id, case=False)]
#     return df_filtered
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_stops_from_gare_departure(data, gare_departure):
#     data_stops = data["stops"].astype(str)
#     df_filtered = data_stops[data_stops["stop_name"].str.contains(gare_departure, case=False)]
#     # Si df_filtered est vide, alors on renvoie None
#     if df_filtered.empty:
#         return None
#     return df_filtered
#
#
# @deprecation.deprecated("Utilise le chemin 1 donné avec freeform")
# def get_list_stop_times_from_list_stop_id(data, list_stop_id):
#     data_stop_times = data["stop_times"].astype(str)
#
#     list_df_filtered = []
#     for stop_id in list_stop_id:
#         df_filtered = data_stop_times[data_stop_times["stop_id"].str.contains(stop_id, case=False)]
#         if not df_filtered.empty:
#             list_df_filtered.append(df_filtered)
#     return list_df_filtered
#
