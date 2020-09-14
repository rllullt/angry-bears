# -*- coding: utf-8 -*-

'''
Clase Alimento
Es la súper clase para generar los alimentos
Los alimentos se pueden sacar de archivos STL
'''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import struct

# Clase Alimento
# Campos:
# xpos (posición en x): float
# ypos (posición en y): float
# zpos (posicioón en z): float
# sz (factor de escala): floatv
# rgb (color del alimento): floatv
# rugosidad (cómo refleja la luz): str
# nombreArchivo (nombre del archivo del cual extraer los triángulos (STL)): str
# lista (lista para dibujarse en OpenGL): glList
# lanzado (si está siendo lanzado o no): bool
# angulo (útil para dibujar en el lanzamiento dada la rotación): float
# omega (rapidez angular): float
# t (tiempo transcurrido desde el lanzamiento): float
# pos0 (posición inicial del alimento [previa a ser lanzado]): floatv
# v0 (velocidad inicial con que es lanzado el alimento): floatv
# a (aceleración que rige sobre los cuerpos): floatv
class Alimento:
    # Constructor
    def __init__(self, rugosidad, nombreArchivo= None, lista= None, pos= [0.0, 0.0, 0.0], sz= None, rgb= [1, 1, 1, 1.0]):
        self.xpos= pos[0]
        self.ypos= pos[1]
        self.zpos= pos[2]
        self.sz= sz
        self.rgb= rgb
        
        self.rugosidad= rugosidad
        self.nombreArchivo= nombreArchivo
        
        if self.nombreArchivo != None:
            self.lista= self.generarLista(nombreArchivo)
            if self.nombreArchivo == "chocoplate.stl":
                self.lista= self.corregirPosicion(self.lista)
        else:
            self.lista= lista
        
        self.lanzado= False
        self.angulo= 0.0 # grados
        self.omega= 0.2
        self.t= 0.0
        
        self.pos0= [self.xpos, self.ypos, self.zpos]
        self.v0= [0.0, 0.0, 0.0]
        self.a= [0.0, 9.8, 0.0]
        
    # Métodos
    
    # corregirPosicion: glList -> glList
    # Traslada el chocolate al origen
    def corregirPosicion(self, lista1):
        lista2= glGenLists(1)
        glNewList(lista2, GL_COMPILE)
        
        glPushMatrix()
        glTranslatef(-35, -52, 0)
        glCallList(lista1)
        glPopMatrix()
        
        glEndList()
        
        return lista2
    
    # actualizar: float -> None
    # Actualiza la posición según el tiempo
    def actualizar(self, dt):
        if self.lanzado:
            self.angulo+= (self.omega*dt)%360
            self.t+= dt
            self.calcularPosicion()
            
    # calcularPosicion: None -> None
    # Calcula la nueva posición del alimento según la ecuación de itinerario
    def calcularPosicion(self):
        self.xpos= self.pos0[0] - self.v0[0]*self.t/50
        self.ypos= self.pos0[1] + self.v0[1]*self.t/50 - 0.5*self.a[1]*self.t*self.t/25000
        self.zpos= self.pos0[2] + self.v0[2]*self.t/50
    
    # lanzar: floatv -> None
    # "Lanza" al alimento, esto es, setea lanzado como True y
    # le asigna una posición y una velocidad iniciales
    def lanzar(self, v0):
        self.lanzado= True
        self.pos0= [self.xpos, self.ypos, self.zpos]
        self.v0= v0
    
    # getPos: None -> list
    # Retorna la posición del alimento
    def getPos(self):
        return [self.xpos, self.ypos, self.zpos]
    
    # setPos: list -> None
    # Setea la posición del objeto en esa posición
    def setPos(self, nuevaPos):
        self.xpos= nuevaPos[0]
        self.ypos= nuevaPos[1]
        self.zpos= nuevaPos[2]
    
    # generarLista: str -> glList
    # Genera una lista de OpenGL en base a los datos de un archivo STL
    def generarLista(self, nombreArchivo):
        # Puede ser un archivo en binario o en texto, hay que ponerse en los casos
        # Se recicla el código usado para los osos sacados de archivos
        archivo= open(nombreArchivo, "r")
        
        lista= glGenLists(1)
        glNewList(lista, GL_COMPILE)
        
        if self.rugosidad == "r": # rugoso
            glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb)
            glMaterialfv(GL_FRONT, GL_SPECULAR,[0.0,0.0,0.0,1.0])
            glMaterialfv(GL_FRONT, GL_SHININESS, [6.0])
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        else: # brillante
            glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0,0.0,0.0,1.0])
            glMaterialfv(GL_FRONT, GL_DIFFUSE, self.rgb)
            glMaterialfv(GL_FRONT, GL_SPECULAR,[1.0,1.0,1.0,1.0])
            glMaterialfv(GL_FRONT, GL_SHININESS, [15.0])
            glMaterialfv(GL_FRONT, GL_EMISSION, [0.0,0.0,0.0,1.0])
        
        if "solid" in archivo.readline(): # si dice solid en la primera línea, es texto
            
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
            
        else: # viene en binario
            # Como ya se leyó una línea, hay que cerrarlo y abrirlo de nuevo
            archivo.close()
            archivo= open(nombreArchivo, "r")
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
    # Genera el dibujo de la clase Alimento
    def dibujar(self):
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        
        glTranslatef(self.xpos, self.ypos, self.zpos)
        
        if self.lanzado:
            glRotatef(self.angulo, 0, 1, 1)
        
        if self.sz != None:
            glScalef(self.sz[0], self.sz[1], self.sz[2])
        
        glColor4fv(self.rgb)
        
        # Si viene de un STL hay que rotarlo
        if self.nombreArchivo != None:
            # Siempre hay que rotarlo porque se dibuja en el eje Z, mirando opuesto a los otros ejes
            glRotatef(180, 0, 1, 0)
            glRotatef(90, -1, 0, 0)
            
        glCallList(self.lista)
        
        glPopMatrix()
        
        
