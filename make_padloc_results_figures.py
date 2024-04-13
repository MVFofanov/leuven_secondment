import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


matplotlib.use('Agg')

# Read the data
padloc_results_file = 'bac_genomes/padloc_results/all_padloc_modified_uniq.tsv'

figures_dir = "bac_genomes/padloc_results/figures"

# Define colors for different genera
genus_colors = {
    'Bifidobacterium': '#4daf4a',
    'Lactobacillus': '#984ea3',
    'Bartonella': '#377eb8',
    'Bombilactobacillus': '#ff7f00',
    'Gilliamella': '#e41a1c',
    'Snodgrassella': '#ffff33'
}


def make_a_defence_system_histogram(padloc_results_file: str, genus_colors: dict,
                                    figures_dir: str):
    data = pd.read_csv(padloc_results_file, sep='\t')

    # Count occurrences of each 'system' value for each 'genus'
    counts = data.groupby(['genus', 'system']).size().reset_index(name='count')

    # Create stacked bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=counts, x='system', y='count', hue='genus', palette=genus_colors)

    plt.title('Stacked Bar Plot of Defence System by Genus')
    plt.xlabel('Defence System')
    plt.ylabel('Count')
    plt.legend(title='Genus', loc='upper right')

    # Save the plot as a JPG file
    plt.savefig(f"{figures_dir}/defence_system_barplot.jpg", dpi=600)

    plt.close()
#    plt.show()


def create_defence_systems_boxplot(input_file_path, output_file_path, genus_colors=None):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Create a boxplot
    plt.figure(figsize=(10, 6))
    # print(data['genus'].unique())
    sns.boxplot(data=data, x='genus', y='number_of_systems',
                palette=[genus_colors[genus] for genus in data['genus'].unique()] if genus_colors else 'Set1')

    # Set labels and title
    plt.xlabel('Genus')
    plt.ylabel('Number of Defence Systems per genome')
    plt.title('Boxplot of Defence Systems in isolated bacteria by Genus')

    # Save the plot
    plt.savefig(output_file_path)

    plt.close()


def create_stacked_barplot(input_file_path, output_file_path):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Sort the data by count in descending order
    data = data.sort_values(by='count', ascending=False)

    # Create a stacked barplot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=data, x='system', y='count', hue='genus', palette='Set1', edgecolor='k')

    # Set labels and title
    plt.xlabel('System Number')
    plt.ylabel('Count')
    plt.title('Stacked Barplot of Defence Systems by System Number')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)

    # Adjust legend position
    plt.legend(title='Genus', loc='upper right')

    # Save the plot
    plt.savefig(output_file_path)


# def create_grouped_barplot(input_file_path, output_file_path):
#     # Read the data
#     data = pd.read_csv(input_file_path, sep='\t')
#
#     # Pivot the data to have 'genus' as columns and 'count' as values
#     pivoted_data = data.pivot(index='system', columns='genus', values='count').fillna(0)
#
#     # Sort the columns by sum of counts in descending order
#     pivoted_data = pivoted_data[pivoted_data.sum().sort_values(ascending=False).index]
#
#     # Create a grouped bar plot
#     plt.figure(figsize=(10, 6))
#     pivoted_data.plot(kind='bar', stacked=True, edgecolor='k')
#
#     # Set labels and title
#     plt.xlabel('Defence System')
#     plt.ylabel('Count')
#     plt.title('Grouped Barplot of Defence Systems by Genus')
#
#     # Rotate x-axis labels for better readability
#     plt.xticks(rotation=45)
#
#     # Save the plot
#     plt.savefig(output_file_path)


def create_grouped_barplot(input_file_path, output_file_path, top_n=30):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Get the top 20 systems based on count
    top_systems = data.groupby('system')['count'].sum().nlargest(top_n).index

    # Filter the data for top systems
    data = data[data['system'].isin(top_systems)]

    # Sort the data by count in descending order
    data = data.sort_values(by='count', ascending=False)

    # Create a grouped bar plot
    plt.figure(figsize=(12, 8))
    sns.barplot(data=data, x='system', y='count', hue='genus', palette='Set1', edgecolor='k')

    # Set labels and title
    plt.xlabel('System')
    plt.ylabel('Count')
    plt.title('Grouped Barplot of Top 20 Defence Systems by Genus')

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Adjust legend position
    plt.legend(title='Genus', loc='upper right')

    # Save the plot
    plt.savefig(output_file_path, bbox_inches='tight')

    plt.close()


def create_stacked_barplot(input_file_path, output_file_path, top_n=30, genus_colors=None):
    # Read the data
    data = pd.read_csv(input_file_path, sep='\t')

    # Calculate cumulative sum of counts for each system
    data['cumulative_count'] = data.groupby('system')['count'].cumsum()

    # Get the top 20 systems based on cumulative sum of counts
    top_systems = data.groupby('system')['cumulative_count'].max().nlargest(top_n).index

    # Filter the data for top systems
    data = data[data['system'].isin(top_systems)]

    # Sort the data by cumulative count in descending order
    data = data.sort_values(by=['system', 'cumulative_count'], ascending=False)

    # Pivot the data to have 'genus' as columns and 'count' as values
    pivoted_data = data.pivot_table(index='system', columns='genus', values='count', fill_value=0)

    # Calculate the cumulative counts for each system
    cumulative_counts = pivoted_data.sum(axis=1)

    # Sort the systems based on cumulative counts in descending order
    sorted_systems = cumulative_counts.sort_values(ascending=False).index

    # Reorder the rows in pivoted_data based on sorted systems
    pivoted_data = pivoted_data.loc[sorted_systems]

    # Plotting
    plt.figure(figsize=(16, 10))  # Increase figure size
    pivoted_data.plot(kind='bar', stacked=True, edgecolor='k',
                      color=[genus_colors[col] for col in pivoted_data.columns] if genus_colors else None)

    # Set labels and title with larger font size
    plt.xlabel('System', fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.title('Sorted Stacked Barplot of Top 30 Defence Systems by Genus', fontsize=16)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=8)

    # Adjust legend position with larger font size
    plt.legend(title='Genus', loc='upper right', fontsize=12)

    # Save the plot with higher quality
    plt.savefig(output_file_path, bbox_inches='tight', dpi=300)

    plt.close()


if __name__ == "__main__":
    # make_a_defence_system_histogram(padloc_results_file, genus_colors, figures_dir)
    #
    input_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems_per_genome.tsv'
    output_file_path = 'bac_genomes/padloc_results/figures/defence_systems_boxplot.png'
    #
    create_defence_systems_boxplot(input_file_path, output_file_path, genus_colors=genus_colors)

    # input_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems.tsv'
    # output_file_path = 'bac_genomes/padloc_results/figures/defence_systems_stacked_barplot.png'
    #
    # create_stacked_barplot(input_file_path, output_file_path)

    input_file_path = 'bac_genomes/padloc_results/all_padloc_modified_uniq_defence_systems_per_genus.tsv'
    output_file_path = 'bac_genomes/padloc_results/figures/defence_systems_grouped_barplot_top_20.png'
    #
    create_grouped_barplot(input_file_path, output_file_path)

    output_file_path = 'bac_genomes/padloc_results/figures/defence_systems_stacked_barplot_top_20.png'

    create_stacked_barplot(input_file_path, output_file_path, genus_colors=genus_colors)

