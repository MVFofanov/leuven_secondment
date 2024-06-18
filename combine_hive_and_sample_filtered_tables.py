import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')


def combine_and_modify_tables(hive_table_path, sample_table_path, output_path):
    # Load the first table
    hive_table = pd.read_csv(hive_table_path, sep='\t')
    # Modify the 'sample_name' column
    hive_table['sample_name'] = hive_table['sample_name'] + '_' + hive_table['bin_number']
    hive_table['binning'] = 'hive'

    # Load the second table
    sample_table = pd.read_csv(sample_table_path, sep='\t')
    # Modify the 'sample_name' column
    sample_table['sample_name'] = sample_table['sample_name'] + '_' + sample_table['bin_number']
    sample_table['binning'] = 'sample'

    # Concatenate the two tables
    combined_table = pd.concat([hive_table, sample_table])

    # Save the combined table with a single header line
    combined_table.to_csv(output_path, sep='\t', index=False)


def add_taxonomy_columns(df):
    taxonomic_ranks = ['d__', 'p__', 'c__', 'o__', 'f__', 'g__', 's__']
    new_columns = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']

    # Function to split the taxonomy string into its components
    def split_taxonomy(taxonomy):
        parts = taxonomy.split(';')
        tax_dict = {rank: 'Unclassified' for rank in new_columns}
        for part in parts:
            for rank, new_col in zip(taxonomic_ranks, new_columns):
                if part.startswith(rank):
                    tax_dict[new_col] = part
                    break
        # Fill the remaining columns with the highest known taxonomic rank
        last_known = 'Unclassified'
        for col in new_columns:
            if tax_dict[col] != 'Unclassified':
                last_known = tax_dict[col]
            else:
                tax_dict[col] = last_known
        return pd.Series(tax_dict)

    taxonomy_df = df['classification'].apply(split_taxonomy)

    # Define the list of specific genera
    specific_genera = {
        'g__Lactobacillus', 'g__Snodgrassella', 'g__Bombilactobacillus',
        'g__Commensalibacter', 'g__Bartonella', 'g__Gilliamella',
        'g__Frischella', 'g__Bifidobacterium'
    }

    # Add 'genus_modified' column based on conditions
    taxonomy_df['genus_modified'] = taxonomy_df['genus'].apply(
        lambda g: g if g in specific_genera else 'other'
    )

    return pd.concat([df, taxonomy_df], axis=1)


def combine_tables_on_sample_name(hive_table_path, gtdbtk_table_path, output_path):
    # Load the first table
    hive_table = pd.read_csv(hive_table_path, sep='\t')
    # Debug: Print columns of the hive table
    #print("Hive Table Columns:", hive_table.columns)

    # Load the second table
    gtdbtk_table = pd.read_csv(gtdbtk_table_path, sep='\t')
    # Debug: Print columns of the GTDB-Tk table
    #print("GTDB-Tk Table Columns:", gtdbtk_table.columns)

    # Strip any leading/trailing whitespace from column names
    hive_table.columns = hive_table.columns.str.strip()
    gtdbtk_table.columns = gtdbtk_table.columns.str.strip()

    # Check columns after stripping whitespace
    #print("Hive Table Columns (Stripped):", hive_table.columns)
    #print("GTDB-Tk Table Columns (Stripped):", gtdbtk_table.columns)

    # Merge the two tables on 'sample_name' and 'user_genome'
    combined_table = pd.merge(hive_table, gtdbtk_table, left_on='sample_name', right_on='user_genome', how='inner')

    # Add taxonomy columns
    combined_table = add_taxonomy_columns(combined_table)

    # Save the combined table to a new TSV file
    combined_table.to_csv(output_path, sep='\t', index=False)


def plot_completeness_vs_contamination(input_path, output_path):
    # Load the combined table
    df = pd.read_csv(input_path, sep='\t')

    # Filter rows where 'binning' column is 'hive'
    hive_df = df[df['binning'] == 'hive']

    # Sort the DataFrame alphabetically based on the 'genus_modified' column
    hive_df_sorted = hive_df.sort_values(by='genus_modified', key=lambda x: x.str.extract(r'(?<=g__)(\w+)', expand=False) if x.name == 'genus_modified' else x)

    # Create a color palette with enough distinct colors
    unique_genera = hive_df_sorted['genus_modified'].unique()
    unique_genera_sorted = sorted(unique_genera)  # Sort genera alphabetically
    n_colors = len(unique_genera_sorted)
    palette = sns.color_palette("tab10", n_colors - 1) if n_colors <= 10 else sns.color_palette("tab10", n_colors - 1)  # Use default palette if more than 10 colors

    # Create the palette dictionary
    palette_dict = {genus: color for genus, color in zip(unique_genera_sorted, palette)}
    palette_dict['other'] = 'black'

    # Create a shape palette with different shapes for each country
    shapes = ['o', 's', '^', 'D', 'v', 'p', 'X', '<', '>']  # Define different shapes
    unique_countries = hive_df_sorted['country'].unique()
    n_shapes = len(unique_countries)
    shape_palette = {country: shape for country, shape in zip(unique_countries, shapes[:n_shapes])}

    # Create the scatter plot
    plt.figure(figsize=(10, 8))
    scatter_plot = sns.scatterplot(data=hive_df_sorted, x='Completeness', y='Contamination', hue='genus_modified',
                                   palette=palette_dict,
                                   style='country', markers=shape_palette)

    # Set the legend title
    # scatter_plot.legend_.set_title('Genus')

    # Set plot title and labels
    plt.title('Completeness vs Contamination')
    plt.xlabel('Completeness')
    plt.ylabel('Contamination')

    # Save the plot to a file
    plt.savefig(output_path, dpi=600)
    plt.close()


def plot_genus_histogram(input_path, output_path):
    # Load the combined table
    df = pd.read_csv(input_path, sep='\t')

    # Filter rows where 'binning' column is 'hive'
    hive_df = df[df['binning'] == 'hive']

    # Create a sorted count DataFrame
    genus_counts = hive_df['genus'].value_counts().reset_index()
    genus_counts.columns = ['genus', 'count']
    genus_counts = genus_counts.sort_values(by='count', ascending=False)

    # Merge the sorted counts back into the filtered DataFrame
    hive_df = hive_df.merge(genus_counts, on='genus')

    # Create a color palette with enough distinct colors
    families = hive_df['family'].unique()
    palette = sns.color_palette("husl", len(families))
    palette_dict = {family: color for family, color in zip(families, palette)}

    # Set up the figure and axis
    plt.figure(figsize=(12, 8))

    # Create the bar plot
    barplot = sns.barplot(data=hive_df, y='count', x='genus', hue='family', palette=palette_dict, dodge=False,
                          order=genus_counts['genus'])

    # Rotate x-axis tick labels by 90 degrees
    plt.xticks(rotation=90)

    # Set plot title and labels
    plt.title('Histogram of Genus members in Hive MAGs')
    plt.xlabel('Genus')
    plt.ylabel('Frequency')

    # Adjust legend
    handles, labels = barplot.get_legend_handles_labels()
    sorted_handles_labels = sorted(zip(handles, labels), key=lambda x: x[1])
    sorted_handles, sorted_labels = zip(*sorted_handles_labels)
    plt.legend(sorted_handles, sorted_labels, title='Family', bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    # Save the plot to a file
    plt.savefig(output_path, dpi=600, bbox_inches='tight')
    plt.close()


if __name__ == '__main__':
    # Example usage:
    hive_table_path = 'hive_analysis/hive_table_filtered.tsv'
    sample_table_path = 'hive_analysis/sample_table_filtered.tsv'
    hive_and_sample_table = 'hive_analysis/all_table_filtered.tsv'

    # Uncomment to combine and modify tables
    # combine_and_modify_tables(hive_table_path, sample_table_path, hive_and_sample_table)

    # Example usage:
    gtdbtk_table_path = 'hive_analysis/filtered_bins_gtdbtk/gtdbtk.bac120.summary.tsv'
    all_table_and_gtdbtk = 'hive_analysis/all_table_filtered_and_gtdbtk.tsv'

    #combine_tables_on_sample_name(hive_and_sample_table, gtdbtk_table_path, all_table_and_gtdbtk)

    # Define the input and output file paths
    hive_bins_completeness_vs_contamination_plot = 'hive_analysis/figures/' \
                                                   'hive_bins_scatterplot_completeness_vs_contamination.png'

    # Create the scatter plot
    # plot_completeness_vs_contamination(all_table_and_gtdbtk, hive_bins_completeness_vs_contamination_plot)

    output_path = 'hive_analysis/figures/hive_bins_histplot_taxonomy.png'
    plot_genus_histogram(all_table_and_gtdbtk, output_path)
