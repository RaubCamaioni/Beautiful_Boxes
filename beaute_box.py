import numpy as np
import cv2
from enum import Enum
from numpy.random import rand
from numpy.random import randint

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Node:
    def __init__(self, p):
        self.p = p
        self.n = None
        self.e = None
        self.s = None
        self.w = None
        self.drawn = False

    def connect(self, node, d):
        if d == Direction.NORTH:
            self.n = node
            node.s = self
        elif d == Direction.EAST:
            self.e = node
            node.w = self
        elif d == Direction.SOUTH:
            self.s = node
            node.n = self
        elif d == Direction.WEST:
            self.w = node
            node.e = self
        else:
            print('Must pass a direction.')

class Square:
    def __init__(self, tl, tr, br, bl, root=False):
        self.tl = tl
        self.tr = tr
        self.br = br
        self.bl = bl

        if root:
            self.tl.connect(tr, Direction.EAST)
            self.tr.connect(br, Direction.SOUTH)
            self.br.connect(bl, Direction.WEST)
            self.bl.connect(tl, Direction.NORTH)

    def area(self, num):
        return (np.linalg.norm(self.vector(self.tl, self.tr)) * np.linalg.norm(self.vector(self.tl, self.bl))) > num

    def aspect(self, mode='aspect', modeval=0.5):

        if mode == 'random':
            return randint(0,2)

        return np.linalg.norm(self.vector(self.tl, self.tr)) * (1-modeval) < np.linalg.norm(self.vector(self.tl, self.bl)) * modeval # width < height

    def splith(self, thresh):

        # finding the placement of the new nodes
        v1 = self.vector(self.tl, self.bl)
        v2 = self.vector(self.tr, self.br)

        if np.linalg.norm(v1) < 3 or np.linalg.norm(v2) < 3:
            #print("can not split this square horizontally")
            return None

        p1 = (self.tl.p+v1*thresh).astype(np.int64)
        p2 = (self.tr.p+v2*thresh).astype(np.int64)

        n1 = Node(p1)
        n2 = Node(p2)

        start = self.tl
        end = self.bl
        while start is not end:
            d = np.linalg.norm(start.s.p) - np.linalg.norm(n1.p)
            if d > 0:
                n1.connect(start.s, Direction.SOUTH)
                start.connect(n1, Direction.SOUTH)
                break
            elif d == 0:
                n1 = start.s
                break
            start = start.s

        start = self.tr
        end = self.br
        while start is not end:
            d = np.linalg.norm(start.s.p - n2.p)
            if d > 0:
                n2.connect(start.s, Direction.SOUTH)
                start.connect(n2, Direction.SOUTH)
                break
            elif d == 0:
                n2 = start.s
                break
            start = start.s

        n1.connect(n2, Direction.EAST)

        return Square(self.tl, self.tr, n2, n1), Square(n1, n2, self.br, self.bl) #????

    def splitv(self, thresh):

        # finding the placement of the new nodes
        v1 = self.vector(self.tl, self.tr)
        v2 = self.vector(self.bl, self.br)

        if np.linalg.norm(v1) < 3 or np.linalg.norm(v2) < 3:
            #print("can not split this square vertically")
            return None

        p1 = (self.tl.p+v1*thresh).astype(np.int64)
        p2 = (self.bl.p+v2*thresh).astype(np.int64)

        n1 = Node(p1)
        n2 = Node(p2)

        start = self.tl
        end = self.tr
        while start is not end:
            d = np.linalg.norm(start.e.p) - np.linalg.norm(n1.p)
            if d > 0:
                n1.connect(start.e, Direction.EAST)
                start.connect(n1, Direction.EAST)
                break
            elif d == 0:
                n1 = start.e
                break
            start = start.e

        start = self.bl
        end = self.br
        while start is not end:
            d = np.linalg.norm(start.e.p - n2.p)
            if d > 0:
                n2.connect(start.e, Direction.EAST)
                start.connect(n2, Direction.EAST)
                break
            elif d == 0:
                n2 = start.e
                break
            start = start.e

        n1.connect(n2, Direction.SOUTH)

        return Square(self.tl, n1, n2, self.bl), Square(n1, self.tr, self.br, n2)

    def vector(self, n1, n2):
        return n2.p - n1.p

    def __repr__(self):
        return str(self.tl.p) + " " + str(self.tr.p) + " " + str(self.br.p) + " " + str(self.bl.p)

class SquareTree():
    def __init__(self, root, mode_val, mode="area", split_mode='aspect', split_modeval=0.5):

        self.p1 = None
        self.p2 = None
        self.sq1 = None
        self.sq2 = None
        self.root = root

        if mode == "area":
            split = root.area(mode_val)

        if mode == "depth":
            split = mode_val > 0

        if split:
            if root.aspect(mode=split_mode, modeval=split_modeval):

                #r = root.splith(.50+(rand()-.5)/2)
                r = root.splith(.50)

                if r is None: return
                self.sq1, self.sq2 = r #sq1 is the top or left rectangle
            else:

                #r = root.splitv(.50+(rand()-.5)/2)
                r = root.splitv(.50)

                if r is None: return
                self.sq1, self.sq2 = r

            self.p1 = SquareTree(self.sq1, mode_val-1, mode=mode, split_mode=split_mode, split_modeval=split_modeval)
            self.p2 = SquareTree(self.sq2, mode_val-1, mode=mode, split_mode=split_mode, split_modeval=split_modeval)

        else:
            return

    @staticmethod
    def graph(st):
        nodes = set()

        def buildGraph(st, set):
            if st.p1 is not None and st.p2 is not None:
                set = buildGraph(st.p1, set)
                return buildGraph(st.p2, set)
            else:
                set.add(st.root.tl)
                set.add(st.root.tr)
                set.add(st.root.br)
                set.add(st.root.bl)
                return set

        return list(buildGraph(st, nodes))

    @staticmethod
    def rootNode(height, width, spacer):
        canvas = np.ones((height, width, 3)) * 255

        n1 = Node(np.array([spacer, spacer]))
        n2 = Node(np.array([spacer, width-spacer]))
        n3 = Node(np.array([height-spacer, width-spacer]))
        n4 = Node(np.array([height-spacer, spacer]))

        return Square(n1, n2, n3, n4, root=True)

    @staticmethod
    def draw_square(s, canvas, line_color=(0,0,0), fill_color=(255,255,255), line_thickness = 2, fill=False):
        if True:
            cv2.rectangle(canvas,  tuple(s.tl.p), tuple(s.br.p), fill_color, -1)

        canvas = cv2.line(canvas, tuple(s.tl.p), tuple(s.tr.p), line_color, 2)
        canvas = cv2.line(canvas, tuple(s.tr.p), tuple(s.br.p), line_color, 2)
        canvas = cv2.line(canvas, tuple(s.br.p), tuple(s.bl.p), line_color, 2)
        canvas = cv2.line(canvas, tuple(s.bl.p), tuple(s.tl.p), line_color, 2)

        return canvas

    @staticmethod
    def draw_st(st, canvas, fill=False):

        def redraw(st, canvas):

            if st.p1 is not None and st.p2 is not None:
                line_color = (randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)
                fill_color = (randint(0, 255) / 255, randint(0, 255) / 255, randint(0, 255) / 255)

                canvas = SquareTree.draw_square(st.sq1, canvas, line_color=(0,0,0), fill_color=fill_color, fill=fill)
                canvas = SquareTree.draw_square(st.sq2, canvas, line_color=(0,0,0), fill_color=fill_color, fill=fill)

                redraw(st.p1, canvas)
                redraw(st.p2, canvas)

            return canvas

        return redraw(st, canvas)

    @staticmethod
    def draw_net(netlist, canvas, color=(0,0,0)):
        for node in netlist: # will go over the same line multiple times...
            if node.n is not None:
                canvas = cv2.line(canvas, tuple(node.p[::-1]), tuple(node.n.p[::-1]), color, 2)
            if node.e is not None:
                canvas = cv2.line(canvas, tuple(node.p[::-1]), tuple(node.e.p[::-1]), color, 2)
            if node.s is not None:
                canvas = cv2.line(canvas, tuple(node.p[::-1]), tuple(node.s.p[::-1]), color, 2)
            if node.w is not None:
                canvas = cv2.line(canvas, tuple(node.p[::-1]), tuple(node.w.p[::-1]), color, 2)

        return canvas

if __name__ == "__main__":

    for i in range(10):
        width, height = 1000, 1000
        border = 50

        s = SquareTree.rootNode(width, height, border)
        st = SquareTree(s, 10000, mode="area", split_mode='random', split_modeval=0)

        nodes = SquareTree.graph(st)

        #canvas = SquareTree.draw_net(nodes, canvas)
        canvas = np.ones((height,width,3)) * 255 # make a white canvas
        canvas = SquareTree.draw_st(st, canvas, fill=True)

        cv2.imshow('canvas', canvas)
        cv2.waitKey(0)
