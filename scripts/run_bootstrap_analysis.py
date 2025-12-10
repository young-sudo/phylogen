#!/usr/bin/env python3

from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor
from Bio.Phylo.Consensus import bootstrap_trees
from dendropy import Tree
import subprocess
import os
import numpy as np
# https://biopython.org/wiki/Phylo
# https://biopython.org/docs/dev/api/Bio.Phylo.TreeConstruction.html

from PhyloPipeline import fetch_aliases, fetch_cluster_names

def main():
    # Tree construction with NJ method
    # All trees will be saved into one text file

    cluster_names = fetch_cluster_names()

    aln_folder = "alns"

    times = 100

    calculator = DistanceCalculator("blosum62")

    trees_file = "trees_bnp.txt"

    # Initiate empty text file
    with open(trees_file, "w") as f:
        pass

    trees_with_negative_lengths = 0

    min_support = 0.9 # min, average or median
    low_sup_count = 0

    counter = 0

    for cluster in cluster_names:
        counter += 1
        print(f"Tree {counter}/{len(cluster_names)}")
        # Load aligned sequences
        alignment = AlignIO.read(os.path.join(aln_folder, f"aln_{cluster}.fasta"), "fasta")
        dm = calculator.get_distance(alignment)
        constructor = DistanceTreeConstructor(calculator, method='nj')
        nj_tree = constructor.nj(dm)

        # Check for negative branch lengths
        if any(edge.branch_length is not None and edge.branch_length < 0 for edge in nj_tree.find_clades()):
            trees_with_negative_lengths += 1
            print(f"Tree {counter} is nr {trees_with_negative_lengths} with negative lengths")
            continue


        # If nj_tree is good - do pre-processing for bootstrapping        
        for leaf in nj_tree.get_terminals():
            new_name = leaf.name[:4]
            leaf.name = new_name
        
        # Remove internal node labels
        for internal in nj_tree.get_nonterminals():
            internal.name = ""

        # Create replicate trees
        trees = bootstrap_trees(alignment, times, constructor)

        with open("tmp_repltrees.txt", "w") as f:
            for replicate in list(trees):
                for leaf in replicate.get_terminals():
                    new_name = leaf.name[:4]
                    leaf.name = new_name
                for internal in replicate.get_nonterminals():
                    internal.name = ""
                f.write(replicate.format("newick"))

        Phylo.write([nj_tree], "tmp_nj_tree.txt", format="newick")

        # Construct bootstrap consensus tree
        # installed with DendroPy
        subprocess.run(["sumtrees",
                        "-t", "tmp_nj_tree.txt",
                        "--unrooted",
                        "-i", "newick",
                        "-o", "tmp_boot.txt",
                        "-F", "newick",
                        "tmp_repltrees.txt",
                        "-q", "-r"])

        bctree = Tree.get(path="tmp_boot.txt", schema="newick")

        supports = []
        for node in bctree.nodes():
            supports.append(float(node.annotations["support"].value))

        # support_value = np.min(supports)
        # support_value = np.median(supports)
        support_value = np.mean(supports)

        if support_value < min_support:
            low_sup_count += 1
            print(f"Tree {counter} with {len(supports)} nodes is nr {low_sup_count} with low support: {support_value:.3f}")
            continue
        else:
            print(f"Tree {counter} with {len(supports)} nodes has high support: {support_value:.3f}")
            with open(trees_file, "a") as f:
                Phylo.write([nj_tree], f, format="newick")


    if trees_with_negative_lengths > 0 or low_sup_count > 0:
        print(f"{trees_with_negative_lengths} trees were discarded due to negative branch lengths.")
        print(f"{low_sup_count} trees were discarded due to low support.")
    else:
        print("All trees were successfully saved.")
    print("NJ tree construction was completed.")


if __name__=="__main__":
    main()

