
import tkinter as tk

import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


text = "Hello_CS166_people,_this_is_a_test"

graph = nx.DiGraph()

nodes = [ "Hello_",
            "CS166",
            "_peop",
            "le,_t",
            "his_is",
            "_a_tes",
            "t"]

i = 1
for x in nodes:
    graph.add_node(x, label =x, pos=(i,1))
    i += 1

while 1:
    new_nodes = []

    while len(nodes) > 1:
        a = nodes.pop(0)
        b = nodes.pop(0)
        j = a+b

        a_pos = graph.nodes[a]['pos']
        b_pos = graph.nodes[b]['pos']

        x_pos = (a_pos[0] + b_pos[0])/2

        y_pos = max(a_pos[1], b_pos[1]) + 1

        graph.add_node(j, label =j, pos = ( x_pos, y_pos ) )

        graph.add_edge(j, a)
        graph.add_edge(j, b)
        new_nodes.append(j) 

    if len(nodes) != 0:
        new_nodes.append(nodes.pop(0))

    nodes = new_nodes
    if len(nodes) == 1:
        break

root = tk.Tk()
root.title("Ropes")

fig = Figure(figsize=(5, 4))
ax = fig.add_subplot(111)

# pos =nx.drawing.nx_agraph.graphviz_layout(graph, prog='dot')


pos = { n:graph.nodes[n]['pos'] for n in graph.nodes()  } 
col = ["#2679B2"] * len(graph.nodes)
col[3] = 'red'

nx.draw(graph, pos, ax, with_labels=True, node_color = col)
# nx.draw(graph, pos, ax, with_labels=True)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


text = tk.Text(root)
text.pack()

root.mainloop()
