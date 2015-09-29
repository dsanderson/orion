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

def pplot(ax,tree,nodes):
    #make a 3d plot of the robot described in the trees+nodes
    ml = 0.5
    vecs = [None]*len(tree)
    vecs[0] = (0,0,0)
    for i in xrange(1,len(vecs)):
        p = find_parent(tree,i)
        x = vecs[p][0]+math.cos(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*nodes[i].length
        y = vecs[p][1]+math.sin(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*nodes[i].length
        z = vecs[p][2]+math.sin(nodes[i].direction.elevation)*nodes[i].length
        vecs[i] = (x,y,z)
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax.hold(True)
    #plot root location
    ax.scatter([vecs[0][0]],[vecs[0][1]],[vecs[0][2]],'r.',s=20)
    for i in xrange(1,len(vecs)):
        #plot links
        if nodes[i].type=='Link':
            p = find_parent(tree,i)
            xs = [vecs[p][0],vecs[i][0]]
            ys = [vecs[p][1],vecs[i][1]]
            zs = [vecs[p][2],vecs[i][2]]
            ax.plot(xs,ys,zs,'k-')
        else:
            p = i
            xs = [vecs[p][0],vecs[p][0]+math.cos(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*ml]
            ys = [vecs[p][1],vecs[p][1]+math.sin(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*ml]
            zs = [vecs[p][2],vecs[p][2]+math.sin(nodes[i].direction.elevation)*ml]
            ax.plot(xs,ys,zs,'b-')
    #ax.view_init(elev=ang[0],azim=ang[1])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    #print vecs

def pplot_2d(ax,tree,nodes,a1,a2):
    #make a 3d plot of the robot described in the trees+nodes
    ml = 0.5
    vecs = [None]*len(tree)
    vecs[0] = (0,0,0)
    for i in xrange(1,len(vecs)):
        p = find_parent(tree,i)
        x = vecs[p][0]+math.cos(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*nodes[i].length
        y = vecs[p][1]+math.sin(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*nodes[i].length
        z = vecs[p][2]+math.sin(nodes[i].direction.elevation)*nodes[i].length
        vecs[i] = (x,y,z)
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax.hold(True)
    #plot root location
    ax.scatter([vecs[0][0]],[vecs[0][1]],[vecs[0][2]],'r')
    for i in xrange(1,len(vecs)):
        #plot links
        if nodes[i].type=='Link':
            p = find_parent(tree,i)
            xs = [vecs[p][0],vecs[i][0]]
            ys = [vecs[p][1],vecs[i][1]]
            zs = [vecs[p][2],vecs[i][2]]
            axs = (xs,ys,zs)
            ax.plot(axs[a1[0]],axs[a2[0]],'k-')
        else:
            p = i
            xs = [vecs[p][0],vecs[p][0]+math.cos(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*ml]
            ys = [vecs[p][1],vecs[p][1]+math.sin(nodes[i].direction.twist)*math.cos(nodes[i].direction.elevation)*ml]
            zs = [vecs[p][2],vecs[p][2]+math.sin(nodes[i].direction.elevation)*ml]
            axs = (xs,ys,zs)
            ax.plot(axs[a1[0]],axs[a2[0]],'b-')
    #ax.view_init(elev=ang[0],azim=ang[1])
    ax.set_xlabel(a1[1])
    ax.set_ylabel(a2[1])

def botplot(tree,node,save= None):
    fig = plt.figure()
    #draw y-axis view_
    #draw z-axis view_
    ax1 = fig.add_subplot(221)
    a1 = (0,'x')
    a2 = (2,'z')
    pplot_2d(ax1,tree,node,a1,a2)
    ax2 = fig.add_subplot(222)
    a1 = (0,'x')
    a2 = (1,'y')
    pplot_2d(ax2,tree,node,a1,a2)
    #draw x-axis view_
    ax3 = fig.add_subplot(223)
    a1 = (1,'y')
    a2 = (2,'z')
    pplot_2d(ax3,tree,node,a1,a2)
    #draw isometric view
    #draw y-axis view_
    ax4 = fig.add_subplot(224, projection='3d')
    ang4 = (math.pi/3,math.pi/6)
    pplot(ax4,tree,node)
    #ax4.elev=ang4[0]
    #ax4.azim=ang4[1]
    if save!=None:
        fig.savefig(save,bbox_inches='tight')
        #plt.close(fig)

def test_plot():
    t6 = [0,1,2,3,1]
    nodes = [None,ls[5],ms[2],ls[1],ls[4]]
    t7, n2 = reflect(t6,nodes)
    #pplot(t7,n2,(0.0,0.0))
    botplot(t7,n2)
    plt.show()

def test_get_size(ls,ms):
    tree = [0,1,2]
    print tree, get_size(tree,ls,ms)
    tree = [0,1,1]
    print tree, get_size(tree,ls,ms)

def test_gen_designs(ls,ms):
    s = os.getcwd()
    s = os.path.join(s,'renders')
    tree = [0,1,2,1]
    tot = get_size(tree,ls,ms)
    for i, d in enumerate(get_designs(tree,ls,ms)):
        print 'Item {} of {}, {:.2%}\r'.format(i,tot,d[2])
        fs = os.path.join(s,str(i)+'.png')
        botplot(d[0],d[1],save=fs)
        if i%10==0:
            plt.close('all')
    print ''

Motor = collections.namedtuple('Motor',['direction','length','type'])
Link = collections.namedtuple('Link',['direction','length','type'])
Dir = collections.namedtuple('Dir',['elevation','twist'])

#build lists of possible motors and links
#angs = [Dir(elevation=math.pi/2,twist=0.0),
#       Dir(elevation=0.0,twist=0.0),Dir(elevation=0.0,twist=math.pi/2),
#       Dir(elevation=0.0,twist=math.pi),Dir(elevation=0.0,twist=-math.pi/2),
#       Dir(elevation=-math.pi/2,twist=0.0)]
angs = [Dir(elevation=0.0,twist=0.0),
       Dir(elevation=math.pi/4,twist=math.pi/4),Dir(elevation=math.pi/4,twist=3*math.pi/4),
       Dir(elevation=-math.pi/4,twist=math.pi/4),Dir(elevation=-math.pi/4,twist=3*math.pi/4),
       Dir(elevation=0.0,twist=math.pi)]
#build list of possible motors
ms = []
for a in angs:
    ms.append(Motor(direction=a,length=0.0,type='Motor'))
#build list of possible links
lengs = [1.0]#[1.25,1.0,0.25]
ls = []
for l in lengs:
    for a in angs:
        ls.append(Link(length=l,direction=a,type='Link'))

#test_get_size(ls,ms)
test_gen_designs(ls,ms)
