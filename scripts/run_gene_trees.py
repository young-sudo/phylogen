#!/usr/bin/env python

import os
from PhyloPipeline import *

# Alignment for tree construction with NJ method
from Bio.Align.Applications import MafftCommandline


def main():
    cluster_names = fetch_cluster_names()

    mafft_exe = os.path.join("mafft")
    aln_folder = "alns"
    os.makedirs(aln_folder, exist_ok=True)

    seq_folder = "sequences" # dir with clustered seqs

    for cluster in cluster_names:
        mafft_in = os.path.join(seq_folder, f"{cluster}.fasta")
        mafft_out = os.path.join(aln_folder, f"aln_{cluster}.fasta")
        
        # Run Mafft for alignment
        mafft_cline = MafftCommandline(mafft_exe, input=mafft_in)
        stdout, stderr = mafft_cline(stdout=True)

        # Write alignment to file
        with open(mafft_out, "w") as handle:
            handle.write(stdout)

    print("Alignment was successful")

    # https://biopython.org/docs/dev/api/Bio.Phylo.TreeConstruction.html
    from Bio import AlignIO, Phylo
    from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

    # Tree construction with NJ method
    # All trees will be saved into one text file

    calculator = DistanceCalculator("blosum62")

    trees_file = "trees_np.txt"

    # Initiate empty text file
    with open(trees_file, "w") as f:
        pass

    trees_with_negative_lengths = 0

    with open(trees_file, "a") as f:
        for cluster in cluster_names:
            # Load aligned sequences
            alignment = AlignIO.read(os.path.join(aln_folder, f"aln_{cluster}.fasta"), "fasta")
            dm = calculator.get_distance(alignment)
            constructor = DistanceTreeConstructor(calculator)
            tree = constructor.nj(dm) # Construct and return a Neighbor Joining tree.

            # Modify leaf names to first 4 letters (aliases)
            for leaf in tree.get_terminals():
                new_name = leaf.name[:4]
                leaf.name = new_name
            
            # Remove internal node labels
            for internal in tree.get_nonterminals():
                internal.name = ""

            # Check for negative branch lengths
            if any(edge.branch_length is not None and edge.branch_length < 0 for edge in tree.find_clades()):
                trees_with_negative_lengths += 1
                continue

            # Save the tree without internal node labels and branch lengths
            # One tree per line
            Phylo.write([tree], f, format="newick")

    if trees_with_negative_lengths > 0:
        print(f"{trees_with_negative_lengths} trees were discarded due to negative branch lengths.")
    else:
        print("All trees were successfully saved.")
    print("NJ tree construction was completed.")

if __name__ == "__main__":
    main()
