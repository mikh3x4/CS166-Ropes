
import tkinter as tk

import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Rope:
    MAX_LEAF = 5
    def __init__(self, string, parent = None):
        self.total_lenth = len(string) # total length of rope
        self.depth = 0                 # max depth of rope
        self.parent = parent           # pointer to parent node

        self.left_length = 0           # length of leafs in left subtree
        self.left_branch = None        # pointer to left branch
        self.right_branch = None       # pointer to right branch

        self.leaf_str = string         # leaf string
        self.leaf_position = 0         # current position inside the string
                                       # \-> None if not in current branch

        #split and rebalance
        if len(self.leaf_str) > self.MAX_LEAF:
            self.split()

    def update(self):
        if self.is_leaf()
            return

        self.left_length = self.left_branch.total_lenth
        self.total_lenth = self.left_branch.total_lenth \
                         + self.right_branch.total_lenth

        self.depth = max(self.left_branch.depth, self.right_branch.depth) + 1

        if self.parent != None:
            self.parent.update()

    def split(self):
        assert self.is_leaf()

        length = len(self.leaf_str)

        left  = self.leaf_str[:length/2]
        right = self.leaf_str[length/2:]

        self.left_branch = Rope(left, self)
        self.right_branch = Rope(right, self)

        self.leaf_str = None
        self.update()

    def substring(self, i, j):
        pass

    def move_cursor(self, i):
        if self.is_leaf():
            self.leaf_position = i

        else:
            if i < self.left_length:
                self.left_branch.move_cursor(i)
            else:
                self.right_branch.move_cursor(i - self.left_length)

    def add_character(self, i, char):
        total_lenth += 1
        if self.is_leaf()
            self.leaf_str += char
            if len(self.leaf_str) > self.MAX_LEAF:
                self.split()

        else:
            if i < self.left_length:
                self.left_length += 1
                self.left_branch.add_character(i, char)
            else:
                self.right_branch.add_character(i - self.left_length, char)

    def remove_character(self, i):
        pass

    def rebalance(self):
        pass

    def is_balanced(self):
        return self.fibonacci(self.depth + 2) =< self.left_length

    def is_leaf(self):
        return self.leaf_str != None

    def get_leafs(self):
        if self.leaf_str != None:
            yield self.leaf_str

        else:
            yield from self.left_branch.get_leafs()
            yield from self.right_branch.get_leafs()

    def get_graph(self):
        pass

    
    
    fib_store = [0, 1]
    @classmethod
    def fibonacci(cls, n):
        # Calculates and memorises Fibonacci number across all instances
        # Probably faster then closed form solution as it usually a lookup
        if n >= len(cls.fib_store):
            out = cls.fibonacci(n-1) + cls.fibonacci(n-2)
            assert len(cls.fib_store) == n
            cls.fib_store.append(out)
            return out
        else:
            return cls.fib_store[n]
        

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


class RopesViz:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Ropes")

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)

        pos = { n:graph.nodes[n]['pos'] for n in graph.nodes()  } 
        col = ["#2679B2"] * len(graph.nodes)
        col[3] = 'red'

        nx.draw(graph, pos, ax, with_labels=True, node_color = col)

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        self.text = tk.Text(self.root)
        self.text.pack()

        self.text.bind('<Key>', self.process_event)

        self.root.mainloop()


    def process_event(self, event):
        print(event.char)
        print(self.text.index("insert"))
        print(self.text.get(1.0,'end'))
        pass

if __name__ == '__main__':
    r = RopesViz()
