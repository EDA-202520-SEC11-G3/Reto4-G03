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
    """
    Crea nodos agrupando eventos cercanos en tiempo y espacio
    """
    events = {}
    processed = set()  # Para trackear eventos ya procesados
    
    for i in range(lt.size(catalog)):
        record = lt.get_element(catalog, i)
        record_id = record["id"]
        
        # Si ya fue procesado, saltar
        if record_id in processed:
            continue
        
        # Crear nuevo evento/nodo
        event = {
            "lat": record["lat"],
            "lon": record["lon"],
            "timestamp": record["timestamp"],
            "events": lt.new_list(),
            "events_count": 1,
            "water_sum": record["comments"],
            "water_count": 1,
            "tag-identifiers": [record["tag-local-identifier"]]
        }
        lt.add_last(event["events"], record)
        processed.add(record_id)
        
        # Buscar eventos cercanos
        for j in range(lt.size(catalog)):
            record2 = lt.get_element(catalog, j)
            record2_id = record2["id"]
            
            if record2_id not in processed:
                location = ef.haversine(record["lat"], record["lon"], record2["lat"], record2["lon"])
                time = ef.calc_time_diff(record["timestamp"], record2["timestamp"])
                
                if location <= 3 and time <= 3:
                    lt.add_last(event["events"], record2)
                    event["events_count"] += 1
                    event["water_sum"] += record2["comments"]
                    event["water_count"] += 1
                    if record2["tag-local-identifier"] not in event["tag-identifiers"]:
                        event["tag-identifiers"].append(record2["tag-local-identifier"])
                    processed.add(record2_id)
        
        # Ordenar eventos por timestamp
        events_list = []
        for k in range(lt.size(event["events"])):
            events_list.append(lt.get_element(event["events"], k))
        events_list.sort(key=lambda d: d["timestamp"])
        
        # ID del evento es el primer evento (más antiguo)
        event["id"] = events_list[0]["id"]
        event["water"] = event["water_sum"] / event["water_count"]
        event["events_sorted"] = events_list
        events[event["id"]] = event
    
    return events


def load_data(catalog, filename):
    """
    Carga los datos y construye los dos grafos
    """
    start = get_time()
    data_files = csv.DictReader(open(data_dir + filename, encoding='utf-8'))
    list_files = lt.new_list()
    cranes_set = set()
    
    print("Leyendo archivo CSV....")
    for file in data_files:
        file_dict = {
            "tag-local-identifier": file["tag-local-identifier"],
            "lat": float(file["location-lat"]),
            "lon": float(file["location-long"]),
            "comments": float(file["comments"]) / 1000,  # Convertir a km
            "timestamp": file["timestamp"],
            "id": file["event-id"]
        }
        lt.add_last(list_files, file_dict)
        cranes_set.add(file["tag-local-identifier"])
    
    print(f"Total de eventos cargados: {lt.size(list_files)}")
    print(f"Total de grullas: {len(cranes_set)}")
    
    # Ordenar por timestamp
    print("Ordenando eventos por timestamp....")
    events_list = []
    for i in range(lt.size(list_files)):
        events_list.append(lt.get_element(list_files, i))
    events_list.sort(key=lambda x: x["timestamp"])
    
    # Recrear lista ordenada
    list_files_sorted = lt.new_list()
    for event in events_list:
        lt.add_last(list_files_sorted, event)
    
    print("Creando nodos (puntos migratorios)....")
    points = create_event_catalog(list_files_sorted)
    print(f"Total de nodos creados: {len(points)}")
    
    # Crear mapeo de evento -> nodo
    event_to_node = {}
    for node_id, node_info in points.items():
        for event in node_info["events_sorted"]:
            event_to_node[event["id"]] = node_id
    
    # Organizar eventos por grulla
    print("Organizando eventos por grulla....")
    subjects_distance = {}
    for node_id, node_info in points.items():
        for event in node_info["events_sorted"]:
            crane_id = event["tag-local-identifier"]
            event_copy = event.copy()
            event_copy["node_id"] = node_id
            event_copy["prom_distancia_agua"] = node_info["water"]
            
            if crane_id not in subjects_distance:
                subjects_distance[crane_id] = []
            subjects_distance[crane_id].append(event_copy)
    
    # Asegurar que estén ordenados por timestamp
    for subject in subjects_distance.keys():
        subjects_distance[subject].sort(key=lambda d: d["timestamp"])
    
    # Crear grafos
    print("Creando grafos....")
    graph1 = graph.new_graph(10000)  # Grafo de distancias
    graph2 = graph.new_graph(10000)  # Grafo hídrico
    
    # Insertar vértices
    print("Insertando vertices....")
    for node_id, node_info in points.items():
        graph.insert_vertex(graph1, node_id, node_info)
        graph.insert_vertex(graph2, node_id, node_info)
    
    print(f"Vertices insertados: {graph.order(graph1)}")
    
    # Calcular arcos
    print("Calculando arcos....")
    edges_distance = {}  # {(node_a, node_b): [distancias]}
    edges_water = {}     # {(node_a, node_b): [distancias_agua]}
    
    for crane_id, events in subjects_distance.items():
        prev_node = None
        
        for event in events:
            current_node = event["node_id"]
            
            # Si cambió de nodo, registrar viaje
            if prev_node and prev_node != current_node:
                # Obtener información de los nodos
                prev_node_info = points[prev_node]
                curr_node_info = points[current_node]
                
                # Calcular distancia geográfica
                distance = ef.haversine(
                    prev_node_info["lat"], prev_node_info["lon"],
                    curr_node_info["lat"], curr_node_info["lon"]
                )
                
                # Registrar para grafo de distancias
                edge_key = (prev_node, current_node)
                if edge_key not in edges_distance:
                    edges_distance[edge_key] = []
                edges_distance[edge_key].append(distance)
                
                # Registrar para grafo hídrico (distancia promedio al agua del destino)
                if edge_key not in edges_water:
                    edges_water[edge_key] = []
                edges_water[edge_key].append(curr_node_info["water"])
            
            prev_node = current_node
    
    # Agregar arcos a los grafos
    print("Agregando arcos a grafo de distancias....")
    for (node_a, node_b), distances in edges_distance.items():
        avg_distance = sum(distances) / len(distances)
        if graph.contains_vertex(graph1, node_a) and graph.contains_vertex(graph1, node_b):
            graph.add_edge(graph1, node_a, node_b, avg_distance)
    
    print(f"Arcos en grafo de distancias: {graph.size(graph1)}")
    
    print("Agregando arcos a grafo hidrico....")
    for (node_a, node_b), water_dists in edges_water.items():
        avg_water = sum(water_dists) / len(water_dists)
        if graph.contains_vertex(graph2, node_a) and graph.contains_vertex(graph2, node_b):
            graph.add_edge(graph2, node_a, node_b, avg_water)
    
    print(f"Arcos en grafo hidrico: {graph.size(graph2)}")
    
    end = get_time()
    print(f"\nTiempo total de carga: {round(delta_time(start, end)/1000, 2)} segundos")
    
    # Preparar información para retornar
    nodes_list = list(points.keys())
    first_5 = []
    last_5 = []
    
    for i in range(min(5, len(nodes_list))):
        node_id = nodes_list[i]
        node = points[node_id]
        first_5.append({
            "id": node_id,
            "lat": round(node["lat"], 6),
            "lon": round(node["lon"], 6),
            "timestamp": node["timestamp"],
            "grullas": ", ".join(node["tag-identifiers"]),
            "eventos": node["events_count"]
        })
    
    for i in range(max(0, len(nodes_list) - 5), len(nodes_list)):
        node_id = nodes_list[i]
        node = points[node_id]
        last_5.append({
            "id": node_id,
            "lat": round(node["lat"], 6),
            "lon": round(node["lon"], 6),
            "timestamp": node["timestamp"],
            "grullas": ", ".join(node["tag-identifiers"]),
            "eventos": node["events_count"]
        })
    
    catalog_result = {
        "graph_distance": graph1,
        "graph_water": graph2,
        "nodes": points,
        "cranes": cranes_set,
        "event_to_node": event_to_node,
        "total_events": lt.size(list_files)
    }
    
    return {
        "catalog": catalog_result,
        "total_cranes": len(cranes_set),
        "total_events": lt.size(list_files),
        "total_nodes": len(points),
        "total_edges_distance": graph.size(graph1),
        "total_edges_water": graph.size(graph2),
        "first_5_nodes": first_5,
        "last_5_nodes": last_5
    }





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
