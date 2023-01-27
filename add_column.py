#!/bin/python3

import math
import unidecode
import re
from tqdm import tqdm

def reformat_string(string):
    string = string.replace(" ", "")  # supprime les espaces
    string = re.sub(r'[^\w\s]', '', string)  # supprime tous les caractères spéciaux
    string = string.lower()  # met tout en minuscules
    string = unidecode.unidecode(string)  # supprime les accents
    string = string.replace("saint", "st")  # remplace saint par st
    return string

def removeGare(txt: str):
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


def init():
    stops = open("Project_data/data_sncf/stops.csv")
    stop_times = open("Project_data/data_sncf/stop_times.csv")
    stopsLines = stops.readlines()
    stop_timesLines = stop_times.readlines()
    stop_times.close()
    stops.close()
    return stopsLines, stop_timesLines

def add_column():
    test1 = open("Project_data/data_sncf/stops_parses.csv", "w")
    percent = -1
    stopLines, stop_timesLines = init()
    newStopTimesLines = stop_timesLines
    newStopTimesLines[0] = newStopTimesLines[0].replace("\n", "") + ",stop_name\n"
    test1.write(newStopTimesLines[0])
    for i in tqdm(range(1, len(stop_timesLines))):
        stop_timeID = stop_timesLines[i].split(',')[3]
        done = False
        for j in range(1, len(stopLines)):
            stopSplited = stopLines[j].split(",")
            stopID = stopSplited[0]
            if stop_timeID == stopID:
                done = True
                gareName = removeGare(stopSplited[1])
                newStopTimesLines[i] = newStopTimesLines[i].replace("\n", "") + f",{gareName}\n"
        if not done :
            print(f"KO for stop_timeID = {stop_timeID}")
        test1.write(newStopTimesLines[i])

if __name__ == "__main__":
    add_column()
