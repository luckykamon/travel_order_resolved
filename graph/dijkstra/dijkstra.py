import sys
import datetime

sys.path.append('..')

from build.index import get_graph_routes
from build.index import parse_name_cities

import pandas as panda

def dijkstra(departure, destination, timestamp):

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

    return get_infos_from_parcours(graph_routes, result)

def get_infos_from_parcours(graph_routes, parcours):
    results = []
    for route_id in parcours["parcours"]:
        for route in graph_routes:
            if route["route_id"] == route_id:
                # Convertir des secondes en durée humaine
                # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
                # Changer le format de la date pour qu'elle soit plus lisible


                poids = datetime.timedelta(seconds=route["poids"])
                departure_time = datetime.timedelta(seconds=route["departure_time"])
                arrival_time = datetime.timedelta(seconds=route["arrival_time"]) + poids

                result = {
                    "route_id": route["route_id"],
                    "departure": parse_name_cities(route["departure"]),
                    "destination": parse_name_cities(route["destination"]),
                    "poids": str(poids),
                    "service_id": route["service_id"],
                    "departure_time": str(departure_time),
                    "arrival_time": str(arrival_time),
                    "trip_id": route["trip_id"],
                    "departure_stop_id": route["departure_stop_id"],
                    "arrival_stop_id": route["arrival_stop_id"],
                }
                results.append(result)
                break
    return results





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



