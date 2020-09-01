import math
import pygame
from sympy import *
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *


pi = math.pi

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
    str_func = input('Enter the function:\n')
    limit = 50
    arc = 0
    k = 2
    l = []
    i = Symbol('i')
    x = Symbol('x')
    R = Symbol('R')
    while True:
        try:
            eval(str_func)
            break
        except NameError as e:
            no_such_name = str(e).split()[1].replace("'", "")
            str_func = str_func.replace(no_such_name, 'sympy.'+no_such_name)

    a = integrate(eval(str_func)*cos(x*i), (x, -R, R), conds='none')
    b = integrate(eval(str_func)*sin(x*i), (x, -R, R), conds='none')
    c = integrate(eval(str_func), (x, -R, R), conds='none')
    
    # print(a.simplify(), '\n', b.simplify())
    R = pi
    print('Integration done')

    ai = lambda i, R: eval(str(a))
    bi = lambda i, R: eval(str(b))
    rad = lambda i: math.sqrt(ai(i, R)**2 + bi(i, R)**2)

    e = lambda i: math.atan2(float(ai(i, R)), float(bi(i, R)))

    list_rad = [rad(i) for i in range(1, limit)]
    scale = (float(c)/(2*R))*10 if c else 10+max(list_rad)/R

    list_e = [e(i) for i in range(1, limit)]
    print('values ready')
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        line((1,0), (-1,0))
        x = center_x_0
        y = center_y_0 + (float(c)/(2*R))/scale
        
        
        for i in range(1, limit):
            prevx = x
            prevy = y
            epoch = list_e[i-1]

            radius = (list_rad[i-1]/R)/scale

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
