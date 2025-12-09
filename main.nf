#!/usr/bin/env nextflow

nextflow.enable.dsl=2

include {  } from './modules/genes.nf'
include {  } from './modules/consensus.nf'
include {  } from './modules/supertree.nf'

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


species_ch = Channel.to("${params.input}")

workflow {
    gene_trees_ch = 
}
