from FSG.fourier import fourier_wave
import threading
m = fourier_wave
def fourier(t, inp):
    m = fourier_wave
    display = (800, 500)
    center = (-0.55, 0)
    m = fourier_wave(center, display)
    print(inp)
    m.set_inp(inp.split(' '))
    m.integrate()
    m.set_radius_epoch()
    m.run()
    print('hahaha')

def trace(t):
    m.draw_trace = not m.draw_trace

def circle(t):
    m.draw_circle = not m.draw_circle

def q(t):
    m.window = False
