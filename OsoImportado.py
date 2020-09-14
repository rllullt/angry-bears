# -*- coding: utf-8 -*-

'''
Clase OsoImportado
Importa valores de un oso desde archivo STL (binario)
Guarda los valores en una lista
'''

from OpenGL.GL import *
from OpenGL.GLU import *

import struct # para trabajar con el binario

# Clase OsoImportado
# Campos:
# pos (posición de la base del oso): floatv
# angulo (angulo para rotar): float
# rot (ejes en los que rotar): floatv
# sz (tamaño a escalarse): floatv
# rgb (color del oso): floatv
# nombreArchivo (de qué archivo extraer el oso): str
# lista (que contiene los puntos a dibujar): glList
class OsoImportado:
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
        self.rgb= rgb # Por defecto viene café pardo
        # Lista de los polígonos
        self.nombreArchivo= "Bear_t.stl"
        self.lista= self.generarLista(self.nombreArchivo)
        self.lista= self.corregirAltura(self.lista)
        
    # Métodos
    
    # corregirAltura: glList -> glList
    # Traslada el oso al origen
    def corregirAltura(self, lista1):
        lista2= glGenLists(1)
        glNewList(lista2, GL_COMPILE)
        
        glPushMatrix()
        # Hay que rotarlo porque se dibuja en el eje Z, mirando opuesto a los otros ejes
        glRotatef(90, 0, 1, 0)
        glRotatef(90, -1, 0, 0)
        glCallList(lista1)
        glPopMatrix()
        
        glEndList()
        
        return lista2
    
    # getBlanco: None -> floatv[floatv]
    # Retorna las coordenadas donde, si le llega el alimento, come
    def getBlanco(self):
        return [[self.xpos - 85, self.xpos + 75],
                [self.ypos, self.ypos + 190],
                [self.zpos - 55, self.zpos + 55]]
    
    # getPos: None -> list
    # Retorna la posición del oso
    def getPos(self):
        return [self.xpos, self.ypos, self.zpos]
    
    # setPos: list -> None
    # Setea la posición del objeto en esa posición
    def setPos(self, nuevaPos):
        self.xpos= nuevaPos[0]
        self.ypos= nuevaPos[1]
        self.zpos= nuevaPos[2]
    
    # generarLista:
    # Se ocupa la librería struct para convertir la información de binario en algo utilizable
    # Se extrajo información de https://www.linux.com/blog/python-stl-model-loading-and-display-opengl
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
        archivo= open(nombreArchivo, "rb")
        h= archivo.read(80) # el binario parte con encabezado de 80 caracteres
        
        l= struct.unpack('I', archivo.read(4))[0]
        cuenta= 0
        
        glBegin(GL_TRIANGLES)
        
        while True:
            try:
                p= archivo.read(12) # p de punto
                if len(p) == 12: # la normal del triángulo
                    # Con la notación de a= "hola", "chao" queda a= ("hola", "chao")
                    n= struct.unpack('f',p[0:4])[0], struct.unpack('f',p[4:8])[0], struct.unpack('f',p[8:12])[0]
                p= archivo.read(12)
                if len(p) == 12: # vértice 1
                    v1= struct.unpack('f',p[0:4])[0], struct.unpack('f',p[4:8])[0], struct.unpack('f',p[8:12])[0]
                p= archivo.read(12)
                if len(p) == 12: # vértice 2
                    v2= struct.unpack('f',p[0:4])[0], struct.unpack('f',p[4:8])[0], struct.unpack('f',p[8:12])[0]
                p= archivo.read(12)
                if len(p) == 12: # vértice 3
                    v3= struct.unpack('f',p[0:4])[0], struct.unpack('f',p[4:8])[0], struct.unpack('f',p[8:12])[0]
                    
                puntos= (n, v1, v2, v3)
                if len(puntos) == 4:
                    glNormal3fv(n)
                    glVertex3fv(v1)
                    glVertex3fv(v2)
                    glVertex3fv(v3)
                
                cuenta+= 1
                archivo.read(2)
                
                if len(p) == 0:
                    break
            
            except EOFError: # si llega al final del archivo
                break
        
        glEnd()
        
        archivo.close()
        
        glEndList()
        
        return lista
    
    # dibujar: None -> None
    # Genera el dibujo del oso
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
        
        
        
        
        
        
