#!/bin/bash

#SBATCH --job-name=snakemake_pipeline
#SBATCH --time=12:00:00
#SBATCH --partition=interactive
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=10GB
#SBATCH --output=/home/zo49sog/crassvirales/leuven_secondment/hive_analysis/snakemake_pipeline/test/slurm_logs/result_%x.%j.log

# Load environment
source /home/zo49sog/mambaforge/etc/profile.d/conda.sh

working_dir="/home/zo49sog/crassvirales/leuven_secondment/hive_analysis/snakemake_pipeline"
# partition = "short"
partition="interactive"

# Run Snakemake
snakemake --snakefile "${working_dir}/Snakefile" --jobs 3 --cluster "sbatch --output={log_directory}/{rule}/%x_%j.out.txt --time=12:00:00 --partition=${partition} --nodes=1 --ntasks=1 --cpus-per-task={threads} --mem={resources.mem_mb}MB" --latency-wait 120
