from descartes import PolygonPatch
from matplotlib import pyplot as plt
import my_graph_helpers as mgh
import random
import shapefile
from matplotlib import cm, colors

BLUE = '#5292c0'
GRAY = '#444444'
random.seed(11235813)

# block.plot_roads(master=block, new_plot=False, update=True)
# block.plot_weak_duals(new_figure=False)
# ax = fig.gca()
# for shape in shapes.iterShapes():
# 	poly = shape.__geo_interface__
# 	ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=GRAY, alpha=0.5, zorder=2))
# ax.axis('scaled')
# print "shapefiles plotted"
# plt.show()


def plot_shapefile(filename, name):
	shapes = shapefile.Reader(filename)
	fig = plt.figure()
	ax = fig.gca()
	for shape in shapes.iterShapes():
		poly = shape.__geo_interface__
		# print poly
		ax.add_patch(PolygonPatch(poly, fc="#FFFFFF", ec="#000000", alpha=1, zorder=2))
	ax.axis('scaled')
	plt.axis('off')
	plt.savefig(name + '_shapefile.svg')
	plt.savefig(name + '_shapefile.png')
	plt.draw()
	plt.show()

def main(filename, threshold=1, name=""):
	shapes = shapefile.Reader(filename)
	
	original = mgh.import_and_setup(filename, threshold=threshold)
	blocklist = original.connected_components()
	
	# fig1 = plt.figure()
	# for block in blocklist:
	# 	block.plot_roads(master=block, new_plot=False, update=False)
	# fig1.gca().axis('scaled')
	# plt.axis('off')
	# plt.draw()
	# plt.savefig(name + '_old_roads_tight.svg', bbox_inches='tight')
	# plt.savefig(name + '_old_roads_tight.png', bbox_inches='tight')
	# print "old roads plotted"

	fig2 = plt.figure()
	for block in blocklist:
		block.plot_roads(master=None, new_plot=False, update=True)
	fig2.gca().axis('scaled')
	plt.axis('off')
	plt.draw()
	# plt.savefig('new_roads_tight.svg', bbox_inches='tight')
	plt.savefig(name + '_new_roads_tight.svg', bbox_inches='tight')
	plt.savefig(name + '_new_roads_tight.png', bbox_inches='tight')
	print "new roads plotted"

	# fig3 = plt.figure()
	# ax = fig3.gca()
	# for shape in shapes.iterShapes():
	# 	poly = shape.__geo_interface__
	# 	print poly
	# 	ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=1, zorder=2))
	# ax.axis('scaled')
	# print "shapefiles plotted"
	# plt.draw()

	plt.show()

def impact(filename, threshold=1, name=""):
	cmap = cm.RdYlGn
	# cmap = cm.Reds
	# cmap = cm.Oranges

	print "importing..."
	original = mgh.import_and_setup(filename, threshold=threshold, byblock=True)
	print "getting connected components"
	blocklist = original.connected_components()
	# print type(blocklist[0]).__name__
	# print dir(blocklist[0])
	impacts = []
	for block in blocklist:
		block.define_roads()
		block.define_interior_parcels()
		length = block.interior_length()
		area = sum(face.area for face in block.inner_facelist)
		impacts.append(length/area)
	max_i, min_i = max(impacts), min(impacts)
	# colormap = cm.ScalarMappable(norm=colors.Normalize(vmin=min_i, vmax=max_i), cmap=cmap)
	colormap = cm.ScalarMappable(norm=colors.Normalize(vmin=-max_i, vmax=-min_i), cmap=cmap)
	figure = plt.figure()
	ax = figure.gca()
	for (impact, block) in zip(impacts, blocklist):
		# block.plot(node_color=colormap.to_rgba(impact), node_size=1)
		for face in block.inner_facelist:
			nodes = face.nodes[:-2] + [face.nodes[-1], face.nodes[-2]]
			xs, ys = zip(*[node.loc for node in nodes])
			plt.fill(xs, ys, 
				facecolor=colormap.to_rgba(-impact), 
				edgecolor=colormap.to_rgba(-impact))
			xs, ys = zip(*[node.loc for node in face.nodes])
			plt.fill(xs, ys, 
				facecolor=colormap.to_rgba(-impact), 
				edgecolor=colormap.to_rgba(-impact))
	ax.axis('scaled')
	plt.axis('off')
	plt.savefig(name + '_road_impact.svg')
	plt.savefig(name + '_road_impact.png')
	plt.show()
	

if __name__ == '__main__':
	# plot_shapefile("data/phule_nagar_v6", "pn")
	# main("data/phule_nagar_v6", 0.5, "pn")
	# impact("data/phule_nagar_v6", 0.5, "pn")

	# plot_shapefile("data/epworth_demo", "ep_demo")
	# main("data/epworth_demo", 0.5, "ep_demo")
	# impact("data/epworth_demo", 0.5, "ep_demo")

	# plot_shapefile("data/epworth_before", "epworth")
	# main("data/epworth_before", 0.5, "epworth")
	impact("data/epworth_before", 0.5, "epworth")

	# plot_shapefile("data/Las_Vegas", "lv")
	# main("data/Las_Vegas", 1, "lv")
	# impact("data/Las_Vegas", 1, "lv")

	# main("data/epworth_before", 0.5)
	# main("data/epworth_demo", 1)
	# main("data/capetown")

	# main('data/private/WestpointEnumerationShapefile', 0, "westpoint")
	# plot_shapefile('data/private/WestpointEnumerationShapefile', "westpoint")
	# impact("data/epworth_before", 0.5)