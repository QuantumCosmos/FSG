import pygame
import numpy as np
from draw import drawGL
from scipy.integrate import quad
from math import pi, atan2, sqrt, sin, cos
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

class fourier_wave(drawGL):
    max_r_for_inf_cond = 0.5
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

    def __init__(self, center, display, speed=.5, limit=50):
        self.inc = pi/limit
        self.center = center
        self.adjustX = display[0]/min(display)
        self.adjustY = display[1]/min(display)

        self.speed = speed
        self.lim = limit
        super(fourier_wave, self).__init__(self.adjustX, self.adjustY, self.inc)

    def get_inp(self):
        return input('Enter the function with limits (separated by space):\n').split(' ')

    def set_inp(self, inp):
        str_func = inp.pop(0)
        for i in fourier_wave.math_tray:
            if i in str_func:
                str_func = str_func.replace(i, fourier_wave.math_tray[i]).replace("np.np.", "np.")
        lL = eval(inp[0])
        uL = eval(inp[1])
        if lL > uL:
            uL, lL = lL, uL

        return str_func, lL, uL

    def integrate(self, str_func, lL, uL):
        R = uL - lL
        ai = lambda n: quad(lambda x: (2/R)*eval(str_func)*np.cos(2*pi*x*n/R), lL, uL)[0]
        bi = lambda n: quad(lambda x: (2/R)*eval(str_func)*np.sin(2*pi*x*n/R), lL, uL)[0]
        c = quad(lambda x: (2/R)*eval(str_func), lL, uL)[0]
        print('Integration Done!')

        return ai, bi, c

    def set_radius_epoch(self, ai, bi, c):
        def radius(i): return sqrt((ai(i))**2 + (bi(i))**2)

        def epoch(i): return atan2(float(ai(i)), float(bi(i)))

        rad_epo = {}
        scale = 0
        for i in range(1, self.lim+1):
            r = radius(i)
            if r > 0:
                scale += r
            if r > 1e+5:
                r = fourier_wave.max_r_for_inf_cond
            rad_epo[i] = {'rad':r, 'epo':float(epoch(i))}
        
        scale = int(scale)+1
        print('Values Ready!')

        return c/scale, rad_epo, scale

    def run(self, c, rad_epo, scale):
        arc = 0
        l = []
        pygame.init()
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.line((1, 0), (-1, 0))
            x = self.center[0]
            y = self.center[1] + c/2

            for i in range(1, self.lim+1):
                prevx = x
                prevy = y
                epoch = rad_epo[i]['epo']
                radius = rad_epo[i]['rad']/scale
                x += radius/self.adjustX * cos(-i*self.speed*arc+epoch)
                y += radius/self.adjustY * sin(-i*self.speed*arc+epoch)

                self.circle(radius, prevx, prevy, i, epoch)
                self.point(prevx, prevy)
                self.line((prevx, prevy), (x, y))

            l.insert(0, y)
            if len(l) > 350:
                l.pop()
            self.point(0, l[0], 5)
            self.line((0, l[0]), (x, y))
            self.line((0, l[0]), (0, 0), 0.5)
            self.line((x, 0), (x, y), 0.5)

            arc += self.inc

            self.curve(l)

            pygame.display.flip()


display = (800, 500)
center = (-0.55, 0)
m = fourier_wave(center, display)
m.run(*m.set_radius_epoch(*m.integrate(*m.set_inp(m.get_inp()))))
