# -*- coding: utf-8 -*-

'''
Clase OsoGLUT
Crea un oso en base a figuras GLUT
Guarda los valores en una lista
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

# Clase OsoGLUT
# Campos:
# pos (posición de la base del oso): floatv
# angulo (angulo para rotar): float
# rot (ejes en los que rotar): floatv
# sz (tamaño a escalarse): floatv
# rgb (color del oso): floatv
# lista (que contiene los puntos a dibujar): glList
class OsoGLUT:
    # Constructor
    def __init__(self, pos=[0.0, 0.0, 0.0], angulo= 0.0, rot= None, sz= [1, 1, 1], rgb= [0.5412, 0.4, 0.2588, 1.0]):
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
        self.lista= self.generarLista()
        self.lista= self.corregirAltura(self.lista)
        
    # Métodos
    
    # getBlanco: None -> floatv[floatv]
    # Retorna las coordenadas donde, si le llega el alimento, come
    def getBlanco(self):
        return [[self.xpos - 75, self.xpos + 85],
                [self.ypos, self.ypos + 185],
                [self.zpos - 50, self.zpos + 50]]
    
    # corregirAltura: glList -> glList
    # Traslada el oso al origen
    def corregirAltura(self, lista1):
        lista2= glGenLists(1)
        glNewList(lista2, GL_COMPILE)
        
        glPushMatrix()
        glTranslatef(-45, -15, 0)
        glCallList(lista1)
        glPopMatrix()
        
        glEndList()
        
        return lista2
    
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
    
    def generarLista(self):
        # Se crea la lista
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # Esferas
        # Cabeza
        glPushMatrix()
        glTranslatef(90, 70, 0)
        glutSolidSphere(15, 100, 100)
        glPopMatrix()
        # Oreja derecha
        glPushMatrix()
        glTranslatef(90+15*math.sin(0.5), 70+15*math.cos(0.5), 0+15*math.sin(0.5))
        glutSolidSphere(5, 100, 100)
        glPopMatrix()
        # Oreja izquierda
        glPushMatrix()
        glTranslatef(90+15*math.sin(0.5), 70+15*math.cos(0.5), 0-15*math.sin(0.5))
        glutSolidSphere(5, 100, 100)
        glPopMatrix()
        # Tronco
        glPushMatrix()
        glTranslatef(60, 45, 0)
        glutSolidSphere(25, 100, 100)
        glPopMatrix()
        # Espalda
        glPushMatrix()
        glTranslatef(60, 65, 0)
        glutSolidSphere(15, 100, 100)
        glPopMatrix()
        # Parte trasera
        glPushMatrix()
        glTranslatef(30, 40, 0)
        glutSolidSphere(30, 100, 100)
        glPopMatrix()
        # Cola
        glPushMatrix()
        glTranslatef(5, 55, 0)
        glutSolidSphere(5, 100, 100)
        glPopMatrix()
        
        # Icosaedros
        # Ojo derecho
        glPushMatrix()
        glTranslatef(90+15*math.cos(0.25), 70+15*math.sin(0.25), 0+15*math.cos(0.25)*math.sin(0.25)) # en el borde de la cabeza
        glScalef(3, 3, 3)
        glutSolidIcosahedron() # tiene radio 1.0
        glPopMatrix()
        # Ojo izquierdo
        glPushMatrix()
        glTranslatef(90+15*math.cos(0.25), 70+15*math.sin(0.25), 0-15*math.cos(0.25)*math.sin(0.25)) # en el borde de la cabeza
        glScalef(3, 3, 3)
        glutSolidIcosahedron() # tiene radio 1.0
        glPopMatrix()
        
        # Cubos
        # Pata delantera derecha
        glPushMatrix()
        glTranslatef(90, 45, 15)
        glRotatef(14.5, 0, 0, 1)
        glTranslatef(-10, -10, 0)
        glutSolidCube(20) # lado 20, en el origen
        glPopMatrix()
        # Pata delantera izquierda
        glPushMatrix()
        glTranslatef(90, 45, -15)
        glRotatef(14.5, 0, 0, 1)
        glTranslatef(-10, -10, 0)
        glutSolidCube(20) # lado 20, en el origen
        glPopMatrix()
        # Pata trasera derecha
        glPushMatrix()
        glTranslatef(10, 20, 20)
        glutSolidCube(20) # lado 20, en el origen
        glPopMatrix()
        # Pata trasera derecha
        glPushMatrix()
        glTranslatef(10, 20, -20)
        glutSolidCube(20) # lado 20, en el origen
        glPopMatrix()
        
        # Conos (+ esfera por nariz)
        # Hocico
        glPushMatrix()
        glTranslatef(107, 65, 0)
        glRotatef(60, 0, 0, 1)
        glRotatef(90, -1, 0, 0)
        glutSolidSphere(2, 100, 100)
        glutSolidCone(5, 10, 50, 50)
        glPopMatrix()
        
        glEndList()
        return lista
        
    def dibujar(self):
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        
        glTranslatef(self.xpos, self.ypos, self.zpos)
        glScalef(self.sz[0], self.sz[1], self.sz[2])
        if (self.rot != None):
            glRotatef(self.angulo, self.rot[0], self.rot[1], self.rot[2])
        glColor4fv(self.rgb)
        glCallList(self.lista)
        
        glPopMatrix()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
