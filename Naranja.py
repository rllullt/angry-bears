# -*- coding: utf-8 -*-

'''
Clase Naranja
Genera una Naranja de clase Alimento
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

from Alimento import Alimento

# Clase Naranja
# Campos:
# rugosidad (si es rugoso o brillante): str
# rgb (color en rgb): floatv
# tallo (lista que contiene los puntos para el tallo): glList
# lista (lista que contiene la lista del alimento): glList
class Naranja(Alimento):
    # Constructor:
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= ([0.9255 , 0.4863, 0.1490, 1.0], [0.8941, 0.6275, 0.0627, 1.0])):
        # Colores: naranja intenso, amarillo maíz
        self.rugosidad= "r"
        
        # El color para dibujar las diferentes partes
        self.rgb= rgb
        
        self.tallo= self.generarCilindro()
        
        self.lista= self.generarLista()
        self.lista= self.corregirAltura(self.lista)
        
        Alimento.__init__(self, self.rugosidad, None, self.lista, pos, sz, rgb[0])
        
    # Métodos
    
    # corregirAltura: glList -> glList
    # Traslada la fruta al origen
    def corregirAltura(self, lista1):
        lista2= glGenLists(1)
        glNewList(lista2, GL_COMPILE)
        
        glPushMatrix()
        glTranslatef(0, -2, 0)
        glCallList(lista1)
        glPopMatrix()
        
        glEndList()
        
        return lista2
    
    # generarLista: None -> glList
    # Retorna una lista con los puntos y polígonos a dibujar
    def generarLista(self):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.2,0.2,0.2,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [10.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # Pomo
        glColor4fv(self.rgb[0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb[0])
        
        glPushMatrix()
        glTranslatef(0, 1.5, 0)
        glutSolidSphere(1.5, 100, 100)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 3.5, 0)
        glutSolidSphere(3, 100, 100)
        glPopMatrix()
        
        # Tallo
        glColor4fv(self.rgb[1])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb[1])
        
        glPushMatrix()
        glTranslatef(0, 6.5, 0)
        glScalef(0.5, 0.5, 0.5)
        glCallList(self.tallo)
        glPopMatrix()
        
        glEndList()
        
        return lista
        
    # generarCilindro: v(float, float, float) -> glList
    # Genera una lista de un cilindro centrado en el origen de tamaño 1, orientado en Y
    def generarCilindro(self, sz=[1, 1, 1]):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glPushMatrix()
        glScalef(sz[0], sz[1], sz[2])
        
        puntosCirculoAbajo= []
        normales= [] # serán normales en las caras
        
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f= (0, -1, 0)
        glVertex3f= (0, -0.5, 0)
        radio= 0.5
        k= 60
        angulo= 2*math.pi/k
        for i in range(k+1):
            ang_i= angulo*i
            p= [radio*math.cos(ang_i), -0.5, -radio*math.sin(ang_i)]
            puntosCirculoAbajo.append(p)
            n= [radio*math.cos(ang_i-angulo/2), 0, -radio*math.sin(ang_i-angulo/2)]
            normales.append(n)
            glVertex3fv(p)
        glEnd()
        
        puntosCirculoArriba= []
        
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f= (0, 1, 0)
        glVertex3f= (0, 0.5, 0)
        radio= 0.5
        angulo= 2*math.pi/k
        for i in range(k+1):
            ang_i= angulo*i
            p= [radio*math.cos(ang_i), 0.5, -radio*math.sin(ang_i)]
            puntosCirculoArriba.append(p)
            glVertex3fv(p)
        glEnd()
        
        glBegin(GL_QUADS)
        for i in range(len(puntosCirculoAbajo) - 1):
            glNormal3fv(normales[i])
            glVertex3fv(puntosCirculoAbajo[i])
            glVertex3fv(puntosCirculoAbajo[i+1])
            glVertex3fv(puntosCirculoArriba[i+1])
            glVertex3fv(puntosCirculoArriba[i])
        glEnd()
        
        glPopMatrix()
        
        glEndList()
        
        return lista