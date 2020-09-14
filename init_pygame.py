# -*- coding: utf-8 -*-

''' Inicializador de Pygame '''

import pygame
from pygame.locals import *

def init_pygame((ancho, alto), title=""):
    pygame.init()
    pygame.display.set_mode((ancho, alto), OPENGL|DOUBLEBUF)
    pygame.display.set_caption(title)