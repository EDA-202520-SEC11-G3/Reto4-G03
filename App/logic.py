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
from DataStructures.Graph import dijsktra as dij
from DataStructures.Graph import bfo as bfs
from DataStructures.Graph import dfs as dfs 
from math import radians, sin, cos, sqrt, atan2, asin
from . import extra_functions as ef 

csv.field_size_limit(2147483647)

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
                        lt.delete_element(catalog, i)
        event["events"]["elements"] = sorted(event["events"]["elements"], key=lambda d: d["timestamp"])
        event["id"] = event["events"]["elements"][0]["id"]
        event["water"] = event["water"][0] / event["water"][1]
        events[event["id"]] = event
    return events

def load_data(catalog, filename):
    start = get_time()
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
    print("Creando grafos....")
    points = create_event_catalog(list_files)
    subjects_distance = {}
    graph1 = graph.new_graph(10000)
    graph2 = graph.new_graph(10000)
    vertex = {}
    water = {}
    print("Insertando vértices...")
    for event in points:
         graph.insert_vertex(graph1, points[event]["id"], event)
         graph.insert_vertex(graph2, points[event]["id"], event)
         for info in points[event]["events"]["elements"]:
            if info["tag-local-identifier"] not in subjects_distance:
                info["prom_distancia_agua"] = points[event]["water"]
                subjects_distance[info["tag-local-identifier"]] = [info]
            else:
               info["prom_distancia_agua"] = points[event]["water"]
               subjects_distance[info["tag-local-identifier"]].append(info)

    for subject in subjects_distance.keys():
        subjects_distance[subject] = sorted(subjects_distance[subject], key=lambda d: d["timestamp"])
    
    for subject in subjects_distance:
        for index in range(len(subjects_distance[subject])):
            if index != 0:
                a = subjects_distance[subject][index]
                b = subjects_distance[subject][index-1]
                location = ef.haversine(a["lat"], a["lon"], b["lat"], b["lon"])
                time = ef.calc_time_diff(b["timestamp"], a["timestamp"])
                for point in points:
                    if b in points[point]["events"]["elements"]:
                        b["id"] = points[point]["id"]
                for point in points:
                    if a in points[point]["events"]["elements"]:
                        a["id"] = points[point]["id"]
                if location > 3 and time > 3:
                    if subject not in vertex:
                        vertex[subject] = {"node_1": b["id"],
                                            "node_2": a["id"],
                                            "distance": location,
                                            "total":1}
                    else:
                        vertex[subject]["distance"] += location
                        vertex[subject]["total"] += 1
                    if subject not in water:
                        water[subject] = {"node_1": b["id"],
                                            "node_2": a["id"],
                                            "water": b["prom_distancia_agua"]}
                    else:
                        water[subject]["water"] = b["prom_distancia_agua"]
    print("Añadiendo vertices...")
    for source in water:
        graph.add_edge(graph2, water[source]["node_2"], water[source]["node_1"], water[source]["water"])
    for trip in vertex:
        graph.add_edge(graph1, vertex[trip]["node_1"], vertex[trip]["node_2"], vertex[trip]["distance"]/vertex[trip]["total"])
    end = get_time()
    print(delta_time(start,end))
    return graph1, graph2, points





# Funciones de consulta sobre el catálogo


def req_1(catalog, initial_point, final_point, crane_id, graph_distance):
    origin_point = ef.find_nearest_migration_point(catalog, initial_point[0], initial_point[1])
    dest_point = ef.find_nearest_migration_point(catalog, final_point[0], final_point[1])
    
    if origin_point is None or dest_point is None:
        return {"mensaje": "No se encontraron puntos migratorios cercanos", "origen": "Desconocido", "destino": "Desconocido"}
    
    if not ef.crane_in_point(origin_point, crane_id):
        return {"mensaje": f"Grulla {crane_id} no encontrada en origen", "primer_nodo": origin_point["id"], "grulla": crane_id}
    
    search_result = dfs.dfs(graph_distance, origin_point["id"])
    if not ef.has_path_to(dest_point["id"], search_result):
        return {"mensaje": "No existe camino viable", "primer_nodo": origin_point["id"], "origen": origin_point["id"], "destino": dest_point["id"]}
    
    path_stack = ef.path_to(dest_point["id"], search_result)
    full_path = []
    total_distance = 0
    while not st.is_empty(path_stack):
        current_node = st.pop(path_stack)
        full_path.append(current_node)
    full_path.reverse()
    
    distances = [0]
    for i in range(1, len(full_path)):
        total_distance += ef.get_edge_weight(graph_distance, full_path[i-1], full_path[i]) or 0
        distances.append(total_distance)

    first_5 = full_path[:5]
    last_5 = full_path[-5:]

    first_details = ef.get_path_details(catalog, first_5, graph_distance, crane_id)
    last_details = ef.get_path_details(catalog, last_5, graph_distance, crane_id)
    
    return {"ruta_encontrada": True, 
            "primer_nodo": origin_point["id"], 
            "distancia_total": total_distance, 
            "total_puntos": len(full_path), 
            "primeros_5_puntos": first_details, 
            "ultimos_5_puntos": last_details, 
            "grulla": crane_id}


def req_2(catalog, initial_point, final_point, radius_km, graph_distance):
    origin_point = ef.find_nearest_migration_point(catalog, initial_point[0], initial_point[1])
    dest_point = ef.find_nearest_migration_point(catalog, final_point[0], final_point[1])
    if origin_point is None or dest_point is None:
        return {"mensaje": "No se encontraron puntos migratorios cercanos"}
    visited_map = bfs.bfs(graph_distance, origin_point["id"])
    if not ef.has_path_to(visited_map, dest_point["id"]):
        return {"mensaje": "No existe camino viable entre puntos", "origen": origin_point["id"], "destino": dest_point["id"]}
    path_stack = ef.path_to(visited_map, dest_point["id"])
    full_path = []
    total_distance = 0
    while not st.is_empty(path_stack):
        node_id = st.pop(path_stack)
        full_path.append(node_id)
    full_path.reverse()
    origin_lat, origin_lon = origin_point["lat"], origin_point["lon"]
    last_in_radius = origin_point["id"]
    for node_id in full_path:
        node = catalog.get(node_id)
        if node and ef.haversine(origin_lat, origin_lon, node["lat"], node["lon"]) <= radius_km:
            last_in_radius = node_id
        else:
            break
    for i in range(1, len(full_path)):
        total_distance += ef.get_edge_weight(graph_distance, full_path[i-1], full_path[i]) or 0
    first_5_details = ef.get_path_details(catalog, full_path[:5], graph_distance)
    last_5_details = ef.get_path_details(catalog, full_path[-5:], graph_distance)
    
    return {"ruta_encontrada": True,"ultimo_nodo_area_interes": last_in_radius,"distancia_total": total_distance,"total_puntos": len(full_path),"primeros_5_puntos": first_5_details,"ultimos_5_puntos": last_5_details,"radio_analizado": radius_km}


def req_4(catalog, initial_point, graph_water):
    origin_point = ef.find_nearest_migration_point(catalog, initial_point[0], initial_point[1])
    if origin_point is None:
        return {"mensaje": "No se encontró punto migratorio cercano al origen."}
    mst_edges, mst_vertices = prim_mst(graph_water, origin_point["id"])
    if not mst_vertices:
        return {"mensaje": "No se encontró red hídrica viable desde el punto origen."}
    total_distance = sum(edge[2] if edge[2] is not None else 0 for edge in mst_edges)
    total_points = len(mst_vertices)
    total_individuals = sum(catalog[v]["events_count"] if v in catalog else 0 for v in mst_vertices)
    sorted_vertices = sorted(mst_vertices)
    first_5_details = ef.get_path_details(catalog, sorted_vertices[:5], graph_water)
    last_5_details = ef.get_path_details(catalog, sorted_vertices[-5:], graph_water)
    
    return {"ruta_encontrada": True,"punto_origen": origin_point["id"],"total_puntos": total_points,"total_individuos": total_individuals,"distancia_total_corredor": total_distance,"primeros_5_puntos": first_5_details,"ultimos_5_puntos": last_5_details}

def prim_mst(graph_, start_vertex):
    import heapq
    mst_edges = []
    mst_vertices = set()
    edge_queue = []
    mst_vertices.add(start_vertex)

    def get_neighbors_with_weights(u):
        vertex = lp.get(graph_['vertices'], u)
        if vertex is None:
            return []
        adj_map = V.get_adjacents(vertex)
        if adj_map is None:
            return []
        keys = lp.key_set(adj_map)
        return [(v, lp.get(adj_map, v)) for v in keys]

    for neighbor, weight in get_neighbors_with_weights(start_vertex):
        heapq.heappush(edge_queue, (weight, start_vertex, neighbor))

    while edge_queue and len(mst_vertices) < graph.order(graph_):
        weight, u, v = heapq.heappop(edge_queue)
        if v not in mst_vertices:
            mst_vertices.add(v)
            mst_edges.append((u, v, weight))
            for n, w in get_neighbors_with_weights(v):
                if n not in mst_vertices:
                    heapq.heappush(edge_queue, (w, v, n))
    return mst_edges, mst_vertices


def req_5(catalog, initial_point, final_point, graph_type, graph1, graph2):
    if graph_type == "distancia":
        selected_graph = graph1
    elif graph_type == "hidrica":
        selected_graph = graph2
    else:
        return {"mensaje": "Tipo de grafo inválido. Use 'distancia' o 'hidrica'"}
    
    origin_point = ef.find_nearest_migration_point(catalog, initial_point[0], initial_point[1])
    dest_point = ef.find_nearest_migration_point(catalog, final_point[0], final_point[1])
    
    if origin_point is None or dest_point is None:
        return {"mensaje": "No se encontraron puntos migratorios cercanos"}
    
    dijkstra_result = dij.dijkstra(selected_graph, origin_point["id"])
    
    if not ef.has_path_to(dest_point["id"], dijkstra_result):
        return {"mensaje": "No existe camino viable", "origen": origin_point["id"], "destino": dest_point["id"], "tipo_grafo": graph_type}
    
    path_stack = ef.path_to(dest_point["id"], dijkstra_result)
    full_path = []
    
    while not st.is_empty(path_stack):
        node_id = st.pop(path_stack)
        full_path.append(node_id)
    full_path.reverse()
    
    total_cost = ef.dist_to(dest_point["id"], dijkstra_result)
    total_points = len(full_path)
    total_segments = total_points - 1
    
    first_5_details = ef.get_path_details(catalog, full_path[:5], selected_graph)
    last_5_details = ef.get_path_details(catalog, full_path[-5:], selected_graph)
    
    return {"ruta_encontrada": True,"tipo_grafo": graph_type,"costo_total": total_cost,"total_puntos": total_points,"total_segmentos": total_segments,"primeros_5_puntos": first_5_details,"ultimos_5_puntos": last_5_details,"origen": origin_point["id"],"destino": dest_point["id"]}

def req_6(graph_water, catalog):
    if graph.order(graph_water) == 0:
        return {"mensaje": "Grafo vacío. No se encontraron subredes hídricas."}
    
    components = ef.find_connected_components(graph_water, catalog)
    
    if not components:
        return {"mensaje": "No se reconocieron subredes hídricas viables."}
    
    total_subredes = len(components)
    top_components = components[:5]
    
    result = {"total_subredes": total_subredes, "subredes_mas_grandes": []}
    
    for comp in top_components:
        subred_info = {
            "id_subred": comp['id_subred'],
            "lat_min": round(comp['lat_min'], 6),
            "lat_max": round(comp['lat_max'], 6),
            "lon_min": round(comp['lon_min'], 6),
            "lon_max": round(comp['lon_max'], 6),
            "total_puntos": comp['total_puntos'],
            "total_individuos": comp['total_individuos'],
            "primeros_3_puntos": [{"id": p['id'], "lat": round(p['lat'], 6), "lon": round(p['lon'], 6)} for p in comp['primeros_3_puntos']],
            "ultimos_3_puntos": [{"id": p['id'], "lat": round(p['lat'], 6), "lon": round(p['lon'], 6)} for p in comp['ultimos_3_puntos']],
            "primeras_3_grullas": comp['primeras_3_grullas'],
            "ultimas_3_grullas": comp['ultimas_3_grullas']
        }
        result["subredes_mas_grandes"].append(subred_info)
    
    return result

def get_time():
    return float(time.perf_counter()*1000)

def delta_time(start, end):
    return float(end - start)
