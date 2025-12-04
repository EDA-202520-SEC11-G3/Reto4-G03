import time
import os
import csv
from DataStructures.Graph import digraph as graph
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as lp
from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as slt
from DataStructures.Queue import queue as q
from DataStructures.Stack import stack as st
from math import radians, sin, cos, sqrt, atan2, asin
from . import extra_functions as ef 

data_dir = os.path.dirname(os.path.realpath('__file__'))

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    return graph.new_graph(10000), graph.new_graph(10000)


# Funciones para la carga de datos

def create_event_catalog(catalog):
    events = {}
    for record in catalog["elements"]:
        event = {
            "lat": record["lat"],
            "lon": record["lon"],
            "timestamp": record["timestamp"],
            "events":lt.new_list(),
            "events_count": 1,
            "water": [record["comments"], 1]
        }
        lt.add_last(event["events"], record) 
        for record2 in catalog["elements"]:
            if record != record2:
                location = ef.haversine(record["lat"], record["lon"], record2["lat"], record2["lon"])
                time = ef.calc_time_diff(record["timestamp"], record2["timestamp"])
                if location <= 3 and time <= 3:
                        lt.add_last(event["events"], record2)
                        event["events_count"] += 1
                        event["water"][0] += record2["comments"]
                        event["water"][1] += 1
                        i = catalog["elements"].index(record2)
                        lt.delete_element(catalog["elements"], i)
        event["events"] = lt.selection_sort(event["events"], ef.cmp_timestamps)
        event["id"] = event["events"]["elements"][0]["id"]
        event["water"] = event["water"][0] / event["water"][1]
        events[event["id"]] = event
    return events
def load_data(catalog, filename):
    data_files = csv.DictReader(open(data_dir + filename, encoding='utf-8'))
    list_files = lt.new_list()
    for file in data_files:
        file_dict = {
            "tag-local-identifier": file["tag-local-identifier"],
            "lat": float(file["location-lat"]),
            "lon": float(file["location-long"]),
            "comments": int(file["comments"]), 
            "timestamp": file["timestamp"],
            "id": file["event-id"]
                          }
        lt.add_last(list_files, file_dict)
    for record in list_files["elements"]:
        for record2 in list_files["elements"]:
            if record != record2:
                distance = ef.haversine(record["lat"], record["lon"], record2["lat"], record2["lon"])





# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
