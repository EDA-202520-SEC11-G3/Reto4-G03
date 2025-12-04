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
    print("Bienvenido")
    print("0- Cargar información")
    print("1- Ejecutar Requerimiento 1")
    print("2- Ejecutar Requerimiento 2")
    print("3- Ejecutar Requerimiento 3")
    print("4- Ejecutar Requerimiento 4")
    print("5- Ejecutar Requerimiento 5")
    print("6- Ejecutar Requerimiento 6")
    print("7- Salir")

def load_data(control, filename):
    """
    Carga los datos
    """
    return log.load_data(control, filename)


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control,lat1,lon1,lat2,lon2,grulla):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    return log.req_1(control[2],[lat1,lon1],[lat2,lon2], grulla, control[0])


def print_req_2(control):
    result = log.req_2(control[2], [float(input("Latitud del origen: ")), float(input("Longuitud del origen: "))], [float(input("Latitud del destino: ")), float(input("Longuitud del destino: "))],
                       float(input("Radio área interés (km): ")), control[0])
    print("Ruta encontrada:", result.get("ruta_encontrada", False))
    print("Último nodo dentro del área de interés:", result.get("ultimo_nodo_area_interes", "Desconocido"))
    print("Distancia total:", result.get("distancia_total", "Desconocido"))
    print("Total de puntos:", result.get("total_puntos", "Desconocido"))
    print("5 primeros puntos:")
    print(tb.tabulate(result.get("primeros_5_puntos", []), headers="keys"))
    print("5 últimos puntos:")
    print(tb.tabulate(result.get("ultimos_5_puntos", []), headers="keys"))


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    lat_origen = float(input("Latitud punto origen: "))
    lon_origen = float(input("Longitud punto origen: "))
    result = log.req_4(control[2], [lat_origen, lon_origen], control[1])
    if result.get("ruta_encontrada", False):
        print("Total puntos en corredor:", result.get("total_puntos", "Desconocido"))
        print("Total individuos en corredor:", result.get("total_individuos", "Desconocido"))
        print("Distancia total del corredor hídrico:", result.get("distancia_total_corredor", "Desconocido"))
        print("5 primeros puntos:")
        print(tb.tabulate(result.get("primeros_5_puntos", []), headers="keys"))
        print("5 últimos puntos:")
        print(tb.tabulate(result.get("ultimos_5_puntos", []), headers="keys"))
    else:
        print(result.get("mensaje", "No se encontró corredor hídrico."))


def print_req_5(control):
    lat1 = float(input("Ingrese latitud del origen: "))
    lon1 = float(input("Ingrese longitud del origen: "))
    lat2 = float(input("Ingrese latitud del destino: "))
    lon2 = float(input("Ingrese longitud del destino: "))
    tipo = input("Seleccione tipo de grafo ('distancia' o 'hidrica'): ").strip().lower()
    result = log.req_5(control[2], [lat1, lon1], [lat2, lon2], tipo, control[0], control[1])
    if result.get("ruta_encontrada", False):
        print("Costo total:", result.get("costo_total", "Desconocido"))
        print("Total puntos:", result.get("total_puntos", "Desconocido"))
        print("Total segmentos:", result.get("total_segmentos", "Desconocido"))
        print("5 primeros puntos:")
        print(tb.tabulate(result.get("primeros_5_puntos", []), headers="keys"))
        print("5 últimos puntos:")
        print(tb.tabulate(result.get("ultimos_5_puntos", []), headers="keys"))
    else:
        print(result.get("mensaje", "No se encontró ruta viable."))


def print_req_6(control):
    result = log.req_6(control[1], control[2])
    if "mensaje" in result:
        print(result["mensaje"])
    else:
        print("Total de subredes hídricas:", result.get("total_subredes", 0))
        for subred in result.get("subredes_mas_grandes", []):
            print(f"Subred ID: {subred['id_subred']}")
            print("Latitud mínima:", subred.get("lat_min", "Desconocido"))
            print("Latitud máxima:", subred.get("lat_max", "Desconocido"))
            print("Longitud mínima:", subred.get("lon_min", "Desconocido"))
            print("Longitud máxima:", subred.get("lon_max", "Desconocido"))
            print("Total puntos migratorios:", subred.get("total_puntos", "Desconocido"))
            print("Total individuos:", subred.get("total_individuos", "Desconocido"))
            print("Primeros 3 puntos migratorios:")
            print(tb.tabulate(subred.get("primeros_3_puntos", []), headers="keys"))
            print("Últimos 3 puntos migratorios:")
            print(tb.tabulate(subred.get("ultimos_3_puntos", []), headers="keys"))
            print("Primeras 3 grullas:", subred.get("primeras_3_grullas", []))
            print("Últimas 3 grullas:", subred.get("ultimas_3_grullas", []))
            print("-" * 40)

# Se crea la lógica asociado a la vista

# main del ejercicio
def main():
    """
    Menu principal
    """
    loaded = False
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
             if not loaded:
                loaded = True
                filename = input("Selecciona el tamaño de los datos:\n A. Pequeño\n B. 30pct \n C. 80pct \n D. Grande\n")
                if filename.lower() == "a":
                    filename = "\\Data\\1000_cranes_mongolia_small.csv"
                if filename.lower() == "b":
                    filename = "\\Data\\1000_cranes_mongolia_30pct.csv"
                if filename.lower() == "d":
                    filename = "\\Data\\1000_cranes_mongolia_large.csv"
                if filename.lower() == "c":
                    filename = "\\Data\\1000_cranes_mongolia_80pct.csv"
                if filename=="":
                    print("Datos de prueba")
                    filename="\\Data\\1000_cranes_mongolia_reference_data.csv"
                print("Cargando información de los archivos ....\n")
                control = new_logic()
                control = load_data(control, filename)
                ef.get_top_bottom_five_points(control[0],control[1])
             elif loaded:
                confirmation = input("¿Desea cargar otro archivo? y/n \n (Recuerde que los datos no se guardarán)\n")
                if confirmation.lower() == "n" or confirmation.lower() == "no" or confirmation.lower() == "non":
                    print("Perfecto, continúa haciendo uso de la aplicación")
                if confirmation.lower() == "y" or confirmation.lower() == "si" or confirmation.lower() == "yes" or confirmation.lower() == "oui":
                    control = new_logic()
                    filename = input("Selecciona el tamaño de los datos:\n A. Pequeño\n B. 30pct \n C. 80pct \n D. Grande\n")
                    if filename.lower() == "a":
                        filename = "\\Data\\1000_cranes_mongolia_small.csv"
                    if filename.lower() == "b":
                        filename = "\\Data\\1000_cranes_mongolia_30pct.csv"
                    if filename.lower() == "d":
                        filename = "\\Data\\1000_cranes_mongolia_large.csv"
                    if filename.lower() == "c":
                        filename = "\\Data\\1000_cranes_mongolia_80pct.csv"
                    if filename=="":
                        print("Datos de prueba")
                        filename="\\Data\\1000_cranes_mongolia_reference_data.csv"
                    print("Cargando información de los archivos ....\n")
                    control = new_logic()
                    control = load_data(control, filename)
                    ef.get_top_bottom_five_points(control[0],control[1])
        elif int(inputs) == 1:
            lat1 = float(input("Ingrese la latitud del origen:"))
            lon1 = float(input("Ingrese la longuitud del origen:"))
            lat2 = float(input("Ingrese la latitud del destino:"))
            lon2 = float(input("Ingrese la longuitud del destino:"))
            grulla = input("Ingrese la grulla por la que desea filtrar")
            data = print_req_1(control, lat1, lon1, lat2, lon2, grulla)
            if data.get("mensaje") == "No existe camino viable":
                print("No existe camino viable")
            else:
                print("Primer punto registrado "+ str(data["primer_nodo"]+ "\n"))
                print("Distancia total entre los dos puntos " + str(data["distancia_total"]+ "\n"))
                print("Total de puntos en el camino " + str(data["total_puntos"]) + "\n")
                print("5 primeros puntos:\n")
                print(tb.tabulate(data["primeros_5_puntos"], headers="keys"))
                print("5 últimos puntos:\n")
                print(tb.tabulate(data["ultimos_5_puntos"], headers="keys"))

        elif int(inputs) == 2:
            print_req_2(control)

        elif int(inputs) == 3:
            print_req_3(control)

        elif int(inputs) == 4:
            print_req_4(control)

        elif int(inputs) == 5:
            print_req_5(control)

        elif int(inputs) == 5:
            print_req_6(control)

        elif int(inputs) == 7:
            working = False
            print("\nGracias por utilizar el programa") 
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
