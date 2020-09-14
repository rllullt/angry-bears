# -*- coding: utf-8 -*-

'''
Clase OsoMano
Crea un oso con valores "dibujados a mano"
"A mano" significa en base a especificación manual de vértices y polígonos
Guarda los valores en una lista
'''

from OpenGL.GL import *
from OpenGL.GLU import *

import math

# Clase OsoMano
# Campos:
# pos (posición de la base del oso): floatv
# angulo (angulo para rotar): float
# rot (ejes en los que rotar): floatv
# sz (tamaño a escalarse): floatv
# rgb (color del oso): floatvat
# lista (que contiene los puntos a dibujar): glList
class OsoMano:
    # Constructor
    def __init__(self, pos=[0.0, 0.0, 0.0], sz= [1, 1, 1], rgb= [0.5412, 0.4, 0.2588, 1.0]):
        # El color es café pardo
        # Posición
        self.xpos= pos[0]
        self.ypos= pos[1]
        self.zpos= pos[2]
        # Tamaño a escalarse
        self.sz= sz
        # Color
        self.rgb= rgb
        
        # Partes del cuerpo
        self.pata1= self.generarCubo(sz=[20, 40, 20])
        self.pata2= self.generarCubo(sz=[20, 40, 20])
        self.pata3= self.generarCubo(sz=[20, 40, 20])
        self.pata4= self.generarCubo(sz=[20, 40, 20])
        self.cabeza= self.generarCubo(sz=[20, 20, 20])
        self.cola= self.generarCubo(sz=[5, 5, 5])
        self.oreja1= self.generarCubo(sz=[5, 5, 5])
        self.oreja2= self.generarCubo(sz=[5, 5, 5])
        
        self.hocico= self.generarCilindro(sz=[10, 10, 5])
        self.cuerpo= self.generarCilindro(sz=[40, 60, 40])
        
        # Cuerpo final
        self.lista= self.generarLista()
        
    # Métodos
    
    # getBlanco: None -> floatv[floatv]
    # Retorna las coordenadas donde, si le llega el alimento, come
    def getBlanco(self):
        return [[self.xpos - 85, self.xpos + 75],
                [self.ypos, self.ypos + 235],
                [self.zpos - 55, self.zpos + 55]]
    
    # getPos: None -> list
    # Retorna la posición del oso
    def getPos(self):
        return [self.xpos, self.ypos, self.zpos]
    
    # setPos: list -> None
    # Setea la posición del objeto en esa posición
    def setPos(self, nuevaPos):
        self.xpos= nuevaPos[0]
        self.ypos= nuevaPos[1] # estaba a 55
        self.zpos= nuevaPos[2]
    
    # generarCubo: floatv -> glList
    # Crea una lista con un puntos de un cubo de tamaño sz centrado en el origen
    def generarCubo(self, sz= [1, 1, 1]):
        # Vértices
        a= [-0.5, -0.5, 0.5]
        b= [0.5, -0.5, 0.5]
        c= [0.5, 0.5, 0.5]
        d= [-0.5, 0.5, 0.5]
        e= [-0.5, -0.5, -0.5]
        f= [0.5, -0.5, -0.5]
        g= [0.5, 0.5, -0.5]
        h= [-0.5, 0.5, -0.5]
        
        # Normales
        # Para iluminación Smooth hay que sacar promedios de normales
        n1= [0, 0, 1]
        n2= [1, 0, 0]
        n3= [0, 0, -1]
        n4= [-1, 0, 0]
        n5= [0, 1, 0]
        n6= [0, -1, 0]
        
        na= self.promedio(n1, n4, n6)
        nb= self.promedio(n1, n2, n6)
        nc= self.promedio(n1, n2, n5)
        nd= self.promedio(n1, n4, n5)
        ne= self.promedio(n3, n4, n6)
        nf= self.promedio(n3, n2, n6)
        ng= self.promedio(n3, n2, n5)
        nh= self.promedio(n3, n4, n5)
        
        # La lista
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glPushMatrix()
        glScalef(sz[0], sz[1], sz[2])
        
        glBegin(GL_QUADS)
        
        glNormal3fv(na)
        glVertex3fv(a)
        glNormal3fv(nb)
        glVertex3fv(b)
        glNormal3fv(nc)
        glVertex3fv(c)
        glNormal3fv(nd)
        glVertex3fv(d)
        
        glNormal3fv(ne)
        glVertex3fv(e)
        glNormal3fv(nf)
        glVertex3fv(f)
        glNormal3fv(ng)
        glVertex3fv(g)
        glNormal3fv(nh)
        glVertex3fv(h)
        
        glNormal3fv(nb)
        glVertex3fv(b)
        glNormal3fv(nf)
        glVertex3fv(f)
        glNormal3fv(ng)
        glVertex3fv(g)
        glNormal3fv(nc)
        glVertex3fv(c)
                
        glNormal3fv(na)
        glVertex3fv(a)
        glNormal3fv(ne)
        glVertex3fv(e)
        glNormal3fv(nh)
        glVertex3fv(h)
        glNormal3fv(nd)
        glVertex3fv(d)
        
        glNormal3fv(nd)
        glVertex3fv(d)
        glNormal3fv(nc)
        glVertex3fv(c)
        glNormal3fv(ng)
        glVertex3fv(g)
        glNormal3fv(nh)
        glVertex3fv(h)
        
        glNormal3fv(na)
        glVertex3fv(a)
        glNormal3fv(nb)
        glVertex3fv(b)
        glNormal3fv(nf)
        glVertex3fv(f)
        glNormal3fv(ne)
        glVertex3fv(e)
        
        glEnd()

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
    
    # generarLista: None -> glList
    # Genera la lista que contiene los puntos y los polígonos
    def generarLista(self):
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        glShadeModel(GL_SMOOTH)
        
        glColor4fv(self.rgb)
        
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb)
        glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
        glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
        glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        glPushMatrix()
        glTranslatef(20, 20, 10)
        glRotatef(14.5, 0, 0, 1)
        glCallList(self.pata1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(20, 20, -10)
        glRotatef(14.5, 0, 0, 1)
        glCallList(self.pata2)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-20, 20, 10)
        glCallList(self.pata3)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-20, 20, -10)
        glCallList(self.pata4)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(25, 70, 0)
        glCallList(self.cabeza)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0, 40, 0)
        glRotatef(90, 0, 0, 1)
        glCallList(self.cuerpo)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(-30, 50, 0)
        glCallList(self.cola)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(25, 80, 10)
        glCallList(self.oreja1)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(25, 80, -10)
        glCallList(self.oreja2)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(40, 70, 0)
        glRotatef(90, 0, 0, 1)
        glCallList(self.hocico)
        glPopMatrix()
        
        glEndList()
        
        return lista
    
    # promedio: floatv floatv floatv -> floatv
    # Calcula el promedio de 3 puntos con coordenadas en 3D
    def promedio(self, n1, n2, n3):
        xprom= (n1[0]+n2[0]+n3[0])/3.0
        yprom= (n1[1]+n2[1]+n3[1])/3.0
        zprom= (n1[2]+n2[2]+n3[2])/3.0
        return [xprom, yprom, zprom]
    
    def dibujar(self):
        glShadeModel(GL_SMOOTH)
        
        glPushMatrix()
        
        glTranslatef(self.xpos, self.ypos, self.zpos)
        if (self.sz != None):
            glScalef(self.sz[0], self.sz[1], self.sz[2])
        glColor4fv(self.rgb)
        glCallList(self.lista)
        
        glPopMatrix()
