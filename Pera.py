# -*- coding: utf-8 -*-

'''
Clase Pera
Crea un Alimento Pera con GLUT
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math

from Alimento import Alimento

# Clase Pera
# Campos:
# rugosidad (si es rugoso o brillante): str
# rgb (color en rgb): floatv
# lista (lista que contiene la lista del alimento): glList
class Pera(Alimento):
    # Constuctor
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= ([0.2392, 0.3922, 0.1765, 1.0], [0.3490, 0.2078, 0.1216, 1.0])):
        # Colores: verde helecho, pardo corzo
        self.rugosidad= "r"
        
        # El color para dibujar las diferentes partes
        self.rgb= rgb
        
        self.piezasTallo= [self.generarCilindro(), self.generarCilindro()]
        
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
    # Retorna una lista de OpenGL con los puntos de la pera
    def generarLista(self):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # El pomo
        glColor4fv(self.rgb[0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb[0])
        
        glPushMatrix()
        glTranslatef(0, 2.5, 0)
        glutSolidSphere(2.5, 100, 100)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 5, 0)
        glScalef(1.5, 2, 1.5)
        glutSolidSphere(1, 100, 100)
        glPopMatrix()
        
        # El tallo
        glColor4fv(self.rgb[1])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb[1])
        
        glPushMatrix()
        glTranslatef(0, 7.4, 0)
        glScalef(0.3, 0.75, 0.3)
        glCallList(self.piezasTallo[0])
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 7.5, 0)
        glRotatef(45, 0, 0, 1)
        glScalef(0.3, 0.5, 0.3)
        glTranslatef(0, 0.5, 0)
        glCallList(self.piezasTallo[1])
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
        