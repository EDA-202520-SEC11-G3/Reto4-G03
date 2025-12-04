import sys
from . import logic as log
from . import extra_functions as ef
import tabulate as tb


def new_logic():
    """
        Se crea una instancia del controlador
    """
    return log.new_logic()


def print_menu():
    print("\n" + "="*60)
    print("ANALISIS DE MOVIMIENTOS MIGRATORIOS")
    print("Grullas Damisela - Mongolia")
    print("="*60)
    print("0- Cargar informacion")
    print("1- Ejecutar Requerimiento 1 (DFS - Camino de individuo)")
    print("2- Ejecutar Requerimiento 2 (BFS - Movimientos en area)")
    print("3- Ejecutar Requerimiento 3 (Topological - Rutas migratorias)")
    print("4- Ejecutar Requerimiento 4 (Prim - Corredores hidricos)")
    print("5- Ejecutar Requerimiento 5 (Dijkstra - Ruta optima)")
    print("6- Ejecutar Requerimiento 6 (Componentes - Subpoblaciones)")
    print("7- Salir")
    print("="*60)


def load_data(control, filename):
    """
    Carga los datos
    """
    return log.load_data(control, filename)


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    pass


def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    print("\n" + "="*60)
    print("REQ 1: Camino de un individuo (DFS)")
    print("="*60)
    
    print("\nIngrese coordenadas GPS del punto de ORIGEN:")
    lat_origen = float(input("  Latitud: "))
    lon_origen = float(input("  Longitud: "))
    
    print("\nIngrese coordenadas GPS del punto de DESTINO:")
    lat_destino = float(input("  Latitud: "))
    lon_destino = float(input("  Longitud: "))
    
    individuo_id = input("\nIngrese el identificador del individuo (grulla): ")
    
    start = log.get_time()
    result = log.req_1(control, lat_origen, lon_origen, lat_destino, lon_destino, individuo_id)
    end = log.get_time()
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"Primer nodo del camino: {result['origin_node']}")
    print(f"Individuo: {result['individuo']}")
    print(f"Distancia total de desplazamiento: {result['total_distance']} km")
    print(f"Total de puntos en el camino: {result['total_points']}")
    print(f"{'='*60}")
    
    print(f"\n5 primeros puntos migratorios:")
    print(tb.tabulate(result['first_5'], headers="keys", tablefmt="grid"))
    
    print(f"\n5 ultimos puntos migratorios:")
    print(tb.tabulate(result['last_5'], headers="keys", tablefmt="grid"))
    
    print(f"\nTiempo de ejecucion: {round(log.delta_time(start, end), 2)} ms")


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    print("\n" + "="*60)
    print("REQ 2: Movimientos alrededor de un area (BFS)")
    print("="*60)
    
    print("\nIngrese coordenadas GPS del punto de ORIGEN:")
    lat_origen = float(input("  Latitud: "))
    lon_origen = float(input("  Longitud: "))
    
    print("\nIngrese coordenadas GPS del punto de DESTINO:")
    lat_destino = float(input("  Latitud: "))
    lon_destino = float(input("  Longitud: "))
    
    radio = float(input("\nIngrese el radio del area de interes (km): "))
    
    start = log.get_time()
    result = log.req_2(control, lat_origen, lon_origen, lat_destino, lon_destino, radio)
    end = log.get_time()
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"Ultimo nodo dentro del area de interes: {result['last_in_area']}")
    print(f"Radio del area: {result['radio']} km")
    print(f"Distancia total de desplazamiento: {result['total_distance']} km")
    print(f"Total de puntos en el camino: {result['total_points']}")
    print(f"{'='*60}")
    
    print(f"\n5 primeros puntos migratorios:")
    print(tb.tabulate(result['first_5'], headers="keys", tablefmt="grid"))
    
    print(f"\n5 ultimos puntos migratorios:")
    print(tb.tabulate(result['last_5'], headers="keys", tablefmt="grid"))
    
    print(f"\nTiempo de ejecucion: {round(log.delta_time(start, end), 2)} ms")


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    print("\n" + "="*60)
    print("REQ 3: Rutas migratorias (Topological Sort)")
    print("="*60)
    
    start = log.get_time()
    result = log.req_3(control)
    end = log.get_time()
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"Total de puntos en la ruta migratoria: {result['total_points']}")
    print(f"Total de individuos que utilizan la ruta: {result['total_individuos']}")
    print(f"{'='*60}")
    
    print(f"\n5 primeros puntos migratorios:")
    print(tb.tabulate(result['first_5'], headers="keys", tablefmt="grid"))
    
    print(f"\n5 ultimos puntos migratorios:")
    print(tb.tabulate(result['last_5'], headers="keys", tablefmt="grid"))
    
    print(f"\nTiempo de ejecucion: {round(log.delta_time(start, end), 2)} ms")


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    print("\n" + "="*60)
    print("REQ 4: Corredores hidricos optimos (Prim MST)")
    print("="*60)
    
    print("\nIngrese coordenadas GPS del punto de ORIGEN:")
    lat_origen = float(input("  Latitud: "))
    lon_origen = float(input("  Longitud: "))
    
    start = log.get_time()
    result = log.req_4(control, lat_origen, lon_origen)
    end = log.get_time()
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"Nodo de origen: {result['origin_node']}")
    print(f"Total de puntos en el corredor hidrico: {result['total_points']}")
    print(f"Total de individuos: {result['total_individuos']}")
    print(f"Distancia total a fuentes hidricas: {result['total_water_distance']} km")
    print(f"{'='*60}")
    
    print(f"\n5 primeros puntos migratorios:")
    print(tb.tabulate(result['first_5'], headers="keys", tablefmt="grid"))
    
    print(f"\n5 ultimos puntos migratorios:")
    print(tb.tabulate(result['last_5'], headers="keys", tablefmt="grid"))
    
    print(f"\nTiempo de ejecucion: {round(log.delta_time(start, end), 2)} ms")


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    print("\n" + "="*60)
    print("REQ 5: Ruta migratoria mas eficiente (Dijkstra)")
    print("="*60)
    
    print("\nIngrese coordenadas GPS del punto de ORIGEN:")
    lat_origen = float(input("  Latitud: "))
    lon_origen = float(input("  Longitud: "))
    
    print("\nIngrese coordenadas GPS del punto de DESTINO:")
    lat_destino = float(input("  Latitud: "))
    lon_destino = float(input("  Longitud: "))
    
    print("\nSeleccione el tipo de grafo:")
    print("  1. Distancia de desplazamiento")
    print("  2. Distancia a fuentes hidricas")
    tipo_grafo = input("Opcion: ")
    
    start = log.get_time()
    result = log.req_5(control, lat_origen, lon_origen, lat_destino, lon_destino, tipo_grafo)
    end = log.get_time()
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"Nodo de origen: {result['origin_node']}")
    print(f"Nodo de destino: {result['dest_node']}")
    print(f"Tipo de grafo: {result['tipo_grafo']}")
    print(f"Costo total: {result['total_cost']} km")
    print(f"Total de puntos: {result['total_points']}")
    print(f"Total de segmentos: {result['total_segments']}")
    print(f"{'='*60}")
    
    print(f"\n5 primeros puntos migratorios:")
    print(tb.tabulate(result['first_5'], headers="keys", tablefmt="grid"))
    
    print(f"\n5 ultimos puntos migratorios:")
    print(tb.tabulate(result['last_5'], headers="keys", tablefmt="grid"))
    
    print(f"\nTiempo de ejecucion: {round(log.delta_time(start, end), 2)} ms")


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    print("\n" + "="*60)
    print("REQ 6: Subpoblaciones aisladas (Componentes Conectados)")
    print("="*60)
    
    start = log.get_time()
    result = log.req_6(control)
    end = log.get_time()
    
    if "error" in result:
        print(f"\nError: {result['error']}")
        return
    
    print(f"\n{'='*60}")
    print(f"Total de subredes hidricas identificadas: {result['total_subredes']}")
    print(f"{'='*60}")
    
    print(f"\nMostrando las 5 subredes mas grandes:\n")
    print(tb.tabulate(result['subredes'], headers="keys", tablefmt="grid"))
    
    print(f"\nTiempo de ejecucion: {round(log.delta_time(start, end), 2)} ms")


# main del ejercicio
def main():
    """
    Menu principal
    """
    loaded = False
    working = True
    control = new_logic()
    
    while working:
        print_menu()
        inputs = input('\nSeleccione una opcion para continuar: ')
        
        try:
            option = int(inputs)
        except ValueError:
            print("\nOpcion invalida. Por favor ingrese un numero.")
            continue
        
        if option == 0:
            if not loaded:
                loaded = True
                print("\n" + "="*60)
                print("CARGA DE DATOS")
                print("="*60)
                filename = input("Selecciona el tamano de los datos:\n A. Pequeno\n B. 30pct\n C. 80pct\n D. Grande\nOpcion: ")
                
                if filename.lower() == "a":
                    filename = "\\Data\\1000_cranes_mongolia_small.csv"
                elif filename.lower() == "b":
                    filename = "\\Data\\1000_cranes_mongolia_30pct.csv"
                elif filename.lower() == "c":
                    filename = "\\Data\\1000_cranes_mongolia_80pct.csv"
                elif filename.lower() == "d":
                    filename = "\\Data\\1000_cranes_mongolia_large.csv"
                else:
                    print("Datos de prueba")
                    filename = "\\Data\\1000_cranes_mongolia_reference_data.csv"
                
                print("\nCargando informacion de los archivos....\n")
                data = load_data(control, filename)
                
                # Actualizar control con el catálogo cargado
                control = data["catalog"]
                
                # Mostrar información de carga
                print("\n" + "="*60)
                print("INFORMACION DE CARGA")
                print("="*60)
                print(f"Total de grullas reconocidas: {data['total_cranes']}")
                print(f"Total de eventos cargados: {data['total_events']}")
                print(f"Total de nodos del grafo: {data['total_nodes']}")
                print(f"Total de arcos (grafo distancias): {data['total_edges_distance']}")
                print(f"Total de arcos (grafo hidrico): {data['total_edges_water']}")
                print("="*60)
                
                print("\nPrimeros 5 nodos creados:")
                print(tb.tabulate(data['first_5_nodes'], headers="keys", tablefmt="grid"))
                
                print("\nUltimos 5 nodos creados:")
                print(tb.tabulate(data['last_5_nodes'], headers="keys", tablefmt="grid"))
                
            else:
                confirmation = input("\n¿Desea cargar otro archivo? (y/n): ")
                if confirmation.lower() in ["n", "no"]:
                    print("\nContinua haciendo uso de la aplicacion")
                elif confirmation.lower() in ["y", "si", "yes"]:
                    control = new_logic()
                    loaded = False
        
        elif option == 1:
            if not loaded:
                print("\nPor favor cargue los datos primero (Opcion 0).")
            else:
                print_req_1(control)
        
        elif option == 2:
            if not loaded:
                print("\nPor favor cargue los datos primero (Opcion 0).")
            else:
                print_req_2(control)
        
        elif option == 3:
            if not loaded:
                print("\nPor favor cargue los datos primero (Opcion 0).")
            else:
                print_req_3(control)
        
        elif option == 4:
            if not loaded:
                print("\nPor favor cargue los datos primero (Opcion 0).")
            else:
                print_req_4(control)
        
        elif option == 5:
            if not loaded:
                print("\nPor favor cargue los datos primero (Opcion 0).")
            else:
                print_req_5(control)
        
        elif option == 6:
            if not loaded:
                print("\nPor favor cargue los datos primero (Opcion 0).")
            else:
                print_req_6(control)
        
        elif option == 7:
            working = False
            print("\n" + "="*60)
            print("Gracias por utilizar el programa")
            print("Analisis de Movimientos Migratorios")
            print("Grullas Damisela - Mongolia")
            print("="*60 + "\n")
        
        else:
            print("\nOpcion erronea, vuelva a elegir.")
    
    sys.exit(0)
