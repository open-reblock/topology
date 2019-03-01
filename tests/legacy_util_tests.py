import unittest
import numpy as np
import random
from graph import my_graph as mg
from graph import my_graph_helpers as mgh

# myG geometry functions
def legacy_distance(mynode0, mynode1):
    return np.sqrt(legacy_distance_squared(mynode0, mynode1))


def legacy_distance_squared(mynode0, mynode1):
    return (mynode0.x-mynode1.x)**2+(mynode0.y-mynode1.y)**2


def legacy_sq_distance_point_to_segment(target, myedge):
    """returns the square of the minimum distance between mynode
    target and myedge.   """
    n1 = myedge.nodes[0]
    n2 = myedge.nodes[1]

    if myedge.length == 0:
        sq_dist = distance_squared(target, n1)
    elif target == n1 or target == n2:
        sq_dist = 0
    else:
        px = float(n2.x - n1.x)
        py = float(n2.y - n1.y)
        u = float((target.x - n1.x)*px + (target.y - n1.y)*py)/(px*px + py*py)
        if u > 1:
            u = 1
        elif u < 0:
            u = 0
        x = n1.x + u*px
        y = n1.y + u*py

        dx = x - target.x
        dy = y - target.y

        sq_dist = (dx * dx + dy * dy)
    return sq_dist


def legacy_intersect(e1, e2):
    """ returns true if myedges e1 and e2 intersect """
    # fails for lines that perfectly overlap.
    def legacy_ccw(a, b, c):
        return (c.y-a.y)*(b.x-a.x) > (b.y-a.y)*(c.x-a.x)

    a = e1.nodes[0]
    b = e1.nodes[1]
    c = e2.nodes[0]
    d = e2.nodes[1]

    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def legacy_are_parallel(e1, e2):
    """ returns true if myedges e1 and e2 are parallel """
    a = e1.nodes[0]
    b = e1.nodes[1]
    c = e2.nodes[0]
    d = e2.nodes[1]

    # check if parallel; handling divide by zero errors
    if a.x == b.x and c.x == d.x:  # check if both segments are flat
        parallel = True
    # if one is flat and other is not
    elif (a.x - b.x)*(c.x - d.x) == 0 and (a.x - b.x) + (c.x - d.x) != 0:
        parallel = False
    # if neither segment is flat and slopes are equal
    elif (a.y-b.y)/(a.x-b.x) == (c.y-d.y)/(c.x-d.x):
        parallel = True
    # n either segment is flat, slopes are not equal
    else:
        parallel = False
    return parallel


def legacy_segment_distance_sq(e1, e2):
    """returns the square of the minimum distance between myedges e1 and e2."""
    # check different
    if e1 == e2:
        sq_distance = 0
    # check parallel/colinear:
    # lines are not parallel/colinear and intersect
    if not are_parallel(e1, e2) and intersect(e1, e2):
        sq_distance = 0
    # lines don't intersect, aren't parallel
    else:
        d1 = sq_distance_point_to_segment(e1.nodes[0], e2)
        d2 = sq_distance_point_to_segment(e1.nodes[1], e2)
        d3 = sq_distance_point_to_segment(e2.nodes[0], e1)
        d4 = sq_distance_point_to_segment(e2.nodes[1], e1)
        sq_distance = min(d1, d2, d3, d4)

    return sq_distance


# vector math
def legacy_bisect_angle(a, b, c, epsilon=0.2, radius=1):
    """ finds point d such that bd bisects the lines ab and bc."""
    ax = a.x - b.x
    ay = a.y - b.y

    cx = c.x - b.x
    cy = c.y - b.y

    a1 = mg.MyNode(((ax, ay))/np.linalg.norm((ax, ay)))
    c1 = mg.MyNode(((cx, cy))/np.linalg.norm((cx, cy)))

    # if vectors are close to parallel, find vector that is perpendicular to ab
    # if they are not, then find the vector that bisects a and c
    if abs(np.cross(a1.loc, c1.loc)) < 0 + epsilon:
        # print("vectors {0}{1} and {1}{2} are close to //)".format(a,b,c)
        dx = -ay
        dy = ax
    else:
        dx = (a1.x + c1.x)/2
        dy = (a1.y + c1.y)/2

    # convert d values into a vector of length radius
    dscale = ((dx, dy)/np.linalg.norm((dx, dy)))*radius
    myd = mg.MyNode(dscale)

    # make d a node in space, not vector around b
    d = mg.MyNode((myd.x + b.x, myd.y + b.y))

    return d


def legacy_find_negative(d, b):
    """finds the vector -d when b is origin """
    negx = -1*(d.x - b.x) + b.x
    negy = -1*(d.y - b.y) + b.y
    dneg = mg.MyNode((negx, negy))
    return dneg


# clean up and probability functions
def legacy_WeightedPick(d):
    """picks an item out of the dictionary d, with probability proportional to
    the value of that item.  e.g. in {a:1, b:0.6, c:0.4} selects and returns
    "a" 5/10 times, "b" 3/10 times and "c" 2/10 times. """
    r = random.uniform(0, sum(d.values()))
    s = 0.0
    for k, w in d.items():
        s += w
        if r < s:
            return k
    return k

class LegacyUtilTests(unittest.TestCase):
    def test_distance(self):
        node_a = mg.MyNode((0, 1))
        node_b = mg.MyNode((2, 3))

        assert legacy_distance(node_a, node_b) == mgh.distance(node_a, node_b)
    
    def test_distance_squared(self):
        node_a = mg.MyNode((0, 1))
        node_b = mg.MyNode((2, 3))

        assert legacy_distance_squared(node_a, node_b) == mgh.distance_squared(node_a, node_b)
    
    def _test_sq_distance_point_to_segment(self):
        pass
    
    def _test_intersect(self):
        pass
    
    def _test_ccw(self):
        pass
    
    def _test_are_parallel(self):
        pass
    
    def _test_segment_distance_sq(self):
        pass
    
    def _test_bisect_angle(self):
        pass
    
    def _test_find_negative(self):
        pass
    
    def test_WeightedPick(self):
        distribution = {'a':1, 'b':0.6, 'c':0.4}
        
        random.seed(11235813)
        legacy_value = legacy_WeightedPick(distribution)

        np.random.seed(11235813)
        builtin_value = mgh.WeightedPick(distribution)

        assert legacy_value == builtin_value


if __name__ == '__main__':
    unittest.main()