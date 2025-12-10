#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include { FETCH_PROTEOMES; CLUSTER_GENES;
          MAKE_GENE_TREES; BOOTSTRAP_ANALYSIS } from './modules/genes.nf'
include { MAKE_CONSENSUS_TREE } from './modules/consensus.nf'
include { MAKE_SUPERTREE } from './modules/supertree.nf'

params.mode = params.mode ?: null
params.input = params.input ?: "data/species.txt"
params.output_dir = params.output_dir ?: "results"


if ( params.help ) {
    log.info """
    Usage:
      nextflow run main.nf -profile conda --mode consensus --input data/species.txt --output_dir results

    Parameters:
       -profile           standard|conda|docker|singularity|slurm
      --mode              consensus|supertree
      --bootstrap         add option to run bootstrap analysis
      --input             txt file with species, one per line
      --output_dir        dir path
    """
    exit 0
}

// validate mode
if (!params.mode) {
    error "Missing required parameter: --mode. Must be 'consensus' or 'supertree'."
}

if ( params.mode != 'consensus' && params.mode != 'supertree' ) {
    throw new IllegalArgumentException("Invalid mode: ${params.mode}. Allowed values: consensus, supertree")
}

workflow { 
    species_ch = Channel.to("${params.input}")
    proteomes_ch = FETCH_PROTEOMES(species_ch)
    clusters_ch = CLUSTER_GENES(proteomes_ch)

    if ( params.bootstrap ) {
        gene_trees_ch = BOOTSTRAP_ANALYSIS(clusters_ch)
    } else {
        gene_trees_ch = MAKE_GENE_TREES(clusters_ch)
    }

    if ( params.mode == 'consensus' ) {
        MAKE_CONSENSUS_TREE(gene_trees_ch)
    } else if (params.mode == 'supertree') {
        MAKE_SUPERTREE(gene_trees_ch)
    } else {
        error "Unknown mode: ${params.mode}"
    }
}
