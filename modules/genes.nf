#!/usr/bin/env nextflow

process FETCH_PROTEOMES {
    input:
        val species_ch
    
    output:
        val "sequences.fasta", emit: proteomes_ch
    
    script:
        """
        scripts/run_fetch_proteomes.sh "${species_ch}" && \
        python3 scripts/merge_proteomes.py
        """
}
// 

process CLUSTER_GENES {
    input:
        path proteomes_ch
    
    output:
        path "sequences/*", emit: clusters_ch

    script:
        """
        scripts/run_clust_mmseqs.sh "${proteomes_ch}" && \
        python3 scripts/save_clusters.py
        """
}


process MAKE_GENE_TREES {
    input:
        path clusters_ch
    
    output:
        val "trees_np.txt", emit: gene_trees_ch

    script:
        """
        python3 scripts/run_gene_trees.py
        """
}

process BOOTSTRAP_ANALYSIS {
    input:
        path clusters_ch

    output:
        path "trees_bnp.txt", emit: bootstrap_trees_ch

    script:
        """
        python3 scripts/run_bootstrap_analysis.py
        """
}
