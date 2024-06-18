import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use('Agg')


def plot_scaffold_length_comparison(hive_lengths, hive_lengths_log10,
                                    sample_lengths, sample_lengths_log10,
                                    scaffold_length_plot, dpi=300):
    """
    This function takes two files containing scaffold lengths, performs a log10 transformation
    on these lengths, and creates a plot to compare the distributions. The plot is saved to
    the specified output path with the given DPI.

    Parameters:
    hive_lengths (str): Path to the first file containing hive scaffold lengths.
    file2 (str): Path to the second file containing scaffold lengths.
    output_path (str): Path to save the output plot.
    dpi (int): DPI for the output plot. Default is 300.
    """
    # Load the scaffold lengths from the text files
    hive_scaffolds = pd.read_csv(hive_lengths, header=None, names=['length'])
    sample_scaffolds = pd.read_csv(sample_lengths, header=None, names=['length'])

    # Apply log10 transformation
    hive_scaffolds['log10_length'] = round(np.log10(hive_scaffolds['length']), 2)

    # hive_scaffolds['log10_length'] = round(np.log10(hive_scaffolds['length']), 2)
    # hive_log10_length_counts = hive_scaffolds['log10_length'].value_counts().reset_index()
    # hive_log10_length_counts.columns = ['log10_length', 'frequency']
    # hive_log10_length_counts['source'] = 'Hive'
    # hive_log10_length_counts.to_csv(hive_lengths_log10, sep='\t', index=False)
    #
    sample_scaffolds['log10_length'] = round(np.log10(sample_scaffolds['length']), 2)
    # sample_log10_length_counts = sample_scaffolds['log10_length'].value_counts().reset_index()
    # sample_log10_length_counts.columns = ['log10_length', 'frequency']
    # sample_log10_length_counts['source'] = 'Sample'
    # sample_log10_length_counts.to_csv(sample_lengths_log10, sep='\t', index=False)

    # Create a combined dataframe for plotting
    hive_scaffolds['source'] = 'Hive'
    sample_scaffolds['source'] = 'Sample'

    combined_data = pd.concat([hive_scaffolds, sample_scaffolds])

    #combined_data = pd.concat([hive_log10_length_counts, sample_log10_length_counts])

    # Create the plot
    plt.figure(figsize=(10, 6))
    #sns.histplot(data=combined_data, x='log10_length', y='frequency', bins=100, kde=True, color='skyblue')
    sns.histplot(data=combined_data, x='log10_length', hue='source', bins=100, kde=True, color='skyblue')
    #sns.histplot(data=combined_data, x='log10_length', y='frequency', hue='source', bins=100, kde=True, color='skyblue')
    # sns.histplot(data=combined_data, x='log10_length', hue='source', kde=True, element='step', stat='density',
    #              common_norm=False)
    plt.title('Log10 Transformed Scaffold Lengths Distribution')
    plt.xlabel('Scaffold Length (log10), bp')
    plt.ylabel('Number of scaffolds')

    # Define custom x-axis ticks and labels
    xticks = list(range(2, 7))  # Example tick positions
    xtick_labels = [f'10^{i}' for i in xticks]  # Corresponding tick labels

    plt.xticks(ticks=xticks, labels=xtick_labels)

    # # Create the legend
    # handles, labels = plt.gca().get_legend_handles_labels()
    # plt.legend(handles=handles, labels=labels, title='Source')
    #
    plt.tight_layout()

    # Save the plot
    plt.savefig(scaffold_length_plot, dpi=dpi)
    plt.close()

    print(f"Plot saved to {scaffold_length_plot}")


if __name__ == "__main__":
    # Usage example
    hive_lengths = '/mnt/c/crassvirales/leuven_secondment/hive_analysis/all_hive_scaffolds_lengths.txt'
    hive_lengths_log10 = '/mnt/c/crassvirales/leuven_secondment/hive_analysis/all_hive_scaffolds_lengths_log10.txt'

    sample_lengths = '/mnt/c/crassvirales/leuven_secondment/metaspades_scaffolds_lenghes_sorted.txt'
    sample_lengths_log10 = '/mnt/c/crassvirales/leuven_secondment/hive_analysis/all_sample_scaffolds_lengths_log10.txt'

    scaffold_length_plot = '/mnt/c/crassvirales/leuven_secondment/hive_analysis/figures/metaspades_scaffold_length_comparison.png'

    plot_scaffold_length_comparison(hive_lengths, hive_lengths_log10,
                                    sample_lengths, sample_lengths_log10,
                                    scaffold_length_plot)


