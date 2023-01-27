import pandas as panda
import re
# import unidecode


def index():
    data = panda.read_excel('../Project_data/data_sncf/routes_parses.xls')
    data_route_id = data['route_id']
    data_parse_route_long_name = data['parse_route_long_name']
    data_json = {}
    for i in range(len(data_route_id)):
        data_json[data_route_id[i]] = data_parse_route_long_name[i]
    data_to_add_column = panda.read_csv('../Project_data/data_sncf/routes.csv')
    data_to_add_column_route_id = data_to_add_column['route_id']
    for i in range(len(data_to_add_column_route_id)):
        data_reformat = data_json[data_to_add_column_route_id[i]]
        if type(data_reformat) == str:
            data_reformat_split = data_reformat.replace("/", ";").split(";")
            data_reformat_final = ""
            for j in range(len(data_reformat_split)):
                data_reformat_final += reformat_string(data_reformat_split[j])
                if j != len(data_reformat_split) - 1:
                    data_reformat_final += ";"
            data_to_add_column['route_long_name_parse'][i] = data_reformat_final
    data_to_add_column.to_csv('../Project_data/data_sncf/routes_parses.csv')
    all_city = []
    for i in range(len(data_to_add_column['route_long_name_parse'])):
        if type(data_to_add_column['route_long_name_parse'][i]) == str:
            all_city += data_to_add_column['route_long_name_parse'][i].split(";")
    # supprimer les doublons de all_city
    all_city = list(set(all_city))
    # trier par ordre alphabétique
    all_city.sort()
    # enregistrer all_city dans un fichier en txt et en revenant à la ligne à chaque élément
    with open('../Project_data/data_sncf/all_city.txt', 'w') as f:
        for city in all_city:
            f.write(city + "\n")
    return data_json


def reformat_string(string):
    string = string.replace(" ", "")  # supprime les espaces
    string = re.sub(r'[^\w\s]', '', string)  # supprime tous les caractères spéciaux
    string = string.lower()  # met tout en minuscules
    # string = unidecode.unidecode(string)  # supprime les accents
    string = string.replace("saint", "st")  # remplace saint par st
    return string
