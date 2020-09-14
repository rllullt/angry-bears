# -*- coding= utf-8 -*-

'''
Programa para visualizar los modelos del juego, incluye los modelos, la vista y el controlador
'''

# Importación de librerías
from init_pygame import *
from init_opengl import *
import math

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

#################################################################################

# La luz que estará en el programa
def initLuz():
    glLightfv(GL_LIGHT0, GL_POSITION, [1000, 1000, 1000, 1.0])
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
ANCHO= 800
ALTO= 600

os.environ["SDL_VIDEO_CENTERED"]= "1" # centra la pantalla

init_pygame((ANCHO, ALTO), u"Visualización de modelos")
init_opengl((ANCHO, ALTO))
glutInit()

# Color de fondo
glClearColor(0.5, 0.5, 0.5, 1.0)

# Variables del programa
# Rotación
angulo= 0.0 # grados
omega= 0.1 # rad/s

# Posición de la cámara
radioCamara= 2500.0

# Fuentes de luz
glEnable(GL_LIGHTING)
initLuz()
glShadeModel(GL_SMOOTH)

# Colores
glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
glEnable(GL_COLOR_MATERIAL)

# Creación de los modelos
# Se añaden a la lista
listaModelos= []

# Alimento

# Bistec
bistec= Bistec(sz= [10, 10, 10])
listaModelos.append(bistec)
# Chocolate
chocolate= Chocolate(sz= [10, 10, 10])
listaModelos.append(chocolate)
# Maní
mani= Mani(sz= [30, 30, 30])
listaModelos.append(mani)
# Naranja
naranja= Naranja(sz= [150, 150, 150])
listaModelos.append(naranja)
# Pescado
pescado= Pescado(sz= [10, 10, 10])
listaModelos.append(pescado)
# Pera
pera= Pera(sz= [200, 200, 200])
listaModelos.append(pera)

# Honda
honda= Honda(pos= [0, -250, 0], sz= [15, 15, 15])
listaModelos.append(honda)

# Osos

# Oso dibujado en GLUT
osoGLUT= OsoGLUT(pos= [0, -350, 0], sz= [15, 15, 15])
listaModelos.append(osoGLUT)
# Oso común
osoImportado= OsoImportado(pos= [0, -350, 0], sz= [25, 25, 25])
listaModelos.append(osoImportado)
# Oso dibujado a mano
osoMano= OsoMano(pos= [0, -350, 0], sz= [15, 15, 15])
listaModelos.append(osoMano)
# El oso Paddington
osoPaddington= OsoPaddington(pos= [0, -700, 0], sz= [15, 15, 15])
listaModelos.append(osoPaddington)

# Medida del tiempo inicial
t0= pygame.time.get_ticks()

numero_actual= 0
run= True
while run:
    # 0. Control del tiempo
    t1= pygame.time.get_ticks() # tiempo actual
    dt= (t1-t0) # diferencial de tiepmo asociado a la iteración
    t0= t1 # actualizar tiempo inicial para la siguiente iteración
    
    # 1. Manejo de eventos de entrada
    for event in pygame.event.get():
        if event.type == QUIT:
            run= False
        elif event.type == KEYDOWN:
            if event.key == K_q:
                run= False
            elif event.key == K_LEFT:
                if numero_actual <= 0:
                    numero_actual= -numero_actual
                numero_actual= (numero_actual-1) % len(listaModelos)
            elif event.key == K_RIGHT:
                numero_actual= (numero_actual+1) % len(listaModelos)
                
    # 2. Obtener teclas presionadas
    presionadas= pygame.key.get_pressed()
    
    rotarMasY= False
    rotarMenosY= False
    
    if presionadas[K_UP]:
        rotarMasY= True
        rotarMenosY= False
    elif presionadas[K_DOWN]:
        rotarMasY= False
        rotarMenosY= True
    
    # 3. Manejo de la lógica de aplicación
    angulo+= (omega*dt)%360
    
    # 4. Dibujo de elementos
    
    # Limpiar pantalla (búfer de color y de profundidad)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # limpia la pantalla
    
    # Configuración de cámara
    glLoadIdentity()
    gluLookAt(radioCamara, 0.0, radioCamara,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
        # donde:
        # eyeX, eyeY, eyeZ: posición vista (desde dónde se observa)
        # centerX, centerY, centerZ: posición punto de ref. (hacia dónde se apunta)
        # upX, upY, upZ: vector posición en X, Y o Z (cuál hacia arriba)
    
    # Dibujar el modelo actual
    glPushMatrix()
    if rotarMasY:
        glRotate(angulo, -1, 0, 1)
    elif rotarMenosY:
        glRotate(angulo, 1, 0, -1)
    glRotatef(angulo, 0, 1, 0)
    listaModelos[numero_actual].dibujar()
    glPopMatrix()

    pygame.display.flip() # vuelca el dibujo a la pantalla
    pygame.time.wait(1000/30) # ajusta para trabajar a 30 fps
    
pygame.quit()










