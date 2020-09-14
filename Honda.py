# -*- coding: utf-8 -*-

'''
Clase Honda
Crea una honda que se usará para lanzarle la comida a los osos
'''

from OpenGL.GL import *
from OpenGL.GLU import *

import math

# Clase Honda
# Campos:
# xpos (posición en x): float
# ypos (posición en y): float
# zpos (posicioón en z): float
# sz (factor de escala): floatv
# rgb (color): floatv
# base (lista con polígonos de la base): glList
# lado1 (lista con polígonos de ese lado): glList
# lado2 (lista con polígonos de ese lado): glList
# lista (lista para dibujarse en OpenGL): glList
class Honda:
    # Constructor:
    def __init__(self, pos= [0.0, 0.0, 0.0], sz= None, rgb= [0.5843, 0.3725, 0.1255, 1.0]):
        # Color marrón
        self.xpos= pos[0]
        self.ypos= pos[1] - 200
        self.zpos= pos[2]
        self.sz= sz
        self.rgb= rgb
        
        self.base= self.generarCilindro(sz= [20, 40, 20])
        self.lado1= self.generarCilindro(sz= [20, 40, 20])
        self.lado2= self.generarCilindro(sz= [20, 40, 20])
        
        self.lista= self.generarLista()
        
    # Métodos
    
    # getPos: None -> floatv
    # Retorna las coordenadas donde ubicar el alimento para lanzarlo
    def getPos(self):
        if self.sz != None:
            return [self.xpos, self.ypos*self.sz[1], self.zpos]
        return [self.xpos, self.ypos, self.zpos]
    
    # generarLista: None -> glList
    # Genera la lista de la onda para dibujar
    def generarLista(self):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glShadeModel(GL_SMOOTH)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # Base
        glPushMatrix()
        glTranslate(0, 20, 0)
        glCallList(self.base)
        glPopMatrix()
        
        # Lados
        glPushMatrix()
        glTranslate(0, 40, 0)
        glRotatef(45, 1, 0, 0)
        glTranslatef(0, 20, 0)
        glCallList(self.lado1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(0, 40, 0)
        glRotatef(45, -1, 0, 0)
        glTranslatef(0, 20, 0)
        glCallList(self.lado2)
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
    
    # dibujar: None -> None
    # Dibuja a la honda en la posición correspondiente
    def dibujar(self):
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        
        glTranslatef(self.xpos, self.ypos, self.zpos)
        
        if self.sz != None:
            glScalef(self.sz[0], self.sz[1], self.sz[2])
        
        glColor4fv(self.rgb)
            
        glCallList(self.lista)
        
        glPopMatrix()
        