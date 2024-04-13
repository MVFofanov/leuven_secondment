import pandas as pd
import os

# Read the table from samples.tsv into a DataFrame
df = pd.read_csv('atlas_results/samples.tsv', sep='\t')

# Extract the lowest directory name from the paths in the first column
df['Sample'] = df['Reads_raw_R1'].apply(lambda x: os.path.basename(os.path.dirname(x)))

df['Sample'] = df['Sample'].apply(lambda x: x.replace('_', ''))

# Extract part of the value from the second column for the fifth column
df['BinGroup'] = df['Reads_raw_R2'].apply(lambda x: '_'.join(os.path.basename(os.path.dirname(x)).split('_')[:2]))

# Set 'Full_Name' as index and remove the column
df.set_index('Sample', inplace=True)

# Remove the index name
df.index.name = None

# Remove the 'Unnamed: 0' column
df.drop(columns=['Unnamed: 0'], inplace=True, errors='ignore')

#del df['Sample']

# Save the modified DataFrame to samples_edited.tsv
#df.to_csv('atlas_results/samples_edited.tsv', sep='\t')
df.to_csv('atlas_results/samples_edited_without_underscores.tsv', sep='\t')

print("Output saved to samples_edited.tsv")
