import re

angles = {
  'N' : 0,
  'S' : 180,
  'E' : 90,
  'W' : 270
}

edges_str = []
nodes_str = []

with open('planet') as f:
  # matcher = re.compile('(-?\d),(-?,\d),(N|S|E|W),(-?\d),(-?\d),(N|S|E|W)')
  # e=[matcher.match(s) for s in f]

  for s in f:
    a = s.strip().split(',')
    node1 = (a[0], a[1])
    node2 = (a[3], a[4])
    for n in node1, node2:
        nodes_str.append('\\node[draw] ({name}) at ({x}, {y}) {{}};'.format(
            name = str(n[0]) + '-' + str(n[1]),
            x = n[0],
            y = n[1]
        ))
    edges_str.append('\\draw[->] ({node1}) to[in={in_}, out={out}] ({node2});'.format(
        node1 = str(node1[0]) + '-' + str(node1[1]), 
        node2 = str(node2[0]) + '-' + str(node2[1]),
        in_ = angles[a[2]],
        out = angles[a[5]]
    ))

with open('out.tex', 'w') as out:
    out.write('\\documentclass[preview]{standalone}\n')
    out.write('\\include{tikz}\n')
    out.write('\\begin{document}\n')
    out.write('\\begin{tikzpicture}\n')
    
    for n in nodes_str:
        out.write(n + '\n')

    for e in edges_str:
        out.write(e + '\n')

    out.write('\\end{tikzpicture}\n')
    out.write('\\end{document}\n')
