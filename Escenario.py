# -*- coding: utf-8 -*-

'''
Clase Escenario
Genera el escenario donde se pondrán las figuras
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

# Clase Escenario
# Campos:
# plataforma1 (plataforma superior donde se ubicarán los osos): glList
# plataforma2 (plataforma inferior donde se ubicarán los osos): glList
# plataforma3 (plataforma donde se ubicará la honda): glList
# suelo_con_rio (losa del terreno donde se ubicarán las plataformas): glList
# sz (factor de escalamiento): floatv
# lista (lista de OpenGL que integra todo el escenario): glList
class Escenario:
    # Constructor
    def __init__(self, sz= [1, 1, 1]):
        # Se ubica siempre en el origen, orientado en el eje Y
        self.plataforma1= self.generarConoTruncado([10, 7.5], [5, 3.75], 5, 5)
        self.plataforma2= self.generarConoTruncado([20, 15], [15, 11.25], 5, 0)
        self.plataforma3= self.generarConoTruncado([10, 7.5], [5, 3.75], 5, 0)
        self.suelo_con_rio= self.generarSueloConRio()
        
        self.sz= sz
        
        self.lista= self.generarLista()

    # Métodos
    
    # getPosOso; None -> list
    # Retorna una posición al azar para ubicar un oso
    def getPosOso(self):
        r= random.randint(1, 2)
        ang= random.uniform(0, math.pi)
        if r == 2: # plataforma 1 (aunque sea contraintuitivo)
            x= random.uniform(0, 3.75*math.sin(ang))
            z= random.uniform(0, 5*math.cos(ang))
        else: # r= 1, plataforma 2
            x= random.uniform(7.5*math.sin(ang), 11.25*math.sin(ang))
            z= random.uniform(15*math.cos(ang), 15*math.cos(ang))
        error=2.5 # error que se produce al cargar, no se sabe por qué
        return [x*self.sz[0], (r*5 - error)*self.sz[1], z*self.sz[2]]
    
    # getPosHonda: None -> list
    # Retorna la posición donde se debe ubicar la honda
    def getPosHonda(self):
        return [45*self.sz[0], 5*self.sz[1], 0]
    
    # generarConoTruncado: v(float, float) v(float, float) float -> glList
    # Genera una lista de un cono truncado centrado en el origen
    # con una lista para los radios de la cara inferior y otra para la cara superior
    def generarConoTruncado(self, radiosAbajo, radiosArriba, altura, y_base):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glPushMatrix()
        
        rgb= [0.2078, 0.4078, 0.1765, 1.0] # verde hierba
        glColor4fv(rgb)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        glTranslatef(0, y_base, 0)
        
        puntosCirculoAbajo= []
        normalesCirculoAbajo= [] # serán normales en las aristas inferiores que se promediarán
                        # con las normales de las aristas superiores
        
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f= (0, -1, 0)
        glVertex3f= (0, -altura/2.0, 0)
        k= 60
        angulo= 2*math.pi/k
        for i in range(k+1):
            ang_i= angulo*i
            p= [radiosAbajo[0]*math.cos(ang_i), -altura/2.0, -radiosAbajo[1]*math.sin(ang_i)]
            puntosCirculoAbajo.append(p)
            n= [radiosAbajo[0]*math.cos(ang_i-angulo/2), -altura/2.0, -radiosAbajo[1]*math.sin(ang_i-angulo/2)]
            normalesCirculoAbajo.append(n)
            glVertex3fv(p)
        glEnd()
        
        puntosCirculoArriba= []
        normalesCirculoArriba= []
        
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f= (0, 1, 0)
        glVertex3f= (0, altura/2.0, 0)
        angulo= 2*math.pi/k
        for i in range(k+1):
            ang_i= angulo*i
            p= [radiosArriba[0]*math.cos(ang_i), altura/2.0, -radiosArriba[1]*math.sin(ang_i)]
            puntosCirculoArriba.append(p)
            n= [radiosArriba[0]*math.cos(ang_i-angulo/2), altura/2.0, -radiosArriba[1]*math.sin(ang_i-angulo/2)]
            normalesCirculoArriba.append(n)
            glVertex3fv(p)
        glEnd()
        
        normalesPromedio= []
        for i in range(len(normalesCirculoAbajo)):
            normalesPromedio.append(self.promedio(normalesCirculoAbajo[i], normalesCirculoArriba[i]))
        
        glBegin(GL_QUADS)
        for i in range(len(puntosCirculoAbajo) - 1):
            glNormal3fv(normalesPromedio[i])
            glVertex3fv(puntosCirculoAbajo[i])
            glVertex3fv(puntosCirculoAbajo[i+1])
            glVertex3fv(puntosCirculoArriba[i+1])
            glVertex3fv(puntosCirculoArriba[i])
        glEnd()
        
        glPopMatrix()
        
        glEndList()
        
        return lista
    
    # promedio: floatv floatv -> floatv
    # Calcula el promedio de 2 puntos con coordenadas en 3D
    def promedio(self, n1, n2):
        xprom= (n1[0]+n2[0])/3.0
        yprom= (n1[1]+n2[1])/3.0
        zprom= (n1[2]+n2[2])/3.0
        return [xprom, yprom, zprom]
    
    # generarLista: None -> glList
    # Genera la lista con los puntos de la escena
    def generarLista(self):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glCallList(self.plataforma1)
        glCallList(self.plataforma2)
        glCallList(self.suelo_con_rio)
        glPopMatrix()
        
        glPushMatrix()
        glRotatef(90, 0, 1, 0)
        glTranslatef(0, 0, 45)
        glCallList(self.plataforma3)
        glPopMatrix()
        
        glEndList()
        
        return lista
    
    # generarSueloConRio: None -> glList
    # Genera una lista con los puntos para el suelo y el río
    # El río sigue una trayectoria sinusoidal
    def generarSueloConRio(self):
        n= 5
        rio= self.generarRio(n)
        
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        rgb= [0.2078, 0.4078, 0.1765, 1.0] # verde hierba
        glColor4fv(rgb)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        # El cuadrado base será 10 veces más grande que las plataformas, esto es, de lado 1000
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        glVertex3f(-1000, 0, 1000)
        glVertex3f(1000, 0, 1000)
        glVertex3f(1000, 0, -1000)
        glVertex3f(-1000, 0, -1000)
        glEnd()
        
        # El río tiene forma sinusoidal y pasa frente a las plataformas
        # Además está rotado 14.5 grados en torno a -Y
        rgb= [0.1451, 0.4275, 0.4824, 1.0] # azul agua
        glColor4fv(rgb)
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[1.0,1.0,1.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [15.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        glPushMatrix()
        glTranslatef(10, 2, 30)
        glScalef(5, 1, 1)
        glRotatef(14.5, 0, -1, 0)
        glCallList(rio)
        glPopMatrix()
        
        glEndList()
        
        return lista
    
    # generarOscilacion: None -> glList
    # Retorna una oscilación de seno
    def generarOscilacion(self, n):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        anchoMeandro= 5
        
        puntosRio1= [] # guardará los puntos del río
        puntosRio2= []
        
        for i in range(n): # de 0 a 99, 100 puntos
            j= 2*math.pi/n # 1 ciclo

            if (0 <= j*i <= math.pi/2):
                puntosRio1.append([j*i, 0, 2.5 + anchoMeandro*math.sin(j*i)]) # x, f(x)=z
                puntosRio2.append([j*i+5, 0, -2.5 + anchoMeandro*math.sin(j*i)])

            elif (math.pi/2 < j <= math.pi):
                puntosRio1.append([j*i, 0, 2.5 + anchoMeandro*math.sin(j*i)]) # x, f(x)=z
                puntosRio2.append([j*i-5, 0, -2.5 + anchoMeandro*math.sin(j*i)])

            elif (math.pi/2 < j <= 3*math.pi/2):
                puntosRio1.append([j*i+5, 0, 2.5 + anchoMeandro*math.sin(j*i)]) # x, f(x)=z
                puntosRio2.append([j*i, 0, -2.5 + anchoMeandro*math.sin(j*i)])

            else: # 3*math.pi/2 < j <= 2*math.pi
                puntosRio1.append([j*i, 0, 2.5 + anchoMeandro*math.sin(j*i)]) # x, f(x)=z
                puntosRio2.append([j*i-5, 0, -2.5 + anchoMeandro*math.sin(j*i)])
                
        glBegin(GL_TRIANGLE_STRIP)
        
        for i in range(len(puntosRio1)):
            glNormal3f(0, 1, 0)
            glVertex3fv(puntosRio2[i])
            glVertex3fv(puntosRio1[i])
            
        glEnd()
                
        glEndList()
        
        return lista
    
    # generarRio: int -> glList
    # Retorna un rio de n oscilaciones
    def generarRio(self, n):
        # Guarda oscilaciones
        oscilaciones= []
        for i in range(n): # n oscilaciones
            oscilaciones.append(self.generarOscilacion(20*n))
        
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        for i in range(n):
            glPushMatrix()
            glTranslatef(-n*math.pi + 2*math.pi*i, 0, 0)
            glCallList(oscilaciones[i])
            glPopMatrix()
        
        glEndList()
        
        return lista
    
    # dibujar: None -> None
    # Dibuja el objeto
    def dibujar(self):
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        glScalef(self.sz[0], self.sz[1], self.sz[2])
        glCallList(self.lista)
        glPopMatrix()