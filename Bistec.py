# -*- coding: utf-8 -*-

'''
Clase Bistec
Crea un bistec de alimento a partir de un archivo STL
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from Alimento import Alimento

# Clase Bistec
# Campos:
# nombreArchivo (contiene el nombre del archivo STL): str
# rugosidad (si es rugoso o brillante): str
# rgb (color en rgb): floatv
# lista (lista que contiene la lista del alimento): glList
class Bistec(Alimento):
    # Constructor:
    # Este es diferente porque recibe listas de colores para ambas partes (el bistec y la grasa)
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= ([0.6863, 0.1686, 0.1176, 1.0], [0.9569, 0.9569, 0.9569, 1.0])):
        # Colores: rojo vivo y blanco señales
        self.nombreArchivo= ["meat.stl", "fat.stl"]
        self.rugosidad= ["r", "b"]
        self.carne= Alimento(self.rugosidad[0], self.nombreArchivo[0], None, pos, None, rgb[0])
        self.grasa= Alimento(self.rugosidad[1], self.nombreArchivo[1], None, pos, None, rgb[1])
        
        self.lista= self.generarLista()
        
        Alimento.__init__(self, self.rugosidad, None, self.lista, pos, sz, rgb[0])
        
    # Métodos
    
    # generarLista: None -> glList
    # Genera la lista con los puntos del bistec
    def generarLista(self):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        self.carne.dibujar()
        self.grasa.dibujar()
        
        glEndList()
        
        return lista
    
