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

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    fileSearch = data_dir + filename
    data_files = csv.DictReader(open(fileSearch, encoding='utf-8'))
    
    #Primero se lee el archivo csv para procesarlo como diccionarios,
    #luego se guardan en un array a modo de tupla (timestamp, record)
    #siendo record la información de cada diccionario 
    events = lt.new_list()
    for record in data_files:
        ts_str = record["timestamp"]
        ts = ts_str
        lt.add_last(events, (ts, row))
    # Las comparaciones alfabeticas funcionan para timestamps en formato dado
    # por tanto se puede ordenar directamente en base al string timestamp
    events["elements"].sort(key=lambda x: x[0])
    # Construir Vértices a partir de los Puntos Migratorios
    nodos_info = {}  # event_id -> dict de información del nodo
    event_to_node = {}  # event_id -> nodo_id, id para el nodo que se creo 
    
    for ts, record_data in events["elements"]:
        event_id = record_data["event-id"]
        lat, lon = float(record_data["location-lat"]), float(record_data["location-long"])
        tag = record_data["tag-local-identifier"]
        dist_agua = float(record_data["comments"]) / 1000 
        assigned = False
        # Buscar nodo existente
        for nid, ndata in nodos_info.items():
            d_dist = ef.haversine(lat, lon, ndata["lat"], ndata["lon"])
            # Diferencia temporal en horas (aprox por string)
            d_time = abs(int((ndata["creation_ts"] - ts).split()[0]) * 24 + 
                        int((ndata["creation_ts"].split()[1][:2] - ts.split()[1][:2])))
            
            if d_dist < 3 and d_time < 3:
                # Actualizar nodo EXISTENTE
                if tag not in ndata['tags']:
                    ndata['tags'].append(tag)
                ndata['events'].append(event_id)
                ndata['events_count'] += 1
                prev_count = ndata['events_count'] - 1
                ndata['prom_agua'] = (ndata['prom_agua'] * prev_count + dist_agua) / ndata['events_count']
                event_to_node[event_id] = nid
                assigned = True
                break
        
        if not assigned:
            # Nuevo nodo - POSICIÓN y TIEMPO FIJOS
            nodos_info[event_id] = {
                'lat': lat, 'lon': lon, 'creation_ts': ts,
                'tags': [tag], 'events': [event_id],
                'events_count': 1, 'prom_agua': dist_agua
            }
            event_to_node[event_id] = event_id
    
    # Insertar TODOS los nodos en AMBOS grafos
    grafo1, grafo2 = catalog  # Desplazamientos, Hídrica
    
    for node_id in nodos_info:
        graph.insert_vertex(grafo1, node_id, nodos_info[node_id])
        graph.insert_vertex(grafo2, node_id, nodos_info[node_id])
    
    # 2. Arcos GRAFO1 (desplazamientos promedio)
    viajes_dist = {}  # (src,dst) -> lista distancias
    tags_grullas = {}
    
    # Agrupar eventos por grulla
    for ts, row in events:
        event_id = row['event-id']
        tag = row['tag-local-identifier']
        if tag not in tags_grullas:
            tags_grullas[tag] = []
        tags_grullas[tag].append(event_id)
    
    for tag, event_list in tags_grullas.items():
        prev_node = None
        for event_id in event_list:
            curr_node = event_to_node[event_id]
            if prev_node and curr_node != prev_node:
                src_lat, src_lon = nodos_info[prev_node]['lat'], nodos_info[prev_node]['lon']
                dst_lat, dst_lon = nodos_info[curr_node]['lat'], nodos_info[curr_node]['lon']
                d = ef.haversine(src_lat, src_lon, dst_lat, dst_lon)
                
                key = (prev_node, curr_node)
                if key not in viajes_dist:
                    viajes_dist[key] = []
                viajes_dist[key].append(d)
            prev_node = curr_node
    
    # Agregar arcos grafo1
    for (src, dst), dists in viajes_dist.items():
        peso = sum(dists) / len(dists)
        graph.add_edge(grafo1, src, dst, peso)
    
    # 3. Arcos GRAFO2 (distancia agua destino promedio)
    viajes_hid = {}  # (src,dst) -> lista prom_agua_destino
    for tag, event_list in tags_grullas.items():
        prev_node = None
        for event_id in event_list:
            curr_node = event_to_node[event_id]
            if prev_node and curr_node != prev_node:
                peso_hid = nodos_info[curr_node]['prom_agua']
                
                key = (prev_node, curr_node)
                if key not in viajes_hid:
                    viajes_hid[key] = []
                viajes_hid[key].append(peso_hid)
            prev_node = curr_node
    
    # Agregar arcos grafo2
    for (src, dst), pesos in viajes_hid.items():
        peso = sum(pesos) / len(pesos)
        graph.add_edge(grafo2, src, dst, peso)
    
    # 4. Reporte Estadísticas
    grullas = len(tags_grullas)
    eventos_total = len(events)
    nodos_total = len(nodos_info)
    arcos1 = graph.size(grafo1)
    arcos2 = graph.size(grafo2)
    
    print(f"Grullas reconocidas: {grullas}")
    print(f"Eventos cargados: {eventos_total}")
    print(f"Nodos construidos: {nodos_total}")
    print(f"Arcos Grafo1 (desplazamientos): {arcos1}")
    print(f"Arcos Grafo2 (hídrica): {arcos2}")
    
    # Primeros y últimos 5 nodos por creation_ts
    nodos_ordenados = sorted(nodos_info.items(), key=lambda x: x[1]['creation_ts'])
    
    print("\n=== PRIMEROS 5 NODOS ===")
    for i, (nid, data) in enumerate(nodos_ordenados[:5]):
        print(f"Nodo {i+1}: ID={nid}, Pos=({data['lat']:.5f},{data['lon']:.5f}), "
              f"Fecha={data['creation_ts']}, Tags={data['tags']}, Events={data['events_count']}")
    
    print("\n=== ÚLTIMOS 5 NODOS ===")
    for i, (nid, data) in enumerate(nodos_ordenados[-5:]):
        print(f"Nodo {len(nodos_ordenados)-5+i+1}: ID={nid}, Pos=({data['lat']:.5f},{data['lon']:.5f}), "
              f"Fecha={data['creation_ts']}, Tags={data['tags']}, Events={data['events_count']}")
    
    return (grafo1, grafo2)

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
