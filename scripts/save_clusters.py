

import os
import pandas as pd
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

def main():
    # 1.
    # Read and analyze mmseqs results
    df_mmseqs = pd.read_csv("clstrs_mmseqs_cluster.tsv", sep="\t", names=["Cluster", "Member"])

    # Select clusters having more than one element (filter out singletons)
    # Redundant code (all is done in the following cell)
    cluster_counts = df_mmseqs['Cluster'].value_counts()
    # Minimum size of clusters
    min_size = 1
    non_singleton_clusters = cluster_counts[cluster_counts > min_size].index
    df_sel = df_mmseqs[df_mmseqs['Cluster'].isin(non_singleton_clusters)]


    # 2.
    # Exclusion of Singletons, Duplets, and Non-Orthologous Clusters
    # Count the number of occurrences for each cluster
    cluster_counts = df_mmseqs['Cluster'].value_counts()

    # Function to check if members in a cluster are from different genomes
    def members_from_different_genomes(group):
        aliases = group['Member'].str.split('_').str[0]
        return aliases.nunique() == len(group)

    # Create a DataFrame to store the results - statistics for clusters
    results = pd.DataFrame(columns=['Cluster Size', 'Percentage', 'Clusters with Unique Genomes'])

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

            # Count the number of clusters that meet the criteria
            num_clusters_with_unique_genomes = len(filtered_clusters['Cluster'].unique())

            # Calculate the percentage for each cluster size
            percentage = (num_clusters_with_unique_genomes / len(clusters_of_size_n)) * 100

            # Append the results to the results DataFrame
            results = pd.concat([results, pd.DataFrame({'Cluster Size': [cluster_size], 'Percentage': [percentage], 'Clusters with Unique Genomes': [num_clusters_with_unique_genomes]})], ignore_index=True)

            # Append selected clusters and members to df_sel
            df_sel = pd.concat([df_sel, filtered_clusters[['Cluster', 'Member']]], ignore_index=True)
            
    # print(results)


    # 3.
    # Saving clusters to fasta
    # Whichever strategy is used
    # Cluster information is in a DataFrame df_sel
    # With columns "Cluster", "Member"

    # Create a DataFrame to store sequences from "sequences.fasta"
    df_seq = pd.DataFrame(columns=['id', 'Seq'])

    sequences_file_path = 'sequences.fasta'
    for record in SeqIO.parse(sequences_file_path, 'fasta'):
        sequence_id = record.id
        sequence = str(record.seq)
        df_seq = pd.concat([df_seq, pd.DataFrame({'id': [sequence_id], 'Seq': [sequence]})], ignore_index=True)

    # Merge df_sel and df_seq on columns 'id' and 'seq' to create df_cls
    df_cls = pd.merge(df_sel, df_seq, left_on='Member', right_on='id', how='left')
    df_cls.drop("id", inplace=True, axis=1)

    
    seq_folder = "sequences"
    os.makedirs(seq_folder, exist_ok=True)

    i = 0
    # Iterate through unique clusters in df_cls
    for cluster_id in df_cls['Cluster'].unique():
        # Filter df_cls for the current cluster
        cluster_df = df_cls[df_cls['Cluster'] == cluster_id]

        # Create a list of SeqRecords for the current cluster
        cluster_records = []
        for _, row in cluster_df.iterrows():
            record_id = row['Member']
            sequence = Seq(row['Seq'])
            cluster_records.append(SeqRecord(seq=sequence, id=record_id, description=''))

        # Write the SeqRecords to a fasta file named after the cluster
        output_file_path = os.path.join(seq_folder, f"{cluster_id}.fasta")
        SeqIO.write(cluster_records, output_file_path, 'fasta')

        i += 1

    print(f"{i} cluster sequences saved to {seq_folder}")