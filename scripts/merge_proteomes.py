#!/usr/bin/env python3

import pandas as pd
from PhyloPipeline import extract_aliases, extract_species
from Bio import SeqIO

def main():
    # Organize output from run_fetch_proteomes.sh
    species = []
    with open("org_spec.txt", "r") as f:
        for line in f.readlines():
            text = line.rstrip()
            if text:
                species.append(text)

    accessions = []
    with open("org_accs.txt", "r") as f:
        for line in f.readlines():
            text = line.rstrip()
            if text:
                accessions.append(line.rstrip())

    data = pd.DataFrame.from_dict({'raw_species': species, 'accessions': accessions}, orient='columns')

    # Set species
    data['species'] = data['raw_species'].apply(extract_species)

    # Set aliases
    data['aliases'] = data['species'].apply(extract_aliases)


    # Rename sequences to alias_num
    # Merge all genomes to one fasta

    base_path = "ncbi_dataset"
    prot_path = f"{base_path}/data"
    seq_path = f"{base_path}/sequences"
    prot_filename = "protein.faa"

    output_sequences = []

    for acc in data['accessions']:
        fasta_file_path = os.path.join(prot_path, acc, prot_filename)
        with open(fasta_file_path) as handle:
            num = 1
            for record in SeqIO.parse(handle, "fasta"):
                alias = data.loc[data['accessions'] == acc, 'aliases'].values[0]
                new_identifier = f"{alias}_{num}"
                record.id = new_identifier
                record.description = ""
                output_sequences.append(record)
                num += 1

    output_file_path = 'sequences.fasta'

    SeqIO.write(output_sequences, output_file_path, 'fasta')
    print(f"Sequences saved to {output_file_path}")

    del output_sequences
