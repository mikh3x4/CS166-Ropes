Rope Vizualization
---

This is a small GUI vizalization of how the datastructures behind a rope backed text editor would work. The balancing scheme is taken from the original paper that introduced ropes ([Ropes: an Alternative to Strings](https://www.cs.rit.edu/usr/local/pub/jeh/courses/QUARTERS/FP/Labs/CedarRope/rope-paper.pdf)).

This project was done for Stanford's [CS166](http://cs166.stanford.edu) datastructures class

IMAGE

Features
---
- Fibonacci based balancing scheme
- Edit the text anywhere and see the rope datastrcuture live update
- You can use both arrow keys and the mouse to move around and the appropriate part of the rope tree will be highlighted in red
- Cut, copy and paste are supported and will update the rope correctly (although cut will just reinitalize the tree)


Demo
---

GIF
GIF
GIF

Installation
---
Dependancies can be installed using:
`pip install matplotlib networkx`

Note that `tkinter` is also required and although its supposed to be bundled with python, recently there are some issues with it on Mac OS. 

Running is simply
`python ropes.py`
