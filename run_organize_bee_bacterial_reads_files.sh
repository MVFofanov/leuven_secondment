#!/bin/bash

#SBATCH --job-name=organize_bee_bacterial_reads_files

#SBATCH --time=03:00:00 # days-hh:mm:ss
#SBATCH --partition=short
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2GB # 4GB

#SBATCH --mail-user=mikhail.v.fofanov@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --output=result_%x.%j.txt

date;hostname;pwd

source /home/zo49sog/miniconda3/etc/profile.d/conda.sh

working_dir="/home/zo49sog/crassvirales/leuven_secondment"

cd "${working_dir}"

# Define the directory containing the files
input_dir="read/"

# Loop through each file in the directory
for file in "$input_dir"/*; do
    # Extract the sample name from the file name
    sample=$(basename "$file" | cut -d '_' -f 1-5)

    # Replace '.R1' with '_R1' and '.R2' with '_R2' in the sample name
    sample=${sample//.R1/_R1}
    sample=${sample//.R2/_R2}

    # Create a subfolder for the sample if it doesn't exist
    mkdir -p "$input_dir/$sample"

    # Move the file to the subfolder
    mv "$file" "$input_dir/$sample"
done

conda deactivate

date

