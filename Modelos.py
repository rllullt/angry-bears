# -*- coding= utf-8 -*-

'''
Archivo que contiene las funciones para trabajar con modelos
'''

# Importación de librerías
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import random
import math

# posicionarAlimento: Honda list(Alimento) list(Alimento) -> None
# Posiciona un alimento sobre la honda para ser lanzado
def posicionarAlimento(honda, alimentos, enHonda):
    if alimentos != []:
        pos= honda.getPos()
        r= random.randint(0, len(alimentos)-1)
        aLanzar= alimentos.pop(r)
        aLanzar.setPos(pos)
        enHonda.append(aLanzar)
        
# posicionarOsos: Escenario list(Oso) -> None
# Posiciona todos los osos en el escenario
def posicionarOsos(escenario, osos):
    for oso in osos:
        pos= escenario.getPosOso()
        oso.setPos(pos)

# lanzarAlimento: Honda list(Alimento) list(Alimento) float float float float -> None
# Dispara a algún alimento de la honda, y posiciona otro en ella si quedan
def lanzarAlimento(honda, alimentos, enHonda, lanzados, v, cam_at_x, cam_at_y, cam_at_z):
    if enHonda != []:
        alimento= enHonda.pop()
        theta= -math.atan((cam_at_y-honda.getPos()[1]) / cam_at_x)
        phi= -math.atan(cam_at_z / cam_at_x)
        v_x= v*math.cos(theta)*math.cos(phi)
        v_y= v*math.sin(theta)
        v_z= v*math.cos(theta)*math.sin(phi)
        alimento.lanzar([v_x, v_y, v_z])
        lanzados.append(alimento)
        posicionarAlimento(honda, alimentos, enHonda)
        
# actualizar: float list(Alimento) list(Oso) float bool -> None
# Actualiza los elementos que pueden haber cambiado, y elimina aquellos que cumplen las condiciones.
# También revisa colisiones.
# Además, actualiza la puntuación y regula los turnos.
# Retorna la nueva puntuación y si puntuó el turno anterior
def actualizar(dt, lanzados, osos, puntuacion, puntuoTurnoAnterior):
    for alimento in lanzados:
        alimento.actualizar(dt)
        pos_alimento= alimento.getPos()
        if (pos_alimento[0] <= -200 or pos_alimento[1] <= 0): # imposible que le haya pegado a algún oso:
            lanzados.remove(alimento)
            print u"Puntuación: "+str(puntuacion)
            if puntuoTurnoAnterior:
                puntuoTurnoAnterior= False
            continue
        
        # Si el alimento aun está en la escena, detectar colisiones
        for oso in osos:
            blanco= oso.getBlanco()
            if (blanco[0][0] <= pos_alimento[0] <= blanco[0][1]
               ) and (blanco[1][0] <= pos_alimento[1] <= blanco[1][1]
                     ) and (blanco[2][0] <= pos_alimento[2] <= blanco[2][1]): # colisión
                lanzados.remove(alimento)
                if puntuoTurnoAnterior:
                    puntuacion+= 15
                else: # no puntuo en el turno anterior
                    puntuacion+= 10
                print u"Puntuación: "+str(puntuacion)
                puntuoTurnoAnterior= True
                osos.remove(oso)
    
    return puntuacion, puntuoTurnoAnterior

