import math
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy

def trees(n):
    #generate all unique non-rooted trees with n elements
    #approach: we know the total degree will be (n-1)*2, and each of the n nodes
    #needs a degree of 1 or higher.  If we list the degrees of all the nodes (e.g.
    # for a 4 element chain, the list would be [1,2,2,1]), we can sort the list.
    #Unique lists after sorting will correspond to unique non-rooted trees.  This function
    #generates those lists
    total_degree = (n-1)*2
    length = n

def summer(num):
    if num == 0:
        return 0
    else:
        for i in xrange(0,num):
            pass

def summer(l,val):
    if val == 0:
        return [[0]]
    nums = []
    for i in xrange(1,val+1):
        for j in summer(l-1, val-i):
            nums.append(j.append(i))
    return nums

def fold_nums(l):
    l.sort()
    l_org = deepcopy(l)
    ls = []
    ls.append(tuple(l))
    while l[-1] != sum(l_org):
        i_z = find_nonzero(l)
        l[i_z] = l[i_z]-1
        l[i_z+1] = l[i_z+1]+1
        l.sort()
        ls.append(tuple(l))
    return ls

def gen_start(n):
    #generate the starting list, which a chain, for a non-rooted tree of n nodes,
    #zeroed)
    if n>1:
        l = [0,0]
        l = l+[1]*(n-2)
    else:
        l = [0]
    return l

def find_nonzero(l):
    for i,e in enumerate(l):
        if e != 0:
            return i
    return None

def test_summer():
    print summer(4,2)

def test_fold_nums():
    ls = gen_start(6)
    print '6:',len(fold_nums(ls))
    ls = gen_start(7)
    print '7:',len(fold_nums(ls))
    ls = gen_start(8)
    print '8:',len(fold_nums(ls))

def test_gen_start():
    print gen_start(3)
    print gen_start(4)
    print gen_start(5)

if __name__ == '__main__':
    test_gen_start()
    test_fold_nums()
