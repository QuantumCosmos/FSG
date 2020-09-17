from sympy import *
start = ['\\documentclass{article}\n',
         '\\usepackage[utf8]{inputenc}\n',
         '\\usepackage{amsmath}\n',
         '\\usepackage{mathtools}\n',
         '\\begin{document}\n']
end = ['\n\end{document}']
texdoc = []  # a list of string representing the latex document in python
head = '\\begin{equation*}\n'
tail = '\n\\end{equation*}\n'
equn = '\\alpha\\cdot\\gamma+\\beta = x^{\\frac{1!}{n}+\\frac{2!}{n^2}+\\frac{3!}{n^3}+\\ldots}'
x = symbols('x')
# inp = x**(12+x+3**(4*x+x))+x*3+46
# inp = x**12+1
# inp = sin(x)**(25*x+4**x*(90+x))+exp(2**(log(x**(2*x+6))+10*x**x))
inp = 2*x +6
inp = simplify(inp)
inp = latex(inp)
texdoc.append(''.join(start))
texdoc.append(head+equn+tail+head+inp+tail)
texdoc.append(''.join(end))
with open('new.tex', 'w') as fout:
    for i in range(len(texdoc)):
        fout.write(texdoc[i])
