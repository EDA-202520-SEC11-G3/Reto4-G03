import os
import csv
from DataStructures.Graph import vertex as V
from DataStructures.Map import map_linear_probing as lp
from DataStructures.List import array_list as lt
from math import radians, sin, cos, sqrt, atan2, asin

data_dir = os.path.dirname(os.path.realpath(__file__))

def haversine(lat1, lon1, lat2, lon2):
    """Haversine en km usando radio Tierra 6371km"""
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return 2 * R * atan2(sqrt(a), sqrt(1-a))

