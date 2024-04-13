#!/bin/bash

#SBATCH --job-name=atlas_init

#SBATCH --time=3-00:00:00 # days-hh:mm:ss
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2GB # 4GB

#SBATCH --mail-user=mikhail.v.fofanov@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --output=result_%x.%j.txt

date;hostname;pwd

source /home/groups/VEO/tools/anaconda3/etc/profile.d/conda.sh && conda activate atlas_v2.0.6

working_dir="/home/zo49sog/crassvirales/leuven_secondment/atlas_results"

mkdir -p "${working_dir}"

cd "${working_dir}"

input_directory="../read/"

atlas init --db-dir atlas_databases "${input_directory}"

conda deactivate

date

