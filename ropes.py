
# Michal Adamkiewicz
# mikadam@stanford.edu
# Done for CS166 final project

# Visualization of a rope backed text editor. Currently edited nodes
# are highlighted red. Supports cut copy and paste (although cut isn't real
# as it just rebuilds the rope

# Needs matplotlib, networkx and tkinter to work

import tkinter as tk
from functools import reduce

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

        self.leaf_str = string
        self.leaf_str = self.leaf_str.replace(" ","_")
        self.leaf_str = self.leaf_str.replace("\n","")

        #split and rebalance
        if len(self.leaf_str) > self.MAX_LEAF:
            self.split()

    @classmethod
    def fromConcatination(cls, left, right):
        out = Rope("")
        out.leaf_str = None
        out.left_branch = left
        out.right_branch = right
        out.update()
        return out

    def update(self):
        if self.is_leaf():
            self.depth = 0
            self.total_lenth = len(self.leaf_str)
        else:
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

        # print("left_length", self.left_length)
        # print("total_lenth", self.total_lenth)
        # print("position", self.position)

        if self.left_length == 0:
            self.replace(self.right_branch)
        elif self.left_length == self.total_lenth:
            self.replace(self.left_branch)

        if self.depth == 1 and self.total_lenth <= self.MAX_LEAF:
            self.merge()

        if self.parent != None:
            self.parent.update()

    def replace(self, node):
        self.total_lenth  = node.total_lenth
        self.depth        = node.depth
        self.position     = node.position

        self.leaf_str     = node.leaf_str
        self.left_length  = node.left_length
        self.left_branch  = node.left_branch
        self.right_branch = node.right_branch
    
    def merge(self):
        self.depth = 0
        self.leaf_str = self.left_branch.leaf_str + self.right_branch.leaf_str
        self.total_lenth = len(self.leaf_str)

        if self.left_branch.position is not None:
            self.position = self.left_branch.position
        elif self.right_branch.position is not None:
            self.position = self.right_branch.position + self.left_length

        self.left_length = None
        self.left_branch = None
        self.right_branch = None

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

    ## CHECK STATES
    def is_balanced(self):
        if self.is_leaf():
            assert self.fibonacci(self.depth + 2) <= self.total_lenth
        return self.fibonacci(self.depth + 2) <= self.total_lenth

    def is_leaf(self):
        return self.leaf_str != None

    def is_left_child(self):
        return self.parent.left_branch is self

    def get_leafs(self):
        if self.is_leaf():
            yield self.leaf_str

        else:
            yield from self.left_branch.get_leafs()
            yield from self.right_branch.get_leafs()

    ## BALANCING METHODS
    def rebalance(self):
        # algoryth straight from 
        # Ropes: an Alternative to Strings
        # https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf

        if self.is_balanced():
            return self

        print("rebalancing")
        sequence = []

        for rope in self.get_balanced_subropes():
            i = 2
            while 1:
                while( rope.total_lenth >= self.fibonacci(i) ):
                    i += 1
                while( i >= len(sequence) ):
                    sequence.append(None)

                # print("total_lenth", rope.total_lenth)
                # print([ self.fibonacci(i) if sequence[i] is not None else None \
                #                  for i in range(len(sequence))])

                if sequence[i] is None:
                    sequence[i] = rope
                    break
                else:
                    rope = Rope.fromConcatination(sequence[i], rope)
                    sequence[i] = None

        ropes = reversed(list(filter( lambda x: x is not None, sequence)))
        return reduce(  lambda x,y: Rope.fromConcatination(y,x), ropes)



    def get_balanced_subropes(self):
        if self.is_balanced():
            yield self

        else:
            yield from self.left_branch.get_balanced_subropes()
            yield from self.right_branch.get_balanced_subropes()

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
            self.position += len(char)
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
        assert self.position is not None

        if self.position == 0:
            return

        if self.is_leaf():
            self.leaf_str = self.leaf_str[:self.position-1] \
                            + self.leaf_str[self.position:]
            self.position -= 1
            self.total_lenth = len(self.leaf_str)
            self.update()

        else:
            if self.position <= self.left_length:
                self.left_branch.remove_character()
            else:
                self.right_branch.remove_character()

        print("removed from node depth", 
              self.depth, "with new pos", self.position)

    ## GRAPH DRAWING
    def get_graph(self):
        graph = nx.DiGraph()
        self.add_to_graph(graph, (0,0), 0)
        return graph
            
    def add_to_graph(self, graph, loc, size):

        col = "#FFAAAA" if self.position is not None else "#AAAAFF"
        # if not self.is_balanced():
        #     col = "#AAFFAA"

        if self.is_leaf():
            graph.add_node(id(self), 
                           label=self.leaf_str, pos=loc, col = col)
        else:
            graph.add_node(id(self),
                           label=str(self.left_length)+","+str(self.total_lenth), 
                                                          pos=loc, col=col)
            offset = 2**(size)
            self.left_branch.add_to_graph(graph,
                                          (loc[0] - offset, loc[1]-1), size-1)
            self.right_branch.add_to_graph(graph,
                                          (loc[0] + offset, loc[1]-1), size-1)

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
        self.root.title("Rope Visualization")

        self.fig = Figure(figsize=(5, 4))
        self.ax = self.fig.add_subplot(111)

        default_text = "This is a t"
        self.rope = Rope(default_text)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.text = tk.Text(self.root)
        self.text.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.text.insert('0.0', default_text)

        self.text.bind('<Key>', self.process_event)
        self.text.bind('<Button-1>', self.mouse_click)

        self.text.bind('<<Copy>>', lambda e: "pass")
        self.text.bind('<<Cut>>', self.cut)
        self.text.bind('<<Paste>>', self.paste)

        self.redraw()
        self.root.mainloop()

    def cut(self, event):
        # during deletions with a selection (such as during cut)
        # we give up on incrementally modifying the rope and we just
        # restart with a new one. Definitely not how it works in practice
        # but this code is already too much of a mess 
        self.root.after(0,self.reinitalize)

    def paste(self, event):
        self.rope.add_character(self.root.clipboard_get())
        self.redraw()

    def reinitalize(self):
        t = self.text.get(1.0,'end').replace("\n","")
        self.rope = Rope(t)
        self.move_cursor()

    def redraw(self):
        graph = self.rope.get_graph()

        pos   = { n:graph.nodes[n]['pos'] for n in graph.nodes()  } 
        lab = { n:graph.nodes[n]['label'] for n in graph.nodes()  } 
        col =   [graph.nodes[n]['col'] for n in graph.nodes()]

        self.ax.clear()
        nx.draw(graph,pos,self.ax,with_labels=True, node_color = col,labels = lab,
            node_shape = 's', font_size = 10, node_size = 500)
        self.canvas.draw()

    # tkinter Text Widget processes callbacks after "normal" character events
    # but *before* updating the cursor position. This hack schedules to run
    # *after* the cursor position is updated
    def move_cursor(self):
        line, char =  self.text.index("insert").split('.')
        lines = list(map(lambda x: len(x), self.text.get(1.0,'end').split("\n")))
        index = sum( lines[: int(line)-1] ) + int(char)

        if index != self.rope.position:
            self.rope.move_cursor(index)
            self.redraw()
            print("updated index", index)

        t = self.text.get(1.0,'end').replace("\n","")
        print( t[:index] + "@" + t[index:])

    def mouse_click(self,event):
        self.root.after(0,self.move_cursor)

    def process_event(self, event):
        print(event.char)
        print(event.keysym)
        print(event.keycode)
        if event.keysym == "BackSpace":
            try:
                self.text.selection_get()
            except tk.TclError:
                pass
            else:
                self.root.after(0,self.reinitalize)
                return

            if int(self.text.index("insert").split('.')[1]) == 0:
                return
            self.rope.remove_character()
            self.redraw()

        elif( event.char.isprintable() and len(event.char)==1 ):
            print("adding char")
            try:
                self.text.selection_get()
            except tk.TclError:
                pass
            else:
                self.root.after(0,self.reinitalize)
                return

            self.rope.add_character(event.char)
            self.rope = self.rope.rebalance()
            self.redraw()

        self.root.after(0,self.move_cursor)

if __name__ == '__main__':
    r = RopesViz()
