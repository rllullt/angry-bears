# -*- coding: utf-8 -*-

''' Inicializador de OpenGL '''

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def init_opengl((ancho, alto)):
    # El reshape
    if alto == 0:
        alto= 1
    
    glViewport(0, 0, ancho, alto)
    
    # La matriz projection controla la perspectiva aplicada a las primitivas
    glMatrixMode(GL_PROJECTION) # los comandos para matriz modifican "projection"
    glLoadIdentity() # inicializa "projection"
    gluPerspective(60.0, 1.0*ancho/alto, 0.1, 20000.0)
    # glOrtho(-w, w, -h, h, 1, 20000)
    
    # La matriz modelview controla la posición de la cámara respecto a las primitivas que se renderizan
    glMatrixMode(GL_MODELVIEW) # los comandos para matriz modifican "modelview"
    glLoadIdentity() # inicializa "modelview"
    
    # El init
    glClearColor(0.5, 0.5, 0.5, 1.0) # color fondo
    # Se habilitan transparencias
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # La cuarta componente del color es la transparencia, alpha
    # alpha= 1 -> lo más opaco
    # alpha= 0 -> lo más transparente
    
    #glShadeModel(GL_SMOOTH)
    
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    #glDepthFunc(GL_LESS)    
        
#    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    
    # normaliza las normales luego del escalamiento.
    glEnable(GL_NORMALIZE)