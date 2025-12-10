#!/usr/bin/env nextflow

process MAKE_CONSENSUS_TREE {
    input:
        path gene_trees_ch
    
    output:
        val "tree_c.txt"

    script:
        """
        python3 scripts/run_genome_trees.py
        """
}
