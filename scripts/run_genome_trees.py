#!/usr/bin/env python3

from dendropy import TaxonNamespace, TreeList
from PhyloPipeline import *


def main():
    aliases = fetch_aliases()
    # Initialize a TreeList object
    # Select trees that have a full set of taxa as leaves
    tlist = TreeList.get(path="trees_np.txt",
            schema="newick",
            rooting="default-unrooted",
            taxon_namespace=TaxonNamespace(aliases))

    with open("trees_cnp.txt", "w") as f:
        pass

    # All trees used to make consensus require to have the same set of taxa
    desired_num_leaves = len(aliases)

    # Open the output file in append mode
    with open("trees_cnp.txt", "a") as outfile:
        # Iterate through trees in the TreeList
        for tree in tlist:
            # Check the number of leaves
            num_leaves = len(tree.leaf_nodes())

            # If the number of leaves is equal to 23, append to the new file
            if num_leaves == desired_num_leaves:
                outfile.write(tree.as_string(schema="newick"))

    # Read selected trees
    tlist = TreeList.get(path="trees_cnp.txt",
            schema="newick",
            rooting="default-unrooted",
            taxon_namespace=TaxonNamespace(aliases))
    

    # Construct a majority consensus tree
    consensus_tree = tlist.consensus(min_freq=0.5, is_bipartitions_updated=True)
    ctree = consensus_tree.as_string(schema="newick")
    ctree = ctree.split()[1].rstrip()

    with open("ctree_np.txt", "w") as f:
        f.write(ctree)

if __name__ == "__main__":
    main()
    