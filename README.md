# Phylogenetic Pipeline (_phyloGen_)

*by Younginn Park*

## Summary

The Phylogenetic Pipeline is a set of tools designed to construct phylogenetic trees using different methods, like consensus or supertree, that aim to automate the process of reconstructing species trees given a list of species of interest and relevant genomic sequences (more details in the main presentation file `phylo_prezi.pdf`).

The benchmark set of species used in this task comes from the [article](https://pubmed.ncbi.nlm.nih.gov/26400318/) by F. Póntigo, M. Moraga and S.V. Flores, *Molecular phylogeny and a taxonomic proposal for the genus Streptococcus*.

## Usage

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

## Analysis Documents

Tree analysis outline can be found in: `analysis.pdf` and `phylo_prezi.pdf`

## Trees Name Guide

`ml_tree.txt` - species trees made with ML

`trees_[alias].txt` - gene trees (NJ) for specific tasks

Aliases:
- `np` - no paralogs for supertree, trees size 3 to 23 (2111)
- `cnp` - no paralogs for consensus tree, only size=23, i.e. 1-1 with taxa set (461)
- `bnp` - no paralogs, filtered with bootstrap, only with high split support (1743)
- `bcnp` - no paralogs, filtered with bootstrap, 1-1 with taxa set (206)
- `p` - with paralogs, size 3 to 23 (4187)

## [DevLog](https://github.com/young-sudo/phyloGen-devlog)

More details can be found in the `gp_projekt_devlog.ipynb` notebook file with task descriptions, links to tools and development milestones.
