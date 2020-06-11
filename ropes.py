
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
        self.position = None           # current position inside the string
                                       # \-> None if not in current branch

        self.left_length = None        # length of rope in left subtree
        self.left_branch = None        # pointer to left branch
        self.right_branch = None       # pointer to right branch

        self.leaf_str = string.replace(" ","_")

        #split and rebalance
        if len(self.leaf_str) > self.MAX_LEAF:
            self.split()

    def update(self):
        if not self.is_leaf():
            self.left_length = self.left_branch.total_lenth
            self.total_lenth = self.left_branch.total_lenth \
                             + self.right_branch.total_lenth

            self.depth = max(self.left_branch.depth, self.right_branch.depth) + 1

            if self.left_branch.position is not None:
                self.position = self.left_branch.position
            elif self.right_branch.position is not None:
                self.position = self.right_branch.position + self.left_length
            else:
                self.position = None

        if self.parent != None:
            self.parent.update()

    def split(self):
        assert self.is_leaf()

        length = len(self.leaf_str)
        midpoint = length//2

        left  = self.leaf_str[:midpoint]
        right = self.leaf_str[midpoint:]

        self.left_branch = Rope(left, self)
        self.right_branch = Rope(right, self)

        if self.position is not None:
            if self.position <= midpoint:
                self.left_branch.position = self.position
            else:
                self.right_branch.position = self.position - midpoint

        self.leaf_str = None
        self.update()

    def rebalance(self):
        pass

    ## EDITING METHODS
    def move_cursor(self, i):
        self.position = i

        if not self.is_leaf():
            if i is None:
                self.left_branch.move_cursor(None)
                self.right_branch.move_cursor(None)

            elif i <= self.left_length:
                self.left_branch.move_cursor(i)
                self.right_branch.move_cursor(None)
            else:
                self.right_branch.move_cursor(i - self.left_length)
                self.left_branch.move_cursor(None)

    def add_character(self, char):
        assert self.position is not None

        if self.is_leaf():
            char = char.replace(" ","_")
            self.leaf_str = self.leaf_str[:self.position] \
                            + char \
                            + self.leaf_str[self.position:]
            self.position += 1
            self.total_lenth = len(self.leaf_str)

            if len(self.leaf_str) > self.MAX_LEAF:
                self.split()
            else:
                self.update()

        else:
            if self.position <= self.left_length:
                self.left_branch.add_character(char)
            else:
                self.right_branch.add_character(char)

        print("added", char, "to node depth", 
              self.depth, "with new pos", self.position)

    def remove_character(self):
        pass

    ## CHECK STATES
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

    ## GRAPH DRAWING
    def get_graph(self):
        graph = nx.DiGraph()
        self.add_to_graph(graph, (0,0) )
        return graph
            
    def add_to_graph(self, graph, loc):

        col = "#FFAAAA" if self.position is not None else "#AAAAFF"

        if self.is_leaf():
            graph.add_node(id(self), 
                           label=str(self.total_lenth)+self.leaf_str,
                                                          pos=loc, col = col)
        else:
            graph.add_node(id(self),
                           label=str(self.left_length)+","+str(self.total_lenth), 
                                                          pos=loc, col=col)
            offset = 2**(self.depth)
            self.left_branch.add_to_graph(graph,
                                          (loc[0] - offset, loc[1]-1))
            self.right_branch.add_to_graph(graph,
                                          (loc[0] + offset, loc[1]-1))

            graph.add_edge( id(self), id(self.left_branch) )
            graph.add_edge( id(self), id(self.right_branch) )

    ## FIBONACCI HELPER
    
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

        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)

        default_text = "This is a t"
        self.rope = Rope(default_text)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.text = tk.Text(self.root)
        self.text.pack()
        self.text.insert('0.0', default_text)

        self.text.bind('<Key>', self.process_event)
        self.text.bind('<Button-1>', self.mouse_click)

        self.redraw()
        self.root.mainloop()

    def redraw(self):
        graph = self.rope.get_graph()

        pos   = { n:graph.nodes[n]['pos'] for n in graph.nodes()  } 
        lab = { n:graph.nodes[n]['label'] for n in graph.nodes()  } 
        col =   [graph.nodes[n]['col'] for n in graph.nodes()]

        self.ax.clear()
        nx.draw(graph,pos,self.ax,with_labels=True, node_color = col, labels = lab)
        self.canvas.draw()

    # tkinter Text Widget processes callbacks after "normal" character events
    # but *before* updating the cursor position. This hack schedules to run
    # *after* the cursor position is updated
    def move_cursor(self):
        index =  int(self.text.index("insert").split('.')[1])
        if index != self.rope.position:
            self.rope.move_cursor(index)
            self.redraw()
            print("updated index", index)

        t = self.text.get(1.0,'end')
        print( t[:index] + "@" + t[index:])

    def mouse_click(self,event):
        self.root.after(0,self.move_cursor)

    def process_event(self, event):
        if( event.char.isprintable() and len(event.char)==1 ):
            print("adding char")
            self.rope.add_character(event.char)
            self.redraw()

        self.root.after(0,self.move_cursor)


if __name__ == '__main__':
    r = RopesViz()
