import csv

import pandas as pd


def make_a_taxonomy_dict(taxonomy_file: str) -> dict:
    with open(taxonomy_file, "r", encoding="utf8") as f_in:
        taxonomy = {}
        reader = csv.reader(f_in, delimiter='\t')

        for row in reader:
            taxonomy[row[0]] = {"species": row[1],
                                "genus": row[1].split()[0]}

        #print(taxonomy)
        return taxonomy


def modify_padloc_output(input_file: str, output_file: str, taxonomy: dict):
    with open(input_file, "r", encoding="utf8") as f_in, open(output_file, "w", encoding="utf8", newline='') as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out, delimiter='\t')

        header = next(reader)
        writer.writerow(["genome", "genus", "species"] + header)

        for row in reader:
            system_number = row[0]
            seqid = row[1]
            genome, _ = row[1].split("_", 1)

            genus = taxonomy[genome]["genus"]
            species = taxonomy[genome]["species"]
            writer.writerow([genome, genus, species, system_number, seqid] + row[2:])


def save_uniq_defence_system_for_all_genomes(padloc_uniq_file, output_file):
    # Read the data
    file_path = padloc_uniq_file
    data = pd.read_csv(file_path, sep='\t')

    # Group by genome, system, genus, and species, and count occurrences
    counts = data.groupby(['genome', 'system', 'system.number', 'genus', 'species']).size().reset_index(name='count')

    # Save the counts to a new file
    counts.to_csv(output_file, sep='\t', index=False)


def calculate_defence_systems_per_genome(input_file_path, output_file_path):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Group by genome, genus, and species, and calculate the sum of counts
    grouped_data = data.groupby(['genome', 'genus', 'species']).agg(
        number_of_systems=('count', 'sum'),
        defence_systems=('system', lambda x: ', '.join(sorted(x))),
        defence_systems_unique=('system', lambda x: ', '.join(sorted(set(x))))
    ).reset_index()

    # Save the grouped data to a new file
    grouped_data.to_csv(output_file_path, sep='\t', index=False)


def calculate_defence_systems_per_species(input_file_path, output_file_path):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Group by genome, genus, and species, and calculate the sum of counts
    grouped_data = data.groupby(['system', 'genus', 'species']).agg(
        count=('count', 'sum'),
        genomes=('genome', lambda x: ', '.join(sorted(set(x))))
    ).reset_index()

    # Save the grouped data to a new file
    grouped_data.to_csv(output_file_path, sep='\t', index=False)


def calculate_defence_systems_per_genus(input_file_path, output_file_path):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Group by genome, genus, and species, and calculate the sum of counts
    grouped_data = data.groupby(['system', 'genus']).agg(
        count=('count', 'sum'),
        species=('species', lambda x: ', '.join(sorted(set(x)))),
        genomes=('genome', lambda x: ', '.join(sorted(set(x))))
    ).reset_index()

    # Save the grouped data to a new file
    grouped_data.to_csv(output_file_path, sep='\t', index=False)


if __name__ == "__main__":
    taxonomy_file = "bac_genomes/list_of_R_numbers_Feb2024_modified.tsv"

    # taxonomy = make_a_taxonomy_dict(taxonomy_file)

    input_file = "bac_genomes/padloc_results/all_padloc.csv"
    output_file = "bac_genomes/padloc_results/all_padloc_modified.tsv"

    # modify_padloc_output(input_file, output_file, taxonomy)

    padloc_uniq = 'bac_genomes/padloc_results/all_padloc_modified_uniq.tsv'
    padloc_uniq_defence_systems_file = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems.tsv'

    # save_uniq_defence_system_for_all_genomes(padloc_uniq, padloc_uniq_defence_systems_file)

    input_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems.tsv'
    output_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems_per_genome.tsv'

    # calculate_defence_systems_per_genome(input_file_path, output_file_path)

    input_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems.tsv'
    output_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems_per_species.tsv'

    calculate_defence_systems_per_species(input_file_path, output_file_path)

    output_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems_per_genus.tsv'

    calculate_defence_systems_per_genus(input_file_path, output_file_path)

