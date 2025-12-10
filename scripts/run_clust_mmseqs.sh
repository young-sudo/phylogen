#!/bin/bash

# Remove any previous output
rm clstrs_mmseqs_cluster.tsv

# Fasta file with sequences to cluster
# FASTA="sequences.fasta"

FASTA=$1

# # Activate environment for genomics
# # genev
# mamba run -n genenv mmseqs easy-cluster "$FASTA" clstrs_mmseqs tmp --min-seq-id 0.3
# min_seq_id 0.3 is a rule of thumb for homologs

mmseqs easy-cluster "$FASTA" clstrs_mmseqs tmp --min-seq-id 0.3

rm clstrs_mmseqs_all_seqs.fasta
rm clstrs_mmseqs_rep_seq.fasta
rm -r tmp
