import collections
import random
import numpy as np
import matplotlib.pyplot as plt

Motor = collections.namedtuple('Motor',['direction','pose','children','id'])#in absolute coords, direction is expressed by elevation, twist
Link = collections.namedtuple('Link',['direction','length','children','id'])

class Stickbug():
    def __init__(self):
        self.body = [Link(direction=(0.0,0.0), length=0.0, children=[], id=self.getId())]
        self.coords = 'absolute'

    def build(self):
        depth = 0
        searchlist = self.body
        t_searchlist = []
        for s in searchlist:
            #add sub-nodes at random
            c = 0
            m = self.generationSize(depth)
            while c<m:
                c+=1
                s.children.append(self.makeNode)
                t_searchlist.append(s.children[-1])



    def generationSize(self,depth):
        #choose either 0, 1, or 2 children, based on depth+random seed
        window = depth/3.0 #at 4 deep, no more children
        p = random.random()
        if p<window:
            return 0
        elif p<window+(1/3.0):
            return 1
        else:
            return 2

    def makeNode(self):
        #some tradeoff between motors and links
        if random.random()<0.5:
            out = Motor(direction=(random.random(180.0*random.random()-90.0,360.0*random.random()-180.0)),pose=0.0,children=[],id=self.getId())
        else:
            out = Link(direction=(random.random(180.0*random.random()-90.0,360.0*random.random()-180.0)),length=random.random()+0.25,children=[],id=self.getId())
        return out

    def getId(self):
        return ''.join(random.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890',10))

    def mirror(plane):

    def __repr__(self):

    def pprint(depth, nodes):
