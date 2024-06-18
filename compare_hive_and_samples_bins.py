import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

matplotlib.use('Agg')


def load_data(file_path):
    """Load data from a TSV file into a DataFrame."""
    return pd.read_csv(file_path, sep='\t')


def create_directory_if_not_exists(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def compare_plots(table1, table2, columns, output_dir, is_filtered=False):
    """Create boxplots and histograms for specified columns from two tables."""
    if is_filtered:
        table_type = 'filtered'
    else:
        table_type = 'unfiltered'

    for col in columns:
        # Create figure with two subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Boxplot
        sns.boxplot(data=pd.concat([table1[col].rename('Hive bins'), table2[col].rename('Sample bins')], axis=1),
                    ax=axes[0])
        axes[0].set_title(f'Comparison of {col}_{table_type} between Hive bins and Sample bins')
        axes[0].set_ylabel(col)
        axes[0].tick_params(axis='x', rotation=45)

        # Histogram
        sns.histplot(table1[col], ax=axes[1], label='Hive bins', color='blue', kde=True)
        sns.histplot(table2[col], ax=axes[1], label='Sample bins', color='orange', kde=True)
        axes[1].set_title(f'Distribution of {col}_{table_type}')
        axes[1].set_xlabel(col)
        axes[1].set_ylabel('Frequency')
        axes[1].legend()

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f'comparison_plot_{col}_{table_type}.png'), dpi=300)
        plt.close()


def create_scatterplot(data1, data2, x_col, y_col, hue_col, output_file):
    """Create scatterplots for hive bins and sample bins separately."""
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    sns.scatterplot(data=data1, x=x_col, y=y_col, hue=hue_col)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'{x_col} vs {y_col} - Hive Bins')
    plt.legend(title=hue_col)

    plt.subplot(1, 2, 2)
    sns.scatterplot(data=data2, x=x_col, y=y_col, hue=hue_col)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f'{x_col} vs {y_col} - Sample Bins')
    plt.legend(title=hue_col)

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()


def main():
    # Define input file paths
    hive_table_file = "hive_analysis/checkm_results_all_hives_edited.tsv"
    sample_table_file = "checkm_results_all_edited.tsv"
    output_directory = "hive_analysis/figures"

    # Load data from both tables
    hive_table = load_data(hive_table_file)
    sample_table = load_data(sample_table_file)

    # Filter tables based on conditions
    hive_table_filtered = hive_table[(hive_table['Completeness'] >= 50) & (hive_table['Contamination'] <= 5)]
    sample_table_filtered = sample_table[(sample_table['Completeness'] >= 50) & (sample_table['Contamination'] <= 5)]

    # Save filtered tables to new TSV files
    hive_table_filtered.to_csv("hive_analysis/hive_table_filtered.tsv", sep='\t', index=False)
    sample_table_filtered.to_csv("hive_analysis/sample_table_filtered.tsv", sep='\t', index=False)

    # Log10 transformation for 'Genome size'
    hive_table['Genome size'] = np.log10(hive_table['Genome size'])
    sample_table['Genome size'] = np.log10(sample_table['Genome size'])

    # Define columns for comparison
    columns_to_compare = ['Genome size', 'Completeness', 'Contamination']

    # Create output directory if it doesn't exist
    create_directory_if_not_exists(output_directory)

    # Generate comparison plots
    compare_plots(hive_table, sample_table, columns_to_compare, output_directory)



    # Generate comparison plots for filtered tables
    compare_plots(hive_table_filtered, sample_table_filtered, columns_to_compare, output_directory, is_filtered=True)

    # Scatterplot comparisons for hive bins and sample bins
    create_scatterplot(hive_table_filtered, sample_table_filtered, 'Completeness', 'Contamination', 'country',
                       os.path.join(output_directory, 'scatterplot_completeness_vs_contamination.png'))
    create_scatterplot(hive_table_filtered, sample_table_filtered, 'Completeness', 'Genome size', 'country',
                       os.path.join(output_directory, 'scatterplot_completeness_vs_genome_size.png'))
    create_scatterplot(hive_table_filtered, sample_table_filtered, 'Genome size', 'Contamination', 'country',
                       os.path.join(output_directory, 'scatterplot_genome_size_vs_contamination.png'))


if __name__ == "__main__":
    main()
