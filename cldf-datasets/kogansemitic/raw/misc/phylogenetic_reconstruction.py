from lingpy.convert.strings import write_nexus
from lingpy.compare.partial import Partial
from lingpy.convert.plot import plot_tree

# Load the necessary data
part = Partial.from_cldf('cldf/cldf-metadata.json')

# Compute cognate sets according to SCA and calculate the distance matrix
part.partial_cluster(method='sca', threshold=0.45, ref="cogids", cluster_method="upgma")
part.add_cognate_ids('cogids', 'cogid', idtype='strict')
part.calculate('tree', ref='cogid', tree_calc='upgma')
out = write_nexus(part, mode='splitstree', filename='distance_matrix.nex')
part.output('dst', filename='distance_matrix')
plot_tree(str(part.tree))
print(part.tree.asciiArt())

# Compute cognate sets according to LexStat and calculate the distance matrix
# part.get_partial_scorer(runs=1000)
# part.partial_cluster(method='lexstat', threshold=0.55, cluster_method='upgma', ref="lexstatids")
# part.add_cognate_ids('lexstatids', 'lexstatid', idtype='strict')
# part.calculate('tree', ref='lexstatid', tree_calc='upgma', force=True)
# part.output('dst', filename='distance_matrix')
# plot_tree(str(part.tree))
# print(part.tree.asciiArt())