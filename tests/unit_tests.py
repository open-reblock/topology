import unittest
from graph import my_graph_helpers as mgh
from graph import my_graph as mg
from matplotlib import pyplot as plt
import math 
from collections import defaultdict

def plot_test_dual(myG):
    """ plots the weak duals based on testGraph"""

    S0 = myG.weak_dual()

    myG.plot_roads(update=False)
    S0.plot(node_color='g', edge_color='g', width=3)

def get_test_graph_lattice(n, xshift=0, yshift=0, scale=1):
    """returns a square lattice of dimension nxn   """
    nodelist = {}
    for j in range(0, n**2):
        x = (math.fmod(j, n))*scale + xshift
        y = (math.floor(j/n))*scale + yshift
        nodelist[j] = mg.MyNode((x, y))

    edgelist = defaultdict(list)

    for i in nodelist.keys():
        ni = nodelist[i]
        for j in nodelist.keys():
            nj = nodelist[j]
            if ni != nj:
                if mgh.distance(ni, nj) == scale:
                    edgelist[ni].append(nj)

    myedgelist = []

    for n1 in edgelist.keys():
        n2s = edgelist[n1]
        for n2 in n2s:
            myedgelist.append(mg.MyEdge((n1, n2)))

    lattice = mgh.graphFromMyEdges(myedgelist)
    lattice.name = "lattice"

    return lattice


def get_test_graph():
    n = {}
    n[1] = mg.MyNode((0, 0))
    n[2] = mg.MyNode((0, 1))
    n[3] = mg.MyNode((0, 2))
    n[4] = mg.MyNode((0, 3))
    n[5] = mg.MyNode((1, 2))
    n[6] = mg.MyNode((1, 3))
    n[7] = mg.MyNode((0, 4))
    n[8] = mg.MyNode((-1, 4))
    n[9] = mg.MyNode((-1, 3))
    n[10] = mg.MyNode((-1, 2))
    n[11] = mg.MyNode((1, 4))
    n[12] = mg.MyNode((-2, 3))

    lat = mg.MyGraph(name="S0")
    lat.add_edge(mg.MyEdge((n[1], n[2])))
    lat.add_edge(mg.MyEdge((n[2], n[3])))
    lat.add_edge(mg.MyEdge((n[2], n[5])))
    lat.add_edge(mg.MyEdge((n[3], n[4])))
    lat.add_edge(mg.MyEdge((n[3], n[5])))
    lat.add_edge(mg.MyEdge((n[3], n[9])))
    lat.add_edge(mg.MyEdge((n[4], n[5])))
    lat.add_edge(mg.MyEdge((n[4], n[6])))
    lat.add_edge(mg.MyEdge((n[4], n[7])))
    lat.add_edge(mg.MyEdge((n[4], n[8])))
    lat.add_edge(mg.MyEdge((n[4], n[9])))
    lat.add_edge(mg.MyEdge((n[5], n[6])))
    lat.add_edge(mg.MyEdge((n[6], n[7])))
    lat.add_edge(mg.MyEdge((n[7], n[8])))
    lat.add_edge(mg.MyEdge((n[8], n[9])))
    lat.add_edge(mg.MyEdge((n[9], n[10])))
    lat.add_edge(mg.MyEdge((n[3], n[10])))
    lat.add_edge(mg.MyEdge((n[2], n[10])))
    lat.add_edge(mg.MyEdge((n[7], n[11])))
    lat.add_edge(mg.MyEdge((n[6], n[11])))
    lat.add_edge(mg.MyEdge((n[10], n[12])))
    lat.add_edge(mg.MyEdge((n[8], n[12])))

    return lat

class GraphTests(unittest.TestCase): 
    def test_graph(self):
        master = get_test_graph_lattice(4)

        S0 = master.copy()

        S0.define_roads()
        S0.define_interior_parcels()

        road_edge = S0.myedges()[1]

        S0.add_road_segment(road_edge)

        S0.define_interior_parcels()

        plot_test_dual(S0)

        plt.show()

class GraphHelperTests(unittest.TestCase):
    def test_edges_equality(self):
        """checks that myGraph points to myEdges correctly   """
        testG = get_test_graph()
        testG.trace_faces()
        outerE = list(testG.outerface.edges)[0]
        return outerE is testG.G[outerE.nodes[0]][outerE.nodes[1]]['myedge']

    def __test_nodes(n1, n2):
        """ returns true if two nodes are evaluated as the same"""
        eq_num = len(set(n1).intersection(set(n2)))
        is_num = len(set([id(n) for n in n1])
                     .intersection(set([id(n) for n in n2])))
        print("is eq? ", eq_num, "is is? ", is_num)


    def __test_interior_is_inner(myG):
        myG.inner_facelist
        myG.interior_parcels
        in0 = myG.interior_parcels[0]
        ans = in0 in myG.inner_facelist

        # print("interior in inner_facelist is {}".format(ans))

        return ans


    def testGraphEquality(self):
        n = {}
        n[1] = mg.MyNode((0, 0))
        n[2] = mg.MyNode((0, 1))
        n[3] = mg.MyNode((1, 1))
        n[4] = mg.MyNode((1, 0))
        n[5] = mg.MyNode((0, 0))  # actually equal
        n[6] = mg.MyNode((0.0001, 0.0001))  # within rounding
        n[7] = mg.MyNode((0.1, 0.1))  # within threshold
        n[8] = mg.MyNode((0.3, 0.3))  # actually different

        G = mg.MyGraph(name="S0")
        G.add_edge(mg.MyEdge((n[1], n[2])))
        G.add_edge(mg.MyEdge((n[2], n[3])))
        G.add_edge(mg.MyEdge((n[3], n[4])))
        G.add_edge(mg.MyEdge((n[4], n[5])))
        G.add_edge(mg.MyEdge((n[5], n[6])))
        G.add_edge(mg.MyEdge((n[6], n[7])))
        G.add_edge(mg.MyEdge((n[7], n[8])))

        return G, n


    def __centroid_test():
        n = {}
        n[1] = mg.MyNode((0, 0))
        n[2] = mg.MyNode((0, 1))
        n[3] = mg.MyNode((1, 1))
        n[4] = mg.MyNode((1, 0))
        n[5] = mg.MyNode((0.55, 0))
        n[6] = mg.MyNode((0.5, 0.9))
        n[7] = mg.MyNode((0.45, 0))
        n[8] = mg.MyNode((0.4, 0))
        n[9] = mg.MyNode((0.35, 0))
        n[10] = mg.MyNode((0.3, 0))
        n[11] = mg.MyNode((0.25, 0))
        nodeorder = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 1]
        nodetups = [(n[nodeorder[i]], n[nodeorder[i+1]])
                    for i in range(0, len(nodeorder)-1)]
        edgelist = [mg.MyEdge(i) for i in nodetups]

        f1 = mg.MyFace(nodetups)
        S0 = graphFromMyFaces([f1])

        S0.define_roads()
        S0.define_interior_parcels()

        S0.plot_roads(parcel_labels=True)

        return S0, f1, n, edgelist
 
    def get_test_matrix():
        testmat = []
        dim = 4
        for i in range(0, dim):
            k = []
            for j in range(0, dim):
                k.append((i-j)*(i-j))
            testmat.append(k)
        return testmat

    def test_graph_helper(self):
        master = get_test_graph_lattice(7)
        master.name = "Lat_0"
        master.define_roads()
        master.define_interior_parcels()
        # S0, barrier_edges = build_lattice_barrier(S0)
        # barGraph = graphFromMyEdges(barrier_edges)
        S0 = master.copy()

        # S0.plot_roads(master, update=False, new_plot=True)

        plot_test_dual(S0)

        S0 = master.copy()
        new_roads_i = mgh.build_all_roads(S0, master, alpha=2, wholepath=True,
                                      barriers=False, plot_intermediate=False,
                                      strict_greedy=True, vquiet=True,
                                      outsidein=True)

        S0.plot_roads()
        print("outside to in" + str(new_roads_i))

        S0 = master.copy()
        new_roads_i = mgh.build_all_roads(S0, master, alpha=2, wholepath=True,
                                      barriers=False, plot_intermediate=True,
                                      strict_greedy=True, vquiet=True,
                                      outsidein=False)

        S0.plot_roads()
        print("inside out" + str(new_roads_i))

if __name__ == '__main__':
    unittest.main()