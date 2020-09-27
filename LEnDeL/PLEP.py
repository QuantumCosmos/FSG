import os
import subprocess
from sympy import *
def make_A_tex(name='new', rmlog=True, openPDF=False):
    head = ['\\documentclass{article}\n',
            '\\usepackage[utf8]{inputenc}\n',
            '\\usepackage{amsmath}\n',
            '\\usepackage{mathtools}\n',
            '\\begin{document}\n',
            '\\begin{equation*}\n']
    tail = ['\n\\end{equation*}\n', 
            '\\end{document}']
    x = symbols('x')
    inp = latex(simplify(input('Enter math:\n')))
    print(inp)
    texdoc = ''.join(head) + inp + ''.join(tail)
    with open(name+'.tex', 'w') as fout:
        fout.write(texdoc)
    print('.tex file successfully written')
    try:
        subprocess.run("pdflatex " + name + ".tex", stdout=subprocess.DEVNULL)
        print('.tex file successfully compilied')
    except FileNotFoundError:
        print('no latex compiler')
    if rmlog:
        delete(name)
    if openPDF:
        os.popen(name+'.pdf')
    return inp


def delete(name):
    os.remove(name+'.aux')
    os.remove(name+'.log')
    try:
        os.remove(name+'.synctex.gz')
    except FileNotFoundError:
        pass
    


make_A_tex()
