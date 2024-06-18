import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


matplotlib.use('Agg')


def load_data(file_path):
    """Load data from a TSV file into a DataFrame."""
    return pd.read_csv(file_path, sep='\t')


def create_scatterplot(data, x_col, y_col, hue_col, style_col, size_col, output_file):
    """Create a scatterplot from the data and save it to a file."""
    # Calculate statistics for Genome size
    calculate_statistics(data, 'Genome size')

    data[x_col] = np.log10(data[x_col])  # Log10 transformation
    sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col, style=style_col, size=size_col)
    plt.xlabel('log10(Genome size)')  # Set x-axis label
    plt.savefig(output_file, dpi=300)
    plt.close()


def calculate_statistics(data, col):
    """Calculate main statistics of values in the given column and save them to a text file."""
    statistics = data[col].describe()
    with open(f'checkm_results_all_edited_statistics_{col.replace(" ", "_").lower()}.txt', 'w') as file:
        file.write(statistics.to_string())


def main():
    # Input file path
    input_file = "checkm_results_all_edited.tsv"
    # Output file path
    output_file = "figures/checkm_scatterplot_season.png"

    # Load data
    data = load_data(input_file)

    # Define columns for scatterplot
    x_col = 'Genome size'
    y_col = 'Completeness'
    hue_col = 'country'
    style_col = 'season'
    size_col = 'gut_part'  # Size based on 'gut_part' column

    # Create scatterplot
    create_scatterplot(data, x_col, y_col, hue_col, style_col, size_col, output_file)

    output_file = "figures/checkm_scatterplot_season_without_gut_parts.png"
    create_scatterplot_without_gut_parts(data, x_col, y_col, hue_col, style_col, output_file)


def create_scatterplot_without_gut_parts(data, x_col, y_col, hue_col, style_col, output_file):
    """Create a scatterplot from the data and save it to a file."""
    # Calculate statistics for Genome size
    calculate_statistics(data, 'Genome size')
    calculate_statistics(data, 'Completeness')
    calculate_statistics(data, 'Contamination')

    # data[x_col] = np.log10(data[x_col])  # Log10 transformation
    sns.scatterplot(data=data, x=x_col, y=y_col, hue=hue_col, style=style_col)
    plt.xlabel('log10(Genome size)')  # Set x-axis label
    plt.savefig(output_file, dpi=300)
    plt.close()


if __name__ == "__main__":
    main()
