#!/bin/bash

#SBATCH --job-name=modify_read_names

#SBATCH --time=3-00:00:00 # days-hh:mm:ss
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=10GB # 4GB

#SBATCH --mail-user=mikhail.v.fofanov@gmail.com
#SBATCH --mail-type=ALL

#SBATCH --output=result_%x.%j.txt

date;hostname;pwd

source /home/groups/VEO/tools/anaconda3/etc/profile.d/conda.sh

working_dir="/home/zo49sog/crassvirales/leuven_secondment/"

cd "${working_dir}"

#atlas init --db-dir atlas_databases "${input_directory}"

python3 modify_read_names.py

conda deactivate

date

