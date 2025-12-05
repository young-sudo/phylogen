# Phylogenetic Pipeline (_phyloGen_)

*by Younginn Park*



## Summary

The Phylogenetic Pipeline is a set of tools designed to construct phylogenetic trees using different methods, like consensus or supertree, that aim to automate the process of reconstructing species trees given a list of species of interest and relevant genomic sequences.

The benchmark set of species used in this task comes from the [article](https://pubmed.ncbi.nlm.nih.gov/26400318/) by F. Póntigo, M. Moraga and S.V. Flores, *Molecular phylogeny and a taxonomic proposal for the genus Streptococcus*.

<div align="center">
  <figure>
    <img src="https://raw.githubusercontent.com/young-sudo/phylogen/main/img/consensus.png" alt="c" width="400"/>
    <img src="https://raw.githubusercontent.com/young-sudo/phylogen/main/img/consensus_bootstrap.png" alt="cb" width="400"/>
    <br>
    <img src="https://raw.githubusercontent.com/young-sudo/phylogen/main/img/supertree.png" alt="s" width="400"/>
    <img src="https://raw.githubusercontent.com/young-sudo/phylogen/main/img/supertree_bootstrap.png" alt="sb" width="400"/>
    <img src="https://raw.githubusercontent.com/young-sudo/phylogen/main/img/supertree_paralogs.png" alt="sp" width="400"/>
    <br>
    <figcaption style="text-align:center;"><em>Figure 1. Outputs from each of the methods and comparisons with the species tree from the publication.</em></figcaption>
  </figure>
</div>

## Usage

(Nextflow implementatioin coming soon...)

## Methodology

### Data preparation

To fetch proteomes for organism names in `species_list.txt` (one taxon per line) from NCBI Datasets:
>`./run_fetch_proteomes.sh species_list.txt`

`PhyloPipeline.py` - package with helper functions for other scripts

### Sequence clustering

To run clustering on sequences in `sequences.fasta`

>`./run_clust_mmseqs.sh sequences.fasta`

### MSA and NJ

>`run_gene_trees.py` - for gene trees

### Genome Trees

>`run_genome_tree.py` - for consensus tree

>`run_fasturec.sh` - for supertree

## Results

### Trees Name Guide

`ml_tree.txt` - species trees made with ML

`trees_[alias].txt` - gene trees (NJ) for specific tasks

Aliases:
- `np` - no paralogs for supertree, trees size 3 to 23 (2111)
- `cnp` - no paralogs for consensus tree, only size=23, i.e. 1-1 with taxa set (461)
- `bnp` - no paralogs, filtered with bootstrap, only with high split support (1743)
- `bcnp` - no paralogs, filtered with bootstrap, 1-1 with taxa set (206)
- `p` - with paralogs, size 3 to 23 (4187)

## Analysis Documents

Tree analysis outline can be found in: `analysis.pdf` and `phylo_prezi.pdf`

>More details about the results can be found in the main presentation file `phylo_prezi.pdf`
