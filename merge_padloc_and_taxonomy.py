import pandas as pd


def merge_tables(file1, file2, output_file, key):
    """
    Merges two tables based on a common key column and saves the result to a new CSV file.

    Parameters:
    file1 (str): Path to the first CSV file.
    file2 (str): Path to the second CSV file.
    output_file (str): Path to save the merged CSV file.
    key (str): The key column to merge on.
    """
    # Read the tables
    table1 = pd.read_csv(file1)
    table2 = pd.read_csv(file2, sep='\t')  # Assuming the second file is tab-separated

    # Merge the tables on the specified key
    merged_table = pd.merge(table1, table2, on=key)

    # Save the merged table to a new CSV file
    merged_table.to_csv(output_file, index=False, sep='\t')

    print(f"Merged table saved to {output_file}")


if __name__ == "__main__":
    # Usage example
    file1 = 'hive_analysis/padloc/all_padloc.csv'
    file2 = 'hive_analysis/all_table_filtered_and_gtdbtk.tsv'
    output_file = 'hive_analysis/padloc/all_padloc_and_taxonomy.csv'
    key = 'sample_name'

    merge_tables(file1, file2, output_file, key)

