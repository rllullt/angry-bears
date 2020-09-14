# -*- coding= utf-8 -*-

'''
Tarea 2
Autor: Rodrigo Llull Torres
La estructura está basada en la de la clase auxiliar
'''

# Importación de librerías
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import os
from init_pygame import *
from init_opengl import *

import random

from Modelos import *

#################################################################################
# Importación de modelos

# Alimento
from Bistec import Bistec
from Chocolate import Chocolate
from Mani import Mani
from Naranja import Naranja
from Pera import Pera
from Pescado import Pescado

# Honda
from Honda import Honda

# Osos
from OsoGLUT import OsoGLUT
from OsoImportado import OsoImportado
from OsoMano import OsoMano
from OsoPaddington import OsoPaddington

# Escenario
from Escenario import Escenario

#################################################################################

# La luz que estará en el programa
def initLuz():
    glLightfv(GL_LIGHT0, GL_POSITION, [-500, 1500, 500, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT , [0.5, 0.5, 0.5, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE , [1.0, 1.0, 1.0, 1.0])
 
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.0)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.0)
 
    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [-1.0, -1.0, -1.0])
    glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 0.0)
 
    glEnable(GL_LIGHT0)

#################################################################################

# Programa

#################################################################################

# Se crea la vista
ANCHO= 800
ALTO= 600

# Se inicializan Pygame y OpenGL
os.environ["SDL_VIDEO_CENTERED"]= "1" # centra la pantalla
init_pygame((ANCHO, ALTO), "Hungry Bears")
init_opengl((ANCHO, ALTO))
glutInit()
print u"¡Bienvenido a Hungry Bears!"
print ""

# Color de fondo
glClearColor(0.3647, 0.6078, 0.6078, 1.0) # azul pastel

# Colores
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
glEnable(GL_COLOR_MATERIAL)

# Fuentes de luz
glEnable(GL_LIGHTING)
initLuz()
glShadeModel(GL_SMOOTH)

# Temporizador (para el tiempo de los rayos)
t0= pygame.time.get_ticks()

#################################################################################

# Se crean los modelos

# Listas de objetos
osos= []
alimentos= []
enHonda= []
lanzados= []

print u"Cargando escenario..."
# Crea el escenario
escenario= Escenario(sz= [60, 60, 60])

print u"Cargando osos..."
# Se crean los 4 osos
osos.append(OsoGLUT(sz= [2.5, 2.5, 2.5]))
osos.append(OsoImportado(sz= [5, 5, 5]))
osos.append(OsoMano(sz= [3, 3, 3]))
osos.append(OsoPaddington(sz= [2, 2, 2]))

print u"Cargando alimentos..."
# Se crean los 6 alimentos
alimentos.append(Bistec(sz= [0.7, 0.7, 0.7]))
alimentos.append(Chocolate())
alimentos.append(Mani())
alimentos.append(Naranja(sz= [13, 13, 13]))
alimentos.append(Pera(sz= [13, 13, 13]))
alimentos.append(Pescado(sz= [0.7, 0.7, 0.7]))

print u"Cargando honda..."
# Se crea la honda
honda= Honda(pos= escenario.getPosHonda(), sz= [3, 3, 3])

# Posición de la cámara (desde dónde mira)
a= honda.getPos()
b= 200
cam_x= a[0] + b
cam_y= a[1] + b/2
cam_z= a[2]

cam_at_x= -10000
cam_at_y= 0.0
cam_at_z= 0.0

# Variables del programa
v= 40.0
# Puntuación del jugador:
puntuoTurnoAnterior= False
puntuacion= 0

posicionarAlimento(honda, alimentos, enHonda)
posicionarOsos(escenario, osos)

print u"¡Listo!"
print ""

# Bucle de aplicación
while True:
    # Manejo del tiempo
    t1= pygame.time.get_ticks() # tiempo actual
    dt= (t1-t0) # diferencial de tiepmo asociado a la iteración
    t0= t1 # actualizar tiempo inicial para la siguiente iteración

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_q:
                exit()
            elif event.key == K_SPACE:
                lanzarAlimento(honda, alimentos, enHonda, lanzados, v, cam_at_x, cam_at_y, cam_at_z)
        elif event.type == KEYUP:
            if event.key == K_a or event.key == K_z:
                print u"Velocidad: "+str(v)

    presionadas= pygame.key.get_pressed()
    
    # Posición de la cámara en la honda
    x, y, z= cam_x, cam_y, cam_z

    if presionadas[K_UP]:
        cam_at_y+= 20
    elif presionadas[K_DOWN]:
        cam_at_y-= 20
    elif presionadas[K_LEFT]:
        cam_at_z+= 20
    elif presionadas[K_RIGHT]:
        cam_at_z-= 20
    
    elif presionadas[K_a]:
        if v <= 90:
            v+= 0.1
    elif presionadas[K_z]:
        if 0 <= v:
            v-= 0.1
            
    elif presionadas[K_c]:
        if lanzados != []:
            pos= lanzados[0].getPos()
            x, y, z= pos[0] + 150, pos[1] - 50, pos[2]

    # Se actualiza el modelo según el tiempo de la aplicación
    puntuacion, puntuoTurnoAnterior= actualizar(dt, lanzados, osos, puntuacion, puntuoTurnoAnterior)
        
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # limpia la pantalla

    # Configuración de cámara
    glLoadIdentity()
    gluLookAt(x, y, z,
              cam_at_x, cam_at_y, cam_at_z,
              0.0, 1.0, 0.0)
        # donde:
        # eyeX, eyeY, eyeZ: posición vista (desde dónde se observa)
        # centerX, centerY, centerZ: posición punto de ref. (hacia dónde se apunta)
        # upX, upY, upZ: vector posición en X, Y o Z (cuál hacia arriba)



    # Se dibuja el modelo
    honda.dibujar()
    for alimento in lanzados:
        alimento.dibujar()
    for alimento in enHonda:
        alimento.dibujar()
    for oso in osos:
        oso.dibujar()
    escenario.dibujar()
    
    if osos == [] or (alimentos == [] and enHonda == [] and lanzados == []):
        break

    # Se vuelca en la pantalla
    pygame.display.flip()

print ""
print u"¡Fin del juego!"
print u"Puntuación final: "+str(puntuacion)

pygame.quit()
