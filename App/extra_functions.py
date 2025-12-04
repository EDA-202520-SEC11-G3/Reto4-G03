import os
import csv
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as lp
from DataStructures.List import array_list as lt
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