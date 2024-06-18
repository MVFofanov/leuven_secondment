import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


matplotlib.use('Agg')


def process_defense_systems(input_file, output_file):
    # Read the input TSV file
    df = pd.read_csv(input_file, sep='\t')

    # Group by 'sample_name' and aggregate the necessary information
    aggregated_df = df.groupby('sample_name').agg(
        bin_number=('bin_number', 'first'),
        country=('country', 'first'),
        hive=('hive', 'first'),
        Completeness=('Completeness', 'first'),
        Contamination=('Contamination', 'first'),
        Genome_size=('Genome size', 'first'),
        domain=('domain', 'first'),
        phylum=('phylum', 'first'),
        class_=('class', 'first'),
        order=('order', 'first'),
        family=('family', 'first'),
        genus=('genus', 'first'),
        species=('species', 'first'),
        genus_modified=('genus_modified', 'first'),
        number_of_systems=('system', 'nunique'),
        defence_systems=('system', lambda x: ', '.join(x)),
        defence_systems_unique=('system', lambda x: ', '.join(sorted(set(x))))
    ).reset_index()

    # Rename columns to match desired output
    aggregated_df.rename(columns={'class_': 'class'}, inplace=True)

    # Save the result to a new TSV file
    aggregated_df.to_csv(output_file, sep='\t', index=False)

    # print(f"Processed table saved to {output_file}")


def create_defence_systems_boxplot(input_file_path, output_file_path):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Create a boxplot
    plt.figure(figsize=(12, 8))
    sns.boxplot(data=data, x='family', y='number_of_systems')

    # Set labels and title
    plt.xlabel('Family')
    plt.ylabel('Number of Defence Systems per Genome')
    plt.title('Boxplot of Defence Systems in hive MAGs by Family')

    # Rotate x-axis labels by 90 degrees
    plt.xticks(rotation=90)

    # Adjust layout to ensure everything fits without overlap
    plt.tight_layout()

    # Alternatively, you can manually adjust the bottom margin if needed
    # plt.subplots_adjust(bottom=0.25)

    # Save the plot
    plt.savefig(output_file_path, dpi=300)

    plt.close()


if __name__ == '__main__':
    # Usage example
    input_file = 'hive_analysis/padloc/all_padloc_and_taxonomy_uniq.tsv'
    defense_system_per_genome_file = 'hive_analysis/padloc/all_padloc_and_taxonomy_uniq_defense_system_per_genome.tsv'
    # process_defense_systems(input_file, defense_system_per_genome_file)

    defense_system_per_genome_boxplot = 'hive_analysis/figures/defense_system_per_genome_boxplot.png'

    create_defence_systems_boxplot(defense_system_per_genome_file, defense_system_per_genome_boxplot)

