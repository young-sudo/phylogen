# Phylogenetic Pipeline (_phyloGen_)

*by Younginn Park*

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Biopython](https://img.shields.io/badge/Biopython-50C878?style=for-the-badge&logo=python&logoColor=white)
![DendroPy](https://img.shields.io/badge/DendroPy-FBEC5D?style=for-the-badge&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-3c4549?style=for-the-badge&logo=gnubash&logoColor=white)
![Nextflow](https://img.shields.io/badge/Nextflow-23CC85?style=for-the-badge&logo=nextflow&logoColor=white)

## Summary

The Phylogenetic Pipeline is a set of tools designed to construct phylogenetic trees using different methods, consensus or supertree, that aim to automate the process of reconstructing species trees given a list of species of interest and relevant genomic sequences.

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

To fetch proteomes for organism names in `species.txt` (one taxon per line) from NCBI Datasets:

```bash
./run_fetch_proteomes.sh species.txt
```

`PhyloPipeline.py` - package with helper functions for other scripts

### Sequence clustering

To run clustering on sequences in `sequences.fasta`

```bash
./run_clust_mmseqs.sh sequences.fasta
```

### MSA and NJ

For constructing gene trees using Multiple Sequence Alignment (MSA) and Neighbor Joining (NJ) method

```bash
run_gene_trees.py
```

### Genome Trees

For constructing a consensus tree with DendroPy

```bash
run_genome_tree.py
```

For constructing a supertree with Fasturec

```bash
run_fasturec.sh
```

## Results

### Trees Name Guide

`ml_tree.txt` - species trees made with ML (Maximum Likelihood) method

`trees_[alias].txt` - gene trees (NJ) for specific task

Aliases:
- `np` - no paralogs for supertree, trees size 3 to 23 (2111)
- `cnp` - no paralogs for consensus tree, only size=23, i.e. 1-1 with taxa set (461)
- `bnp` - no paralogs, filtered with bootstrap, only with high split support (1743)
- `bcnp` - no paralogs, filtered with bootstrap, 1-1 with taxa set (206)
- `p` - with paralogs, size 3 to 23 (4187)

File names for phylogenetic trees are:
- `bctree_np` - bootstrap consensus tree constructed without paralogs
- `bstree_np` - bootstrap supertree constructed without paralogs
- `ctree_np` - consensus tree constructed without paralogs
- `stree_np` - supertree constructed without paralogs
- `stree_p` - supertree constructed with paralogs

## Analysis Documents

Tree analysis outline can be found in: `analysis.pdf` and `phylo_prezi.pdf`

>More details about the results can be found in the main presentation file `phylo_prezi.pdf`

## References

Tools used throughout the pipeline:

Peter J. A. Cock et al, Biopython: freely available Python tools for computational molecular biology and bioinformatics, Bioinformatics, Volume 25, Issue 11, June 2009, Pages 1422–1423, [https://doi.org/10.1093/bioinformatics/btp163](https://doi.org/10.1093/bioinformatics/btp163)

Jeet Sukumaran, Mark T. Holder, DendroPy: a Python library for phylogenetic computing, Bioinformatics, Volume 26, Issue 12, June 2010, Pages 1569–1571, [https://doi.org/10.1093/bioinformatics/btq228](https://doi.org/10.1093/bioinformatics/btq228)

NCBI Datasets CLI Tools, [https://github.com/ncbi/datasets](https://github.com/ncbi/datasets), [https://www.ncbi.nlm.nih.gov/datasets](https://www.ncbi.nlm.nih.gov/datasets), accessed Jan 2024, 

Katoh, K., & Standley, D. M. (2013). MAFFT multiple sequence alignment software version 7: improvements in performance and usability. Molecular biology and evolution, 30(4), 772–780. [https://doi.org/10.1093/molbev/mst010](https://doi.org/10.1093/molbev/mst010)

Steinegger, M., Söding, J. MMseqs2 enables sensitive protein sequence searching for the analysis of massive data sets. Nat Biotechnol 35, 1026–1028 (2017). [https://doi.org/10.1038/nbt.3988](https://doi.org/10.1038/nbt.3988)

Górecki, P. et al (2012). GTP Supertrees from Unrooted Gene Trees: Linear Time Algorithms for NNI Based Local Searches. In: Bleris, L., Măndoiu, I., Schwartz, R., Wang, J. (eds) Bioinformatics Research and Applications. ISBRA 2012. Lecture Notes in Computer Science(), vol 7292. Springer, Berlin, Heidelberg. [https://doi.org/10.1007/978-3-642-30191-9_11](https://doi.org/10.1007/978-3-642-30191-9_11), Fasturec, [https://bioputer.mimuw.edu.pl/gorecki/fasturec/](https://bioputer.mimuw.edu.pl/gorecki/fasturec/) or [https://bitbucket.org/pgor17/fasturec/src/master/](https://bitbucket.org/pgor17/fasturec/src/master/), accessed Jan 2024
