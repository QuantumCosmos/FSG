import pygame
import numpy as np
from draw import drawGL
from scipy.integrate import quad
from math import pi, atan2, sqrt, sin, cos
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT



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


display = (800, 500)


center = (-0.55, 0)
max_r_for_inf_cond = 0.5

inc = 0.075


def main():
    pygame.init()
    inp = input('Enter the function with limits (separated by space):\n').split(' ')
    str_func = inp.pop(0)
    lim = 50
    arc = 0
    k = 2
    l = []
    for i in math_tray:
        if i in str_func:
            str_func = str_func.replace(i, math_tray[i]).replace("np.np.", "np.")

    lL = eval(inp[0])
    uL = eval(inp[1])
    temp = str_func
    max_val = float(eval(temp.replace('x', str(uL))))

    R = uL-lL
    ai = lambda n: quad(lambda x: (2/R)*eval(str_func)*np.cos(2*pi*x*n/R), lL, uL)[0]
    bi = lambda n: quad(lambda x: (2/R)*eval(str_func)*np.sin(2*pi*x*n/R), lL, uL)[0]
    c = quad(lambda x: (2/R)*eval(str_func), lL, uL)[0]


    def rad(i): return sqrt((ai(i))**2 + (bi(i))**2)

    def e(i): return atan2(float(ai(i)), float(bi(i)))

    list_rad = []
    list_e = []
    for i in range(1, lim+1):
        r = rad(i)
        if r > 1e+5:
            r = max_r_for_inf_cond
        list_rad.append(r)
        list_e.append(float(e(i)))

    scale = 2*(max(list_rad)+list_rad[0])

    list_rad = [float(list_rad[i]/scale) for i in range(len(list_rad))]

    print('Values Ready!')

    adjustX = display[0]/min(display)
    adjustY = display[1]/min(display)
    draw = drawGL(adjustX, adjustY, inc)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw.line((1, 0), (-1, 0))
        x = center[0]
        y = center[1] + (c/2)/scale

        for i in range(1, len(list_rad)+1):
            prevx = x
            prevy = y
            epoch = list_e[i-1]

            radius = (list_rad[i-1])
            x += radius/adjustX * cos(-i*k*arc+epoch)
            y += radius/adjustY * sin(-i*k*arc+epoch)

            draw.circle(radius, prevx, prevy, i, epoch)
            draw.point(prevx, prevy)
            draw.line((prevx, prevy), (x, y))

        l.insert(0, y)
        if len(l) > 300:
            l.pop()
        draw.point(0, l[0], 5)
        draw.line((0, l[0]), (x, y))
        draw.line((0, l[0]), (0, 0), 0.5)
        draw.line((x, 0), (x, y), 0.5)

        arc += inc

        draw.curve(l)

        pygame.display.flip()


main()
