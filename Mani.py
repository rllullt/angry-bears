# -*- coding: utf-8 -*-

'''
Clase Mani
Crea un maní de la clase Alimento
'''

from Alimento import Alimento

# Clase Mani
# Campos:
# nombreArchivo (contiene el nombre del archivo STL): str
# rugosidad (si es rugoso o brillante): str
class Mani(Alimento):
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= [0.7608, 0.6902, 0.4706, 1.0]):
        # Color beige
        self.nombreArchivo= "peanut_2.stl"
        self.rugosidad= "r"
        
        Alimento.__init__(self, self.rugosidad, self.nombreArchivo, None, pos, sz, rgb)