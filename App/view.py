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

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

# Se crea la lógica asociado a la vista

# main del ejercicio
def main():
    """
    Menu principal
    """
    loaded = False
    working = True
    control = new_logic()
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 0:
             if not loaded:
                loaded = True
                filename = input("Selecciona el tamaño de los datos:\n A.Pequeño\n B. 30pct \n C.80pct \n D. Grande\n")
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
                data = load_data(control, filename)
             elif loaded:
                confirmation = input("¿Desea cargar otro archivo? y/n \n (Recuerde que los datos no se guardarán)\n")
                if confirmation.lower() == "n" or confirmation.lower() == "no" or confirmation.lower() == "non":
                    print("Perfecto, continúa haciendo uso de la aplicación")
                if confirmation.lower() == "y" or confirmation.lower() == "si" or confirmation.lower() == "yes" or confirmation.lower() == "oui":
                    control = new_logic()
                    filename = input("Selecciona el tamaño de los datos:\n A.Pequeño\n B. 30pct \n C.80pct \n D. Grande\n")
                    if filename.lower() == "a":
                        filename = "\\Data\\1000_cranes_mongolia_small.csv"
                    if filename.lower() == "b":
                        filename = "\\Data\\1000_cranes_mongolia_30pct.csv"
                    if filename.lower() == "d":
                        filename = "\\Data\\1000_cranes_mongolia_large.csv"
                    if filename.lower() == "c":
                        filename = "\\Data\\1000_cranes_mongolia_80pct.csv"
                    if filename_=="":
                        print("Datos de prueba")
                        filename_="\\Data\\1000_cranes_mongolia_reference_data.csv"
                    print("Cargando información de los archivos ....\n")
                    load_data(control, filename_)
        elif int(inputs) == 1:
            print_req_1(control)

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
