from DataStructures.Map import map_linear_probing as map
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Queue import queue as q


def new_prim_structure(source, g_order):
    """
    Crea una estructura de busqueda usada en el algoritmo **prim**.

    Se crea una estructura de busqueda con los siguientes atributos:

    - **source**: Vertice de inicio del MST.
    - **edge_from**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **dist_to**: Mapa con las distancias a los vertices. Se inicializa en ``None``
    - **marked**: Mapa con los vertices visitados. Se inicializa en ``None``
    - **pq**: Cola de prioridad indexada (index_priority_queue). Se inicializa en ``None``

    :returns: Estructura de busqueda
    :rtype: prim_search
    """

    structure = {
        "source": source,
        "edge_from": map.new_map(g_order, 0.5),
        "dist_to": map.new_map(g_order, 0.5),
        "marked": map.new_map(g_order, 0.5),
        "pq":  pq.new_heap(),
    }

    return structure

def prim_mst(graph, start_vertex):
    """
    Implementación mínima de Prim para grafo dirigido con pesos.
    Recebe grafo y vértice inicial.
    Retorna lista de aristas MST y conjunto de vértices incluidos.
    """

    import heapq

    mst_edges = []
    mst_vertices = set()
    edge_queue = []

    mst_vertices.add(start_vertex)

    # Usar mapa de vertices para obtener adyacencias y pesos
    def get_neighbors_with_weights(u):
        vertex = mp.get(graph['vertices'], u)
        if vertex is None:
            return []
        adj_map = vtx.get_adjacents(vertex)
        if adj_map is None:
            return []
        keys = mp.key_set(adj_map)
        neighbor_weights = [(v, mp.get(adj_map, v)) for v in keys]
        return neighbor_weights

    # Push edges origen a queue
    for neighbor, weight in get_neighbors_with_weights(start_vertex):
        heapq.heappush(edge_queue, (weight, start_vertex, neighbor))

    while edge_queue and len(mst_vertices) < dg.order(graph):
        weight, u, v = heapq.heappop(edge_queue)
        if v not in mst_vertices:
            mst_vertices.add(v)
            mst_edges.append((u, v, weight))
            # Agregar nuevos bordes desde v
            for n, w in get_neighbors_with_weights(v):
                if n not in mst_vertices:
                    heapq.heappush(edge_queue, (w, v, n))

    return mst_edges, mst_vertices
