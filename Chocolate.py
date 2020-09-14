# -*- coding: utf-8 -*-

'''
Clase Chocolate
Genera un nuevo chocolate a partir de archivo STL
'''

from Alimento import Alimento

# Clase Chocolate
# Campos:
# nombreArchivo (contiene el nombre del archivo STL): str
# rugosidad (si es rugoso o brillante): str
class Chocolate(Alimento):
    # Constructor;
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= [0.2706, 0.1961, 0.1804, 1.0]):
        # El color es color chocolate
        self.nombreArchivo= "chocoplate.stl"
        self.rugosidad= "r"
        
        Alimento.__init__(self, self.rugosidad, self.nombreArchivo, None, pos, sz, rgb)
        