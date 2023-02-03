import sys
import datetime

sys.path.append('..')

from build.index import get_graph_routes
from build.index import parse_name_cities
from build.index import is_available_a_day_from_service_id
from build.index import load_data

import pandas as panda


def dijkstra(departure, destination, timestamp):
    # On va créer un graph afin d'implémenter digistra à partir du fichier routes.csv
    # graph = create_graph_routes(data)

    # print("graph created")

    graph_routes = get_graph_routes()

    # if timestamp is not None:
    #     list_service_id_not_available = []
    #     # On va récupérer les services_id qui sont disponibles à la date passée en paramètre
    #     for i in range(len(graph_routes)):
    #         service_id = graph_routes[i]["service_id"]
    #         services_id_is_available = is_available_a_day_from_service_id(load_data(), service_id, timestamp)
    #         if not services_id_is_available:
    #             list_service_id_not_available.append(service_id)
    #
    #     # On va supprimer les routes qui ne sont pas disponibles à la date passée en paramètre
    #     for service_id in list_service_id_not_available:
    #         for i in range(len(graph_routes)):
    #             if graph_routes[i]["service_id"] == service_id:
    #                 graph_routes.pop(i)
    #                 break

    result = dijkstra_from_graph(graph_routes, departure, destination, timestamp)

    if result is None:
        return "Pas de trajets trouvés"

    return humans_results(get_infos_from_parcours(graph_routes, result))


def get_infos_from_parcours(graph_routes, parcours):
    results = []
    for route_id in parcours["parcours"]:
        for route in graph_routes:
            if route["route_id"] == route_id:
                # Convertir des secondes en durée humaine
                # https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds
                # Changer le format de la date pour qu'elle soit plus lisible

                poids = datetime.timedelta(seconds=route["poids"])
                if (route["departure_time"] > route["arrival_time"]):
                    departure_time = datetime.timedelta(seconds=route["arrival_time"])
                    arrival_time = datetime.timedelta(seconds=route["departure_time"])
                else:
                    departure_time = datetime.timedelta(seconds=route["departure_time"])
                    arrival_time = datetime.timedelta(seconds=route["arrival_time"])

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

def inverse_timedelta_str(x):
    hours, minutes, seconds = map(int, x.split(":"))
    return hours * 3600 + minutes * 60 + seconds


def humans_results(results):
    total_duration = 0
    etapes = []
    duree_entre_deux_arrets = []
    index_result = 0
    for result in results:
        if index_result > 0:
            second_arrival_trajet_precedent = inverse_timedelta_str(results[index_result-1]["arrival_time"])
            second_depart_trajet_actuel = inverse_timedelta_str(result["departure_time"])
            if second_arrival_trajet_precedent > second_depart_trajet_actuel:
                duree_entre_deux_arrets.append(86400 - second_arrival_trajet_precedent + second_depart_trajet_actuel)
            else:
                duree_entre_deux_arrets.append(second_depart_trajet_actuel - second_arrival_trajet_precedent)
            total_duration += duree_entre_deux_arrets[index_result-1]
        total_duration += int(inverse_timedelta_str(result["poids"]))
        etapes.append(
            "Dans la ville " + result["departure"] + " aller à l'arrêt nommé " + result["departure_stop_id"] + " à " +
            result["departure_time"] + " patientez pendant " + result["poids"] + " et arriver à l'arrêt nommé " +
            result["arrival_stop_id"] + " à " + result["arrival_time"] + " dans la ville " + result[
                "destination"] + " où vous serez déposé à l'arrêt " + result["arrival_stop_id"] + ". \n")
        index_result += 1
    total_duration = datetime.timedelta(seconds=total_duration)
    humans_results = "Le trajets le plus court a une durée de " + str(total_duration) + ". \nIl est composé de " + str(
        len(results)) + " étapes. \n"
    for index_etape in range(len(etapes)):
        humans_results += etapes[index_etape]
        if index_etape < len(etapes) - 1:
            humans_results += "Pendant " + str(datetime.timedelta(seconds=duree_entre_deux_arrets[index_etape])) + " attendez le prochain train. \n"
    humans_results += "Vous êtes arrivé à destination !"
    print(duree_entre_deux_arrets)
    return humans_results

    # humans_results.append("")
    # print("route_id: ", result["route_id"])
    # print("departure: ", result["departure"])
    # print("destination: ", result["destination"])
    # print("poids: ", result["poids"])
    # print("service_id: ", result["service_id"])
    # print("departure_time: ", result["departure_time"])
    # print("arrival_time: ", result["arrival_time"])
    # print("trip_id: ", result["trip_id"])
    # print("departure_stop_id: ", result["departure_stop_id"])
    # print("arrival_stop_id: ", result["arrival_stop_id"])
    # print("")
    return humans_results


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

def dijkstra_from_graph(graph_data, departure, destination, timestamp):
    sommet_actuel = departure
    graph_dijkstra = {"voisins": get_voisins(graph_data, sommet_actuel, None)}
    chemin_dijkstra = get_chemin_dijkstra_initial(graph_dijkstra, timestamp, graph_data)

    i = 0

    while True:
        if len(chemin_dijkstra) == 0:
            break
        elif chemin_dijkstra[0]["destination"] == destination:
            print("Chemin trouvé")
            break

        graph_dijkstra, chemin_dijkstra = update_graph_and_chemin_dijkstra(graph_data, graph_dijkstra, chemin_dijkstra,
                                                                           timestamp)

        i += 1
        if i == 100:
            break

    if len(chemin_dijkstra) == 0:
        return None
    else:
        return chemin_dijkstra[0]


def update_graph_and_chemin_dijkstra(graph_data, graph_dijkstra, chemin_dijkstra, timestamp):
    if len(chemin_dijkstra) == 0:
        return graph_dijkstra, chemin_dijkstra
    # On va récupérer le chemin le plus court actuel qui est le premier car la liste est triée

    chemin_court_actuel = chemin_dijkstra[0]
    # On va récupérer la destination de ce chemin
    destination_chemin_court_actuel = chemin_court_actuel["destination"]
    # On va récupérer les voisins de la destination du chemin le plus court actuel
    voisins_destination_chemin_court_actuel = get_voisins(graph_data, destination_chemin_court_actuel,
                                                          chemin_court_actuel["parcours"])
    # On va ajouter les voisins de la destination du chemin le plus court actuel au graph_dijkstra
    new_chemins = add_voisins_from_chemin(graph_dijkstra, chemin_court_actuel, voisins_destination_chemin_court_actuel)
    # Supprimer le premier element de la liste chemin_dijkstra
    chemin_dijkstra.pop(0)
    # Ajouter les nouveaux chemins au chemin_dijkstra
    if new_chemins is not None:
        for new_chemin in new_chemins:
            chemin_dijkstra = ajout_chemin_dijkstra(chemin_dijkstra, new_chemin, timestamp, graph_data)

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


def get_chemin_dijkstra_initial(graph_dijkstra, timestamp, graph_data):
    chemin_dijkstra = []
    for voisin in graph_dijkstra["voisins"]:
        add_chemin_dijkstra = False
        if timestamp is not None:
            if is_available_a_day_from_service_id(load_data(), voisin["service_id"], timestamp):
                add_chemin_dijkstra = True
        else:
            add_chemin_dijkstra = True
        if add_chemin_dijkstra:
            chemin_dijkstra = ajout_chemin_dijkstra(chemin_dijkstra,
                                                    {"poids": voisin["poids"], "destination": voisin["destination"],
                                                     "parcours": [voisin["route_id"]]}, timestamp, graph_data)
    return chemin_dijkstra


def ajout_chemin_dijkstra(chemin_dijkstra, element, timestamp, graph_data):
    if is_available_a_day_from_parcours(graph_data, element["parcours"], timestamp):
        # ajouter dans cette liste triée par poids
        chemin_dijkstra.append(element)
        return trie_chemin_dijkstra(chemin_dijkstra)
    else:
        return chemin_dijkstra


def is_available_a_day_from_parcours(graph_data, parcours, timestamp):
    if timestamp is None:
        return True
    len_parcours = len(parcours)
    if len_parcours == 0:
        return True
    else:
        route_id = parcours[len_parcours - 1]
        # get the value in the graph_data where route_id == parcours[0]
        infos_parcours = list(filter(lambda x: x['route_id'] == route_id, graph_data))
        if len(infos_parcours) > 0:
            service_id = infos_parcours[0]["service_id"]
            return is_available_a_day_from_service_id(load_data(), service_id, timestamp)
    return True


def trie_chemin_dijkstra(chemin_dijkstra):
    chemin_dijkstra.sort(key=lambda x: x["poids"])
    return chemin_dijkstra


def get_voisins(graph, sommet_actuel, exclude_route_id=None):
    return [voisin for voisin in graph if voisin["departure"] == sommet_actuel and (
            exclude_route_id is None or voisin["route_id"] not in exclude_route_id)]
