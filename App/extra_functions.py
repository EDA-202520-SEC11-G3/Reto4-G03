import os
import csv
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as alt
from DataStructures.Graph import digraph as dg
from DataStructures.Stack import stack as st
from math import radians, sin, cos, sqrt, atan2, asin

data_dir = os.path.dirname(os.path.realpath(__file__))

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1-a))

def calc_time_diff(ts1, ts2):
    """
    Calcula diferencia en horas entre dos timestamps string
    Formato: "YYYY-MM-DD HH:MM:SS.ffffff"
    """
    date1, time1 = ts1.split()
    date2, time2 = ts2.split()
    
    # Fecha
    y1, m1, d1 = map(int, date1.split('-'))
    y2, m2, d2 = map(int, date2.split('-'))
    
    # Tiempo
    h1, min1, s1 = time1.split(':')
    h2, min2, s2 = time2.split(':')
    h1, min1 = int(h1), int(min1)
    h2, min2 = int(h2), int(min2)
    s1 = float(s1)
    s2 = float(s2)
    
    # Calcular días aproximados
    days1 = y1 * 365 + m1 * 30 + d1
    days2 = y2 * 365 + m2 * 30 + d2
    
    # Calcular horas totales
    total_hours1 = days1 * 24 + h1 + min1/60 + s1/3600
    total_hours2 = days2 * 24 + h2 + min2/60 + s2/3600
    
    return abs(total_hours1 - total_hours2)


def get_grid_key(lat, lon, grid_size):
        grid_x = int(lat / grid_size)
        grid_y = int(lon / grid_size)
        return (grid_x, grid_y)

def cmp_timestamps(e1, e2):
        return e1[0] < e2[0]

# Funciones Auxiliares

def dfs(my_graph, source):
    # función DFS usando las estructuras indicadas
    # implementación la misma que la que ya proporcionaste anteriormente
    pass

def bfs(my_graph, source):
    # función BFS usando queue proporcionada en estructura
    # implementación ya proporcionada anteriormente
    pass

def find_nearest_migration_point(catalog, target_lat, target_lon):
    min_dist = float('inf')
    nearest = None
    for event_id, event in catalog.items():
        dist = haversine(target_lat, target_lon, event["lat"], event["lon"])
        if dist <= 3 and dist < min_dist:
            min_dist = dist
            nearest = event
    return nearest

def crane_in_point(event, crane_id):
    for record in event["events"]["elements"]:
        if record["tag-local-identifier"] == crane_id:
            return True
    return False

def get_path_details(catalog, node_ids, graph, crane_id=None):
    details = []
    for i, node_id in enumerate(node_ids):
        event = catalog.get(node_id, {})
        if not event:
            details.append({"error": "Punto desconocido"})
            continue
        first_record = event["events"]["elements"][0]
        cranes_list = get_cranes_in_point(event)
        top3_cranes = cranes_list[:3] if len(cranes_list) >= 3 else cranes_list
        bottom3_cranes = cranes_list[-3:] if len(cranes_list) >= 3 else cranes_list
        next_dist = "Destino" if i == len(node_ids) - 1 else get_edge_weight(graph, node_id, node_ids[i+1])
        detail = {
            "id_punto": node_id,
            "lat": first_record["lat"],
            "lon": first_record["lon"],
            "num_grullas": event["events_count"],
            "primeras_3_grullas": top3_cranes,
            "ultimas_3_grullas": bottom3_cranes,
            "distancia_siguiente": round(next_dist, 2) if next_dist else "Desconocido"
        }
        details.append(detail)
    return details

def get_cranes_in_point(event):
    return sorted({record["tag-local-identifier"] for record in event["events"]["elements"]})

def get_edge_weight(graph, node1, node2):
    adjacents_list = dg.adjacents(graph, node1)
    if adjacents_list is None:
        return None
    for i in range(alt.size(adjacents_list)):
        adj_node = alt.get_element(adjacents_list, i)
        if adj_node == node2:
            vertex = mp.get(graph['vertices'], node1)
            adj_map = V.get_adjacents(vertex)
            return mp.get(adj_map, node2)
    return None

def is_empty(my_stack):
    return my_stack["size"] == 0

def has_path_to(key_v, structure):
    if structure is None:
        return False
    
    if 'marked' in structure:
        marked_map = structure['marked']
        if mp.contains(marked_map, key_v):
            marked_value = mp.get(marked_map, key_v)
            return marked_value is not None and marked_value != False
        return False
    
    elif 'visited' in structure:
        visited_map = structure['visited']
        if mp.contains(visited_map, key_v):
            vertex_info = mp.get(visited_map, key_v)
            return vertex_info is not None and vertex_info['dist_to'] < float('inf')
        return False
    
    return False

def path_to(key_v, structure):
    path_stack = st.new_stack()
    current_vertex = key_v
    while current_vertex is not None:
        st.push(path_stack, current_vertex)
        if 'marked' in structure:
            edge_to = structure['edge_to'] if 'edge_to' in structure else None
            current_vertex = mp.get(edge_to, current_vertex) if edge_to else None
        elif 'visited' in structure:
            vertex_info = mp.get(structure['visited'], current_vertex)
            current_vertex = vertex_info['edge_from'] if vertex_info else None
        else:
            current_vertex = None
    return path_stack

def dist_to(key_v, structure):
    if 'visited' in structure:
        vertex_info = mp.get(structure['visited'], key_v)
        if vertex_info is None:
            return float('inf')
        return vertex_info['dist_to']
    return float('inf')

def dijkstra(my_graph, source):
    # implementación según estructura proporcionada previamente
    pass

def bfs_component(graph, start_vertex, visited, component_id):
    component_vertices = alt.new_list()
    bfs_result = bfs(graph, start_vertex)
    all_vertices = mp.key_set(graph['vertices'])
    for i in range(alt.size(all_vertices)):
        v = alt.get_element(all_vertices, i)
        if has_path_to(v, bfs_result) or v == start_vertex:
            alt.add_last(component_vertices, v)
            mp.put(visited, v, True)
    return component_vertices

def analyze_component(catalog, component_vertices, component_id):
    vertices_list = []
    total_individuals = 0
    all_cranes = set()
    for i in range(alt.size(component_vertices)):
        vertex_id = alt.get_element(component_vertices, i)
        if vertex_id in catalog:
            event = catalog[vertex_id]
            cranes = get_cranes_in_point(event)
            vertex_info = {
                'id': vertex_id,
                'lat': event["lat"],
                'lon': event["lon"],
                'events_count': event["events_count"],
                'cranes': cranes
            }
            vertices_list.append(vertex_info)
            total_individuals += event["events_count"]
            all_cranes.update(cranes)
    vertices_list.sort(key=lambda x: x['id'])
    lats = [v['lat'] for v in vertices_list]
    lons = [v['lon'] for v in vertices_list]
    return {
        'id_subred': component_id,
        'total_puntos': len(vertices_list),
        'total_individuos': total_individuals,
        'lat_min': min(lats) if lats else "Desconocido",
        'lat_max': max(lats) if lats else "Desconocido",
        'lon_min': min(lons) if lons else "Desconocido",
        'lon_max': max(lons) if lons else "Desconocido",
        'primeros_3_puntos': vertices_list[:3],
        'ultimos_3_puntos': vertices_list[-3:],
        'primeras_3_grullas': sorted(list(all_cranes))[:3],
        'ultimas_3_grullas': sorted(list(all_cranes))[-3:],
        'vertices': vertices_list
    }

def find_connected_components(graph_water, catalog):
    all_vertices = mp.key_set(graph_water['vertices'])
    visited = mp.new_map(num_elements=alt.size(all_vertices), load_factor=0.5)
    components = []
    component_id = 0
    for i in range(alt.size(all_vertices)):
        vertex_id = alt.get_element(all_vertices, i)
        if not mp.contains(visited, vertex_id):
            component_vertices = bfs_component(graph_water, vertex_id, visited, component_id)
            component_info = analyze_component(catalog, component_vertices, component_id)
            components.append(component_info)
            component_id += 1
    components.sort(key=lambda x: (-x['total_puntos'], x['id_subred']))
    return components

def get_top_bottom_five_points(graph1, graph2):
    def extract_node_data(graph, vertex_id):
        vertex_entry = mp.get(graph['vertices'], vertex_id)
        if vertex_entry is None:
            return "Nodo no encontrado"
        return vertex_entry  # Retorna el valor guardado en el nodo, generalmente un diccionario o estructura
    
    vertices_g1 = mp.key_set(graph1['vertices'])
    vertices_g2 = mp.key_set(graph2['vertices'])
    
    size_g1 = alt.size(vertices_g1)
    size_g2 = alt.size(vertices_g2)
    
    first_5_g1 = [alt.get_element(vertices_g1, i) for i in range(min(5, size_g1))]
    last_5_g1 = [alt.get_element(vertices_g1, size_g1 - i - 1) for i in range(min(5, size_g1))]
    
    first_5_g2 = [alt.get_element(vertices_g2, i) for i in range(min(5, size_g2))]
    last_5_g2 = [alt.get_element(vertices_g2, size_g2 - i - 1) for i in range(min(5, size_g2))]
    print("GRAFO 1 (Distancias):")
    print("Primeros 5 nodos y sus valores:")
    for vid in first_5_g1:
        print(f"ID: {vid} - Valor: {extract_node_data(graph1, vid)}")
    print("Últimos 5 nodos y sus valores:")
    for vid in last_5_g1:
        print(f"ID: {vid} - Valor: {extract_node_data(graph1, vid)}")
    print(f"Total vértices: {size_g1}\n")
    
    print("GRAFO 2 (Hídrico):")
    print("Primeros 5 nodos y sus valores:")
    for vid in first_5_g2:
        print(f"ID: {vid} - Valor: {extract_node_data(graph2, vid)}")
    print("Últimos 5 nodos y sus valores:")
    for vid in last_5_g2:
        print(f"ID: {vid} - Valor: {extract_node_data(graph2, vid)}")
    print(f"Total vértices: {size_g2}")