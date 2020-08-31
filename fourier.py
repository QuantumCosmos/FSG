from sympy.abc import x
import inspect
import math
from sympy import integrate, Symbol, exp, cos, sin
import scipy.integrate
from time import sleep, time
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *


pi = math.pi
time_lst = []
pos_list_a = []
pos_list_b = []

display = (800,500)
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
    for i in range(slides+1, -1, -1):    
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
    glVertex2f(x, y);
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
    str_func = input('Enter the function:\n')

    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    limit = 50
    arc = 0
    k = 1
    l = []
    r = pi
    i = Symbol('i')
    x = Symbol('x')
    R = Symbol('R')
    R = r
    fa = eval(str_func)*cos(x*i)
    fb = eval(str_func)*sin(x*i)
    a = integrate(fa, (x, -R, R), conds='none')
    b = integrate(fb, (x, -R, R), conds='none')
    print(a, b)
    print('Integration done')

    ai = lambda i: eval(str(a))
    bi = lambda i: eval(str(b))
    rad = lambda i: math.sqrt(ai(i)**2 + bi(i)**2)

    e = lambda i: math.atan2(float(ai(i)), float(bi(i)))

    list_rad = [rad(i) for i in range(1, limit)]
    list_e = [e(i) for i in range(1, limit)]
    print('values ready')


    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        line((1,0), (-1,0))
        x = center_x_0
        y = center_y_0
        
        
        for i in range(1, limit):
            prevx = x
            prevy = y
            epoch = list_e[i-1]

            radius = list_rad[i-1]*0.1/r

            x += radius/adjustX * math.cos(-i*k*arc+epoch)
            y += radius/adjustY * math.sin(-i*k*arc+epoch)
            circle(radius, prevx, prevy, i, epoch)
            point(prevx,prevy)

            line((prevx, prevy), (x, y))

        l.insert(0,y)
        if len(l)>300:
            l.pop()
        point(0, l[0], 5)
        line((0, l[0]), (x, y))
        line((0, l[0]), (0, 0), 0.5)
        line((x, 0), (x, y), 0.5)
        
        arc += inc

        curve(l)
        
        pygame.display.flip()



main()
