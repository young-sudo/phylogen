#!/usr/bin/env python3

import pandas as pd

def get_data():
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

    return data


def fetch_aliases():
    data = get_data()

    def extract_species(raw_species):
        parts = raw_species.split()
        if len(parts) >= 2:
            return ' '.join(parts[:2])
        else:
            return raw_species

    data['species'] = data['raw_species'].apply(extract_species)

    def extract_aliases(species):
        parts = species.split()
        assert len(parts) == 2

        return f"{parts[0][0].upper()}{parts[1][:3].upper()}"

    data['aliases'] = data['species'].apply(extract_aliases)

    return data['aliases'].unique()


def fetch_cluster_names():
    data = get_data()
    # Read and analyze mmseqs results
    df_mmseqs = pd.read_csv("clstrs_mmseqs_cluster.tsv", sep="\t", names=["Cluster", "Member"])

    # Count the number of occurrences for each cluster
    cluster_counts = df_mmseqs['Cluster'].value_counts()

    # Function to check if members in a cluster are from different genomes
    def members_from_different_genomes(group):
        aliases = group['Member'].str.split('_').str[0]
        return aliases.nunique() == len(group)

    # Minimal size of cluster to be considered
    min_size = 3

    # Create a DataFrame to store selected clusters and members
    df_sel = pd.DataFrame(columns=['Cluster', 'Member'])

    # Iterate through unique cluster sizes
    for cluster_size in range(min_size, len(data) + 2):
        # It only makes sense to check up to nr of genomes + 2 (to verify)
        # Check if clusters of the current size exist

        # Filter clusters based on the current size
        clusters_of_size_n = cluster_counts[cluster_counts == cluster_size].index

        # Filter the DataFrame to keep only rows with clusters of the current size
        df_of_size_n = df_mmseqs[df_mmseqs['Cluster'].isin(clusters_of_size_n)]

        # Check if the DataFrame is non-empty before further processing
        if not df_of_size_n.empty:
            # Apply the unique genome filtering function to each group in the DataFrame
            filtered_clusters = df_of_size_n.groupby('Cluster').filter(members_from_different_genomes)

            # Append selected clusters and members to df_sel
            df_sel = pd.concat([df_sel, filtered_clusters[['Cluster', 'Member']]], ignore_index=True)
            
    # print(results)

    cluster_names = list(df_sel["Cluster"].unique())

    return cluster_names


def extract_species(raw_species):
    parts = raw_species.split()
    if len(parts) >= 2:
        return ' '.join(parts[:2])
    else:
        return raw_species

def extract_aliases(species):
    parts = species.split()
    assert len(parts) == 2

    return f"{parts[0][0].upper()}{parts[1][:3].upper()}"
