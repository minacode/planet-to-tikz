def node_name(a, b):
    return str(a) + '-' + str(b)

def node_highlight(x, y):
    return '\\node[draw=green, circle, minimum width=3mm, minimum height=3mm, label={{[green]120:{c}}}] ({name}) at ({x}, {y}) {{}};'.format(
                    name = 'h-' + node_name(x, y),
                    x = x,
                    y = y,
                    c = (int(x), int(y))
                )

angles = {
    'N' : 90,
    'S' : 270,
    'E' : 0,
    'W' : 180
}

edges_str = []
targets_str = []
nodes_str = []
node_highlights = []
start_count = 0

with open('planet') as f:
    for s in f:
        # comment
        if s.strip() == '':
            continue
        if s.strip()[0] == '#':
            continue
        elif s.strip()[:4] == 'edge':
            parts = s.strip().split()
            trigger_node = parts[1].split(',')
            node_highlights.append(node_highlight(trigger_node[0], trigger_node[1]))
        elif s.strip()[:5] == 'start':
            a = s.strip().split()[1].split(',')
            start_node = 's' + str(start_count)
            x = float(a[0])
            y = float(a[1]) - 0.5
            nodes_str.append('\\node ({name}) at ({x}, {y}) {{}};'.format(
                name = start_node,
                x = x,
                y = y,
            ))
            edges_str.append('\\draw ({node1}) -- ({node2});'.format(
                node1 = start_node,
                node2 = node_name(a[0], a[1]) 
            ))
        elif s.strip()[:6] == 'target':
            parts = s.strip().split()
            trigger_node = parts[1].split(',')
            target_node = parts[2].split(',')
            targets_str.append('\\path[->] ({trigger}) edge[dashed, color=green, bend left=10] ({target});'.format(
                trigger = 'h-' + node_name(trigger_node[0], trigger_node[1]),
                target = 'h-' + node_name(target_node[0], target_node[1])
            ))
            for n in trigger_node, target_node:
                node_highlights.append(node_highlight(n[0], n[1]))
        else:
            a = s.strip().split(',')
            node1 = (a[0], a[1])
            node2 = (a[3], a[4])
            for n in node1, node2:
                b = int(n[0])+int(n[1])
                if b%2 == 0:
                    col = 'red'
                else:
                    col = 'blue'
                nodes_str.append('\\node[draw={col}, fill={col}, minimum width=1mm, minimum height=1mm] ({name}) at ({x}, {y}) {{}};'.format(
                    name = node_name(n[0], n[1]),
                    x = n[0],
                    y = n[1],
                    col = col
                ))

            node1 = node_name(node1[0], node1[1]) 
            node2 = node_name(node2[0], node2[1])
            dir1 = str(angles[a[5]])
            dir2 = str(angles[a[2]])
            weight = str(a[6])
            edges_str.append('\\draw (' + node1 + ') to[in=' + dir1 + ', out=' + dir2 + ', edge node={node[auto] {' + weight +'}}] (' + node2 + ');')

with open('out.tex', 'w') as out:
    out.write('\\documentclass[preview, border=20pt]{standalone}\n')
    out.write('\\include{tikz}\n')
    out.write('\\usetikzlibrary{backgrounds}')
    out.write('\\begin{document}\n')
    out.write('\\tikzstyle{background grid}=[draw, black!20, step=2cm]')
    out.write('\\begin{tikzpicture}[show background grid, x=2cm, y=2cm]')
    # out.write('\\begin{tikzpicture}\n')
    
    for s in node_highlights + nodes_str + edges_str + targets_str:
        out.write(s + '\n')

    out.write('\\end{tikzpicture}\n')
    out.write('\\end{document}\n')
