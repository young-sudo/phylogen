#!/usr/bin/env nextflow

process MAKE_SUPERTREE {
    input:
        path gene_trees_ch
    
    output:
        val "tree_s.txt"

    script:
        """
        python3 scripts/run_fasturec.sh "${gene_trees_ch}"
        """
}
