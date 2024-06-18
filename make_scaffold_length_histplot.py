import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


matplotlib.use('Agg')


def plot_log_histogram(file_path, log_transformed, output_plot):
    # Read data from file
    data = pd.read_csv(file_path, header=None, names=['Length'])

    # Transform values using log10
    data['Log_Length'] = np.log10(data['Length'])

    data.to_csv(log_transformed, sep='\t', index=False)

    # Create histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='Log_Length', bins=100, kde=True, color='skyblue')
    plt.title('Histogram of Scaffold Lengths (log10-transformed)')
    plt.xlabel('log10(Length)')
    plt.ylabel('Frequency')
    plt.grid(True)

    plt.savefig(output_plot, dpi=300)
    plt.close()


def plot_log_histogram_frequency_log10(file_path, log_transformed, output_plot):
    # Read data from file
    data = pd.read_csv(file_path, header=None, names=['Length'])

    # Transform values using log10 and round to two decimal places
    data['Log_Length'] = round(np.log10(data['Length']), 2)

    # Transform frequency values using log10
    data['Frequency'] = np.log10(data.groupby('Length').transform('count'))

    data.to_csv(log_transformed, sep='\t', index=False)

    # Create histogram
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x='Log_Length', y='Frequency', bins=100, kde=True, color='skyblue')
    plt.title('Histogram of Scaffold Lengths (log10-transformed)')
    plt.xlabel('log10(Length)')
    plt.ylabel('log10(Frequency)')
    plt.grid(True)

    plt.savefig(output_plot, dpi=300)
    plt.close()


if __name__ == "__main__":
    # Call the function with the file path
    file_path = "/mnt/c/crassvirales/leuven_secondment/metaspades_scaffolds_lenghes_sorted.txt"
    log_transformed = "/mnt/c/crassvirales/leuven_secondment/metaspades_scaffolds_lenghes_sorted_log10.txt"

    # output_plot = "/mnt/c/crassvirales/leuven_secondment/figures/scaffold_length_histplot_all.png"
    # plot_log_histogram(file_path, log_transformed, output_plot)

    output_plot = "/mnt/c/crassvirales/leuven_secondment/figures/scaffold_length_histplot_all_frequency_log10.png"

    plot_log_histogram_frequency_log10(file_path, log_transformed, output_plot)

