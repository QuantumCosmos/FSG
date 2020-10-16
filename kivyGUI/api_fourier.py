from FSG.fourier import fourier_wave
import threading
m = fourier_wave
class api:
    def fourier(self, t, inp):
        m = fourier_wave
        display = (800, 500)
        center = (-0.55, 0)
        m = fourier_wave(center, display)
        print(inp)
        m.set_inp(inp.split(' '))
        m.integrate()
        m.set_radius_epoch()
        m.run()
        return 0

    def trace(self, t):
        m.draw_trace = not m.draw_trace
        return 0


    def circle(self, t):
        m.draw_circle = not m.draw_circle
        return 0


    def q(self, t):
        m.runLoop = False
        return 0
