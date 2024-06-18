import pandas as pd
import glob
import os


def extract_sample_name(filename):
    """
    Extracts the sample name from the given filename.

    Parameters:
    filename (str): The filename to extract the sample name from.

    Returns:
    str: The extracted sample name.
    """
    # Extract the part of the filename before '.fa_padloc.csv'
    base = os.path.basename(filename)
    sample_name = base.replace('.fa_padloc.csv', '')
    return sample_name


def combine_csv_files(directory):
    """
    Combines all .csv files in the given directory into a single DataFrame
    with an additional 'sample_name' column.

    Parameters:
    directory (str): The directory containing the .csv files.

    Returns:
    DataFrame: The combined DataFrame with the 'sample_name' column.
    """
    # Find all .csv files in the directory
    all_files = glob.glob(os.path.join(directory, "*.csv"))

    # Print the files found
    print(f"Found {len(all_files)} CSV files.")

    # List to hold each DataFrame
    df_list = []

    for file in all_files:
        # Extract sample name from filename
        sample_name = extract_sample_name(file)

        print(f"Processing file: {file} with sample name: {sample_name}")

        # Read the CSV file into a DataFrame
        try:
            df = pd.read_csv(file)

            # Add the sample_name column
            df['sample_name'] = sample_name

            # Reorder columns to make 'sample_name' the first column
            cols = ['sample_name'] + [col for col in df.columns if col != 'sample_name']
            df = df[cols]

            # Append the DataFrame to the list
            df_list.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not df_list:
        print("No dataframes were created. Check if the files are in correct format and not empty.")
    else:
        # Combine all DataFrames into a single DataFrame
        combined_df = pd.concat(df_list, ignore_index=True)
        return combined_df


if __name__ == '__main__':
    # Usage example
    directory = 'hive_analysis/padloc/padloc/'
    combined_df = combine_csv_files(directory)

    if combined_df is not None:
        # Save the combined DataFrame to a new CSV file
        output_file = 'hive_analysis/padloc/all_padloc.csv'
        combined_df.to_csv(output_file, index=False)
        print(f"Combined CSV saved to {output_file}")
    else:
        print("No CSV files were combined.")

