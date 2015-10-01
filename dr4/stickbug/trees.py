from __future__ import division
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import math
import collections
import os

def get_parent_candidates(tree):
    """return the indicies of the level-rep parent candidates in the tree
    if adding a node to the identified candidate would break lexigraphic ordering, it is not a candidate"""
    #walk backwards up tree, keeping track of children
    i = len(tree)-1
    candidates = []
    while i!=None:
        if is_lexigraphically_valid(tree, i):
            candidates.append(i)
        i = find_parent(tree, i)
    return candidates

def find_parent(tree,i):
    """find the index of the parent of i.  if i is the root, return None"""
    if i==0:
        return None
    temp = i
    while tree[temp]>=tree[i]:
        temp -= 1
    return temp

def is_lexigraphically_valid(tree,i_candidate):
    """check if using this parent candidate would keep the tree lexigraphically valid"""
    #check if candidate is last on left path(eg, straight chain)
    if tree[:i_candidate]==():#it's now a tuple, so check for empty tuple
        return True
    return tree[i_candidate]!=max(tree[:i_candidate])

def insert_child(tree,i):
    t = list(tree)
    t.append(tree[i]+1)#add a new node at the end, one level deeper than the parent
    return tuple(t)

def make_children(tree):
    cs = get_parent_candidates(tree)
    trees = []
    for i in cs:
        trees.append(insert_child(tree,i))
    return trees

def make_generation(n):
    trees = [tuple([0])]
    i=0
    while i<n:
        i+=1
        t_trees = []
        for t in trees:
            t_trees = t_trees+make_children(t)
        trees = t_trees
    return trees

def reflect(tree,nodes):
    """reflect the tree around the y-axis plane"""
    tree_ext = tree[1:]
    tree = tree+tree_ext
    nodes_ext = nodes[1:]
    for i in xrange(1,len(nodes)):
        n = nodes[i]
        el = n.direction.elevation
        tw = -n.direction.twist
        if n.type=='Link':
            nodes_ext[i-1] = Link(direction=Dir(elevation=el,twist=tw),length=n.length,type='Link')
        else:
            nodes_ext[i-1] = Motor(direction=Dir(elevation=el,twist=tw),length=n.length,type='Motor')
    nodes = nodes+nodes_ext
    return tree, nodes

#functions to select nodes for a tree, and estimate total search space
def get_size(tree,ls,ms):
    acc = 1
    for i in xrange(1,len(tree)):
        if is_leaf(tree,i):
            acc *= len(ls)
        else:
            acc *= len(ls+ms)
    return acc

def is_leaf(tree,i):
    return i == len(tree)-1 or tree[i+1]<=tree[i]

def get_design(tree,ls,ms,i):
    """returns the ith design of the robot"""
    nodes = [None,]
    for j in xrange(1,len(tree)):
        if is_leaf(tree,j):
            it = ls
        else:
            it = ls+ms
        ind = i%len(it)
        nodes.append(it[ind])
        i = int(i/len(it))
    return nodes

def get_designs(tree,ls,ms):
    tot = get_size(tree, ls, ms)
    for i in xrange(0,tot):
        nodes = get_design(tree,ls,ms,i)
        tt,tn = reflect(tree,nodes)
        yield [tt,tn,(i+1)/tot]
