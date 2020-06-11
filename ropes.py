
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
        if self.is_leaf():
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

        left  = self.leaf_str[:length//2]
        right = self.leaf_str[length//2:]

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
        if self.is_leaf():
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
        return self.fibonacci(self.depth + 2) <= self.left_length

    def is_leaf(self):
        return self.leaf_str != None

    def is_left_child(self):
        return self.parent.left_branch is self

    def get_leafs(self):
        if self.leaf_str != None:
            yield self.leaf_str

        else:
            yield from self.left_branch.get_leafs()
            yield from self.right_branch.get_leafs()

    def get_graph(self):
        graph = nx.DiGraph()
        self.add_to_graph(graph, (0,0) )
        return graph
            
    def add_to_graph(self, graph, loc):

        if self.is_leaf():
            graph.add_node(id(self), label=self.leaf_str, pos=loc, col = "red")
        else:
        
            graph.add_node(id(self), label='test', pos=loc, col="blue")
            offset = 2**(self.depth)
            self.left_branch.add_to_graph(graph,
                                          (loc[0] - offset, loc[1]-1))
            self.right_branch.add_to_graph(graph,
                                          (loc[0] + offset, loc[1]-1))

            graph.add_edge( id(self), id(self.left_branch) )
            graph.add_edge( id(self), id(self.right_branch) )

    
    
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
        

class RopesViz:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Ropes")

        fig = Figure(figsize=(5, 4))
        ax = fig.add_subplot(111)

        self.rope = Rope("This is a long test Magic hello")

        for leaf in self.rope.get_leafs():
            print(leaf)

        graph = self.rope.get_graph()

        pos   = { n:graph.nodes[n]['pos'] for n in graph.nodes()  } 
        lab = { n:graph.nodes[n]['label'] for n in graph.nodes()  } 
        col =   [graph.nodes[n]['col'] for n in graph.nodes()]

        nx.draw(graph,pos,ax,with_labels=True, node_color = col, labels = lab)

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
