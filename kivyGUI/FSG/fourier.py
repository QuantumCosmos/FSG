import pygame
import numpy as np
try:
    from .draw import drawGL
except ImportError:
    from draw import drawGL
from scipy.integrate import quad
from math import pi, atan2, sqrt, sin, cos
from pygame.locals import DOUBLEBUF, OPENGL
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

class fourier_wave(drawGL):
    draw_trace = False
    draw_circle = True
    runLoop = True

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

    def __init__(self, center, display, speed=1, limit=50):
        self.inc = 2*pi/limit
        self.center = center
        self.adjustX = display[0]/min(display)
        self.adjustY = display[1]/min(display)
        self.display = display

        self.speed = speed
        self.lim = limit
        super(fourier_wave, self).__init__(self.adjustX, self.adjustY, self.inc)


    def set_inp(self, inp):
        self.str_func = inp.pop(0)
        for i in fourier_wave.math_tray:
            if i in self.str_func:
                self.str_func = self.str_func.replace(i, fourier_wave.math_tray[i]).replace("np.np.", "np.")
        self.lL = eval(inp[0])
        self.uL = eval(inp[1])
        if self.lL > self.uL:
            self.uL, self.lL = self.lL, self.uL


    def integrate(self):
        R = self.uL - self.lL
        self.ai = lambda n: quad(lambda x: (2/R)*eval(self.str_func)*np.cos(2*pi*x*n/R), self.lL, self.uL)[0]
        self.bi = lambda n: quad(lambda x: (2/R)*eval(self.str_func)*np.sin(2*pi*x*n/R), self.lL, self.uL)[0]
        self.c = quad(lambda x: (2/R)*eval(self.str_func), self.lL, self.uL)[0]
        print('Integration Done!')


    def set_radius_epoch(self):
        def radius(i): return sqrt((self.ai(i))**2 + (self.bi(i))**2)

        def epoch(i): return atan2(float(self.ai(i)), float(self.bi(i)))

        self.rad_epo = {}
        scale = 0
        for i in range(1, self.lim+1):
            r = radius(i)
            if r > 0:
                scale += r
            if r > 1e+5:
                r = fourier_wave.max_r_for_inf_cond
            self.rad_epo[i] = {'rad': r, 'epo': float(epoch(i))}
        
        self.scale = int(scale)+1
        print('Values Ready!')


    def run(self):
        self.runLoop = True
        arc = 0
        l = []
        all_val = []
        pygame.init()
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fourier_wave.runLoop = False
                    break
            if not fourier_wave.runLoop:
                break

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.line((1, 0), (-1, 0))
            x = self.center[0]
            y = self.center[1] + self.c*0.5/self.scale

            for i in range(1, self.lim+1):
                prevx = x
                prevy = y
                epoch = self.rad_epo[i]['epo']
                radius = self.rad_epo[i]['rad']/self.scale
                x += radius/self.adjustX * cos(-i*self.speed*arc+epoch)
                y += radius/self.adjustY * sin(-i*self.speed*arc+epoch)

                if fourier_wave.draw_circle:
                    self.circle(radius, prevx, prevy, i, epoch)
                self.point(prevx, prevy)
                self.line((prevx, prevy), (x, y))

            l.insert(0, y)
            if arc < 2*pi/self.speed:
                all_val.append((prevx, prevy))
                
            if len(l) > 350:
                l.pop()
            self.point(0, l[0], 5)
            self.line((0, l[0]), (x, y))
            self.line((0, l[0]), (0, 0), 0.5)
            self.line((x, 0), (x, y), 0.5)

            arc += self.inc

            self.curve(l)
            if fourier_wave.draw_trace:
                self.trace(all_val)

            pygame.display.flip()


if __name__ == '__main__':
    display = (800, 500)
    center = (-0.55, 0)
    m = fourier_wave(center, display)
    m.set_inp(input('Enter the function with limits (separated by space):\n').split(' '))
    m.integrate()
    m.set_radius_epoch()
    m.run()

