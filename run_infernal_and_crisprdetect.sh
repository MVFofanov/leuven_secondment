#!/bin/bash

#SBATCH --job-name=padloc

#SBATCH --time=3-00:00:00 # days-hh:mm:ss
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=40
#SBATCH --mem-per-cpu=1GB # 4GB

#SBATCH --mail-user=mikhail.v.fofanov@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --output=result_bac_genomes_padloc.%j.txt

date;hostname;pwd

source /home/zo49sog/miniconda3/etc/profile.d/conda.sh

conda activate

conda activate /home/zo49sog/mambaforge/envs/padloc

cd /home/zo49sog/crassvirales/leuven_secondment

# Set the directory containing *.fna files
input_directory="bac_genomes/"

infernal_dir="bac_genomes/padloc_results/infernal"
crisprdetect_dir="bac_genomes/padloc_results/crisprdetect"

# Create output directories if they don't exist
mkdir -p ${infernal_dir}
mkdir -p ${crisprdetect_dir}

# Iterate over all *.fna files in the input directory
for file_path in ${input_directory}*.fna; do
    # Extract file name without extension
    file_name=$(basename "${file_path%.fna}")

    # Step 1: run-infernal
    run-infernal --input "${file_path}" --output "${infernal_dir}/${file_name}_ncrna.tblout"

    # Step 2: run-crisprdetect
    run-crisprdetect --input "${file_path}" --output "${crisprdetect_dir}/${file_name}_crispr"

    # Step 3: padloc
    padloc --fna "${file_path}" --ncrna "${infernal_dir}/${file_name}_ncrna.tblout.formatted" \
	   --crispr "${crisprdetect_dir}/${file_name}_crispr.gff" --cpu 40 \
	   --outdir "bac_genomes/padloc_results/padloc"
done

conda deactivate
conda deactivate

date

