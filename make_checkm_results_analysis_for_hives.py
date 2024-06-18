import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import seaborn as sns

matplotlib.use('Agg')


def load_data(file_path):
    """Load data from a TSV file into a DataFrame."""
    return pd.read_csv(file_path, sep='\t')


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def create_scatterplot(data, x_col, y_col, hue_col, output_file):
    """Create a scatterplot from the data and save it to a file."""
    create_directory_if_not_exists(os.path.dirname(output_file))
    sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col)
    plt.savefig(output_file, dpi=300)
    plt.close()


def calculate_statistics(data, col, output_dir):
    """Calculate main statistics of values in the given column and save them to a text file."""
    create_directory_if_not_exists(output_dir)
    statistics = data[col].describe()
    with open(os.path.join(output_dir, f'checkm_results_{col.lower()}_statistics.txt'), 'w') as file:
        file.write(statistics.to_string())


def main():
    # Define input and output file paths
    input_file = "hive_analysis/checkm_results_all_hives_edited.tsv"
    figures_directory = "hive_analysis/figures"
    statistics_directory = "hive_analysis/statistics"

    # Load data
    data = load_data(input_file)

    # Calculate statistics for relevant columns
    for col in ['Genome size', 'Completeness', 'Contamination']:
        calculate_statistics(data, col, statistics_directory)

    # Define columns for scatterplot
    x_col = 'Genome size'
    y_col = 'Completeness'
    hue_col = 'country'

    # Log10 transformation
    data[x_col] = np.log10(data[x_col])

    # Create scatterplots
    create_scatterplot(data, x_col, y_col, hue_col,
                       os.path.join(figures_directory, 'checkm_scatterplot_genome_size_vs_completeness.png'))
    create_scatterplot(data, 'Contamination', y_col, hue_col,
                       os.path.join(figures_directory, 'checkm_scatterplot_contamination_vs_completeness.png'))
    create_scatterplot(data, x_col, 'Contamination', hue_col,
                       os.path.join(figures_directory, 'checkm_scatterplot_genome_size_vs_contamination.png'))


if __name__ == "__main__":
    main()
