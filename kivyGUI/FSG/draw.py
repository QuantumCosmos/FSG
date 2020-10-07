from math import pi, sin, cos
from OpenGL.GL import *
from OpenGL.GLU import *

class drawGL:
    def __init__(self, adjustX, adjustY, increment):
        self.adjustX = adjustX
        self.adjustY = adjustY
        self.inc = increment
        pass

    def circle(self, radius, posx, posy, n, epoch=0, slides=100):
        glLineWidth(0.05)
        glColor3f(0.4, 0.4, 0.4)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glBegin(GL_LINE_STRIP)
        x = y = 0
        for i in range(1, slides):
            x = (radius/self.adjustX * cos(n*2*pi*i/slides + epoch) + posx)
            y = (radius/self.adjustY * sin(n*2*pi*i/slides + epoch) + posy)
            glVertex2f(x, y)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)


    def point(self, x, y, size=2.0):
        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_BLEND)
        glPointSize(size)
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()


    def line(self, a, b, width=1):
        glLineWidth(width)
        glBegin(GL_LINES)
        glVertex2f(a[0], a[1])
        glVertex2f(b[0], b[1])
        glEnd()
        glLineWidth(1)


    def curve(self, l):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_LINE_SMOOTH)
        glBegin(GL_LINE_STRIP)
        for i in range(len(l)):
            glVertex2f(i*self.inc*0.05, l[i])
        glEnd()


    def trace(self, l):
        glLineWidth(0.1)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_LINE_LOOP)
        for i in range(len(l)):
            glVertex2f(l[i][0], l[i][1])
        glEnd()
