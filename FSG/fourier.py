import math
import pygame
# from sympy import Symbol
from scipy import *
import numpy as np
from time import time
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import scipy.integrate
# import warnings
# warnings.filterwarnings("error", category=DeprecationWarning)


math_tray = {
    "sinh": "np.sinh",
    "cosh": "np.cosh",
    "tanh": "np.tanh",
    "sin": "np.sin",
    "cos": "np.cos",
    "tan": "np.tan",
    "log": "np.log",
    "exp": "np.exp",
}

pi = math.pi

display = (800, 500)
adjustX = display[0]/min(display)
adjustY = display[1]/min(display)


center_x_0 = -0.55
center_y_0 = 0

inc = 0.075


def circle(radius, posx, posy, n, epoch=0):
    slides = 100
    glLineWidth(0.05)
    glColor3f(0.4, 0.4, 0.4)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glBegin(GL_LINE_STRIP)
    x = y = 0
    for i in range(1, slides):
        x = (radius/adjustX * math.cos(n*2*pi*i/slides + epoch) + posx)
        y = (radius/adjustY * math.sin(n*2*pi*i/slides + epoch) + posy)
        glVertex2f(x, y)
    glEnd()
    glColor3f(1.0, 1.0, 1.0)


def point(x, y, size=2.0):
    glEnable(GL_POINT_SMOOTH)
    glEnable(GL_BLEND)
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def line(a, b, width=1):
    glLineWidth(width)
    glBegin(GL_LINES)
    glVertex2f(a[0], a[1])
    glVertex2f(b[0], b[1])
    glEnd()
    glLineWidth(1)


def curve(l):
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LINE_SMOOTH)
    glBegin(GL_LINE_STRIP)
    for i in range(len(l)):
        glVertex2f(i*inc*0.05, l[i])
    glEnd()


def main():
    pygame.init()
    inp = input(
        'Enter the function with limits (separated by space):\n').split(' ')
    str_func = inp.pop(0)
    lim = 50
    arc = 0
    k = 2
    l = []
    for i in math_tray:
        if i in str_func:
            str_func = str_func.replace(i, math_tray[i]).replace("np.np.", "np.")

    uL = eval(max(inp))
    lL = eval(min(inp))
    temp = str_func
    max_val = float(eval(temp.replace('x', str(uL))))

    R = uL-lL
    ai = lambda n: scipy.integrate.quad(lambda x: (2/R)*eval(str_func)*np.cos(2*pi*x*n/R), lL, uL)[0]
    bi = lambda n: scipy.integrate.quad(lambda x: (2/R)*eval(str_func)*np.sin(2*pi*x*n/R), lL, uL)[0]
    c = scipy.integrate.quad(lambda x: (2/R)*eval(str_func), lL, uL)[0]


    def rad(i):
        a1 = (ai(i))**2
        b1 = (bi(i))**2
        return math.sqrt(a1 + b1)

    def e(i): return math.atan2(float(ai(i)), float(bi(i)))

    list_rad = []
    list_e = []
    max_r_for_inf_cond = 0.5
    for i in range(1, lim+1):
        r = rad(i)
        if r > 1e+5:
            r = max_r_for_inf_cond
        list_rad.append(r)
        list_e.append(float(e(i)))

    scale = 2*(max(list_rad)+list_rad[0])

    list_rad = [float(list_rad[i]/scale) for i in range(len(list_rad))]

    print('Values Ready!')

    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        line((1, 0), (-1, 0))
        x = center_x_0
        y = center_y_0 + (c/2)/scale

        for i in range(1, len(list_rad)+1):
            prevx = x
            prevy = y
            epoch = list_e[i-1]

            radius = (list_rad[i-1])
            x += radius/adjustX * math.cos(-i*k*arc+epoch)
            y += radius/adjustY * math.sin(-i*k*arc+epoch)

            circle(radius, prevx, prevy, i, epoch)
            point(prevx, prevy)

            line((prevx, prevy), (x, y))

        l.insert(0, y)
        if len(l) > 300:
            l.pop()
        point(0, l[0], 5)
        line((0, l[0]), (x, y))
        line((0, l[0]), (0, 0), 0.5)
        line((x, 0), (x, y), 0.5)

        arc += inc

        curve(l)

        pygame.display.flip()


main()
