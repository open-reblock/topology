import unittest
# from context.topology import my_graph_helpers as mgh 
from .topology import my_graph_helpers as mgh

class GraphTests(unittest.TestCase): 
    def test_graph(self):
        master = mgh.testGraphLattice(4)

        S0 = master.copy()

        S0.define_roads()
        S0.define_interior_parcels()

        road_edge = S0.myedges()[1]

        S0.add_road_segment(road_edge)

        S0.define_interior_parcels()

        mgh.test_dual(S0)

        plt.show()

class GraphHelperTests(unittest.TestCase):
    pass 

if __name__ == '__main__':
    unittest.main()