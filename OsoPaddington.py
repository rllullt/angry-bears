# -*- coding: utf-8 -*-

'''
Clase OsoPaddington
Importa los valores del oso Paddington de un archivo STL (de texto)
Guarda los valores en una lista
'''

from OpenGL.GL import *
from OpenGL.GLU import *

# Clase OsoPaddington
# Campos:
# pos (posición de la base del oso): floatv
# angulo (angulo para rotar): float
# rot (ejes en los que rotar): floatv
# sz (tamaño a escalarse): floatv
# rgb (color del oso): floatv
# cuerpo (lista que contiene el cuerpo principal): glList
# maleta (lista que contiene la maleta): glList
# lista (que contiene los puntos a dibujar): glList
class OsoPaddington:
    # Constructor
    def __init__(self, pos=[0.0, 0.0, 0.0], angulo= 0.0, rot= None, sz= None, rgb= [0.5412, 0.4, 0.2588, 1.0]):
        # El color es café pardo
        # Posición
        self.xpos= pos[0]
        self.ypos= pos[1]
        self.zpos= pos[2]
        # Ángulo de rotación
        self.angulo= angulo
        # Eje de rotación
        self.rot= rot
        # Tamaño a escalarse
        self.sz= sz
        # Color
        self.rgb= rgb
        # Lista de los polígonos
        self.cuerpo= self.generarLista("Paddington_Bear.stl")
        self.maleta= self.generarLista("Paddington_Bear_Suitcase.stl")
        self.lista= self.corregirAltura(self.cuerpo, self.maleta)
        
    # Métodos
    
    # corregirAltura: glList -> glList
    # Traslada el oso al origen
    def corregirAltura(self, lista1, lista2):
        lista3= glGenLists(1)
        glNewList(lista3, GL_COMPILE)
        
        glPushMatrix()
        glTranslatef(0, 0, 5)
        # Hay que rotarlo porque se dibuja en el eje Z, mirando opuesto a los otros ejes
        glRotatef(180, 0, 1, 0)
        glRotatef(90, -1, 0, 0)
        glCallList(lista1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-5, 3, 12)
        # Hay que rotarlo porque se dibuja en el eje Z, mirando opuesto a los otros ejes
        glRotatef(180, 0, 1, 0)
        glRotatef(90, -1, 0, 0)
        glCallList(lista2)
        glPopMatrix()
        
        glEndList()
        
        return lista3
    
    # getBlanco: None -> floatv[floatv]
    # Retorna las coordenadas donde, si le llega el alimento, come
    def getBlanco(self):
        return [[self.xpos - 30, self.xpos + 30],
                [self.ypos, self.ypos + 250],
                [self.zpos - 55, self.zpos + 55]]
    
    # getPos: None -> list
    # Retorna la posición del oso
    def getPos(self):
        return [self.xpos, self.ypos, self.zpos]
    
    # setPos: list -> None
    # Setea la posición del objeto en esa posición
    def setPos(self, nuevaPos):
        self.xpos= nuevaPos[0]
        self.ypos= nuevaPos[1] # estaba en -73*sz[1]
        self.zpos= nuevaPos[2]
    
    # generarLista: str -> glList
    # Genera la lista que contiene los puntos, a partir de un archivo STL
    def generarLista(self, nombreArchivo):
        # Se crea la lista que guardará los triángulos
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # Abrir el archivo
        archivo= open(nombreArchivo, "r") # archivo es un objeto File, "r" es por leer
        # Se lee el archivo y se trabaja
        glBegin(GL_TRIANGLES)
        
        for linea in archivo:
            # Se asume que cada punto está en 3D
            if "vertex" in linea: # vértices primero porque hay más
                palabras= linea.split() # por defecto es espacio
                glVertex3f(float(palabras[1]), float(palabras[2]), float(palabras[3]))
            elif "normal" in linea:
                palabras= linea.split()
                glNormal3f(float(palabras[2]), float(palabras[3]), float(palabras[4]))
        
        glEnd()
        
        archivo.close()
        
        glEndList()
        
        return lista
        
    def dibujar(self):
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        
        glTranslatef(self.xpos, self.ypos, self.zpos)
        if (self.sz != None):
            glScalef(self.sz[0], self.sz[1], self.sz[2])
        if (self.rot != None):
            glRotatef(self.angulo, self.rot[0], self.rot[1], self.rot[2])
        if (self.rgb != None):
            glColor4fv(self.rgb)
        glCallList(self.lista)
        
        glPopMatrix()
        
