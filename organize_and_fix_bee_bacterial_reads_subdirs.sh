#!/bin/bash

date
hostname
pwd

source /home/zo49sog/miniconda3/etc/profile.d/conda.sh

working_dir="/home/zo49sog/crassvirales/leuven_secondment"

cd "${working_dir}"

# Define the directory containing the files
input_dir="read"

# Define a function to recursively move files to the first subdirectory
move_files_recursive() {
    local dir="$1"
    local first_subdir=$(basename "$dir")

    # Move files to the first subdirectory
    for file in "$dir"/*; do
        if [[ -f "$file" ]]; then
            local filename=$(basename "$file")
            mv "$file" "$dir/../$first_subdir/$filename"
        elif [[ -d "$file" && "$file" != "$dir" ]]; then
            move_files_recursive "$file"
        fi
    done

    # Remove empty subdirectory
    if [[ -z $(ls -A "$dir") ]]; then
        rmdir "$dir"
    fi
}

# Call the function to start recursively moving files
for subdir in "$input_dir"/*/; do
    move_files_recursive "${subdir%/}"  # Remove trailing slash from directory path
done

conda deactivate

date

