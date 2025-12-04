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
    Crea nodos agrupando eventos cercanos en tiempo y espacio (OPTIMIZADO)
    """
    events = {}
    processed = set()
    
    total_events = lt.size(catalog)
    print(f"Procesando {total_events} eventos...")
    
    for i in range(total_events):
        if i % 1000 == 0 and i > 0:
            print(f"Procesado: {i}/{total_events} eventos, {len(events)} nodos creados")
        
        record = lt.get_element(catalog, i)
        record_id = record["id"]
        
        if record_id in processed:
            continue
        
        # Buscar en nodos EXISTENTES si cabe (no en todos los eventos)
        found_node = False
        for node_id, node_info in events.items():
            location = ef.haversine(record["lat"], record["lon"], node_info["lat"], node_info["lon"])
            time = ef.calc_time_diff(record["timestamp"], node_info["timestamp"])
            
            if location <= 3 and time <= 3:
                # Agregar a nodo existente
                lt.add_last(node_info["events"], record)
                node_info["events_count"] += 1
                node_info["water_sum"] += record["comments"]
                node_info["water_count"] += 1
                if record["tag-local-identifier"] not in node_info["tag-identifiers"]:
                    node_info["tag-identifiers"].append(record["tag-local-identifier"])
                node_info["events_sorted"].append(record)
                processed.add(record_id)
                found_node = True
                break
        
        if not found_node:
            # Crear nuevo nodo
            event = {
                "lat": record["lat"],
                "lon": record["lon"],
                "timestamp": record["timestamp"],
                "events": lt.new_list(),
                "events_count": 1,
                "water_sum": record["comments"],
                "water_count": 1,
                "tag-identifiers": [record["tag-local-identifier"]],
                "id": record["id"],
                "events_sorted": [record]
            }
            lt.add_last(event["events"], record)
            processed.add(record_id)
            events[event["id"]] = event
    
    # Calcular distancia promedio al agua
    for node_id, node_info in events.items():
        node_info["water"] = node_info["water_sum"] / node_info["water_count"]
        node_info["events_sorted"].sort(key=lambda d: d["timestamp"])
    
    print(f"Total de nodos creados: {len(events)}")
    return events


def load_data(catalog, filename):
    """
    Carga los datos y construye los dos grafos (OPTIMIZADO)
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
            "comments": float(file["comments"]) / 1000,
            "timestamp": file["timestamp"],
            "id": file["event-id"]
        }
        lt.add_last(list_files, file_dict)
        cranes_set.add(file["tag-local-identifier"])
    
    total_events = lt.size(list_files)
    print(f"Total de eventos cargados: {total_events}")
    print(f"Total de grullas: {len(cranes_set)}")
    
    # Ordenar por timestamp (más rápido con lista Python)
    print("Ordenando eventos por timestamp....")
    events_list = []
    for i in range(total_events):
        events_list.append(lt.get_element(list_files, i))
    events_list.sort(key=lambda x: x["timestamp"])
    
    list_files_sorted = lt.new_list()
    for event in events_list:
        lt.add_last(list_files_sorted, event)
    
    print("Creando nodos (puntos migratorios)....")
    points = create_event_catalog(list_files_sorted)
    
    # Crear mapeo de evento -> nodo (más rápido)
    print("Creando mapeo evento -> nodo....")
    event_to_node = {}
    for node_id, node_info in points.items():
        for event in node_info["events_sorted"]:
            event_to_node[event["id"]] = node_id
    
    # Organizar eventos por grulla (optimizado)
    print("Organizando eventos por grulla....")
    subjects_distance = {crane: [] for crane in cranes_set}
    
    for node_id, node_info in points.items():
        for event in node_info["events_sorted"]:
            crane_id = event["tag-local-identifier"]
            event_copy = {
                "id": event["id"],
                "timestamp": event["timestamp"],
                "node_id": node_id,
                "lat": node_info["lat"],
                "lon": node_info["lon"],
                "prom_distancia_agua": node_info["water"]
            }
            subjects_distance[crane_id].append(event_copy)
    
    # Ya están ordenados por timestamp al crear nodos
    
    # Crear grafos
    print("Creando grafos....")
    graph1 = graph.new_graph(len(points))
    graph2 = graph.new_graph(len(points))
    
    # Insertar vértices
    print("Insertando vertices....")
    for node_id, node_info in points.items():
        graph.insert_vertex(graph1, node_id, node_info)
        graph.insert_vertex(graph2, node_id, node_info)
    
    print(f"Vertices insertados: {graph.order(graph1)}")
    
    # Calcular arcos (optimizado)
    print("Calculando arcos....")
    edges_distance = {}
    edges_water = {}
    
    for crane_id, events in subjects_distance.items():
        if len(events) < 2:
            continue
        
        prev_node = None
        for event in events:
            current_node = event["node_id"]
            
            if prev_node and prev_node != current_node:
                # Calcular distancia
                prev_event = events[events.index(event) - 1]
                distance = ef.haversine(
                    prev_event["lat"], prev_event["lon"],
                    event["lat"], event["lon"]
                )
                
                edge_key = (prev_node, current_node)
                
                if edge_key not in edges_distance:
                    edges_distance[edge_key] = []
                edges_distance[edge_key].append(distance)
                
                if edge_key not in edges_water:
                    edges_water[edge_key] = []
                edges_water[edge_key].append(event["prom_distancia_agua"])
            
            prev_node = current_node
    
    # Agregar arcos
    print(f"Agregando {len(edges_distance)} arcos a grafo de distancias....")
    for (node_a, node_b), distances in edges_distance.items():
        avg_distance = sum(distances) / len(distances)
        graph.add_edge(graph1, node_a, node_b, avg_distance)
    
    print(f"Agregando {len(edges_water)} arcos a grafo hidrico....")
    for (node_a, node_b), water_dists in edges_water.items():
        avg_water = sum(water_dists) / len(water_dists)
        graph.add_edge(graph2, node_a, node_b, avg_water)
    
    end = get_time()
    print(f"\nTiempo total: {round(delta_time(start, end)/1000, 2)} segundos")
    
    # Preparar info para retornar
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
        "total_events": total_events
    }
    
    return {
        "catalog": catalog_result,
        "total_cranes": len(cranes_set),
        "total_events": total_events,
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
