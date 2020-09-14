# -*- coding: utf-8 -*-

'''
Clase Pescado
Genera un objeto pescado sacado de un archivo STL
Hereda la clase Alimento
'''

from Alimento import Alimento

# Clase Pescado
# Campos:
# nombreArchivo (contiene el nombre del archivo STL): str
# rugosidad (si es rugoso o brillante): str
class Pescado(Alimento):
    # Constructor
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= [0.4706, 0.5216, 0.5451, 1.0]):
        # El color es gris ardilla
        self.nombreArchivo= "concrete_fish.stl"
        self.rugosidad= "b"
        
        Alimento.__init__(self, self.rugosidad, self.nombreArchivo, None, pos, sz, rgb)