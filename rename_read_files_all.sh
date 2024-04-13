#!/bin/bash

# Define the directory path
base_directory="read/"

# Iterate over each subdirectory in the base directory
for directory in "$base_directory"*/; do
    # Iterate over each file in the subdirectory
    for file in "$directory"*; do
        # Check if the file exists and is a regular file
        if [ -f "$file" ]; then
            # Get the file name without the path
            filename=$(basename -- "$file")
            
            # Replace '.R1' with '_R1' and '.R2' with '_R2'
            new_filename="${filename//.R1/_R1}"
            new_filename="${new_filename//.R2/_R2}"
            
            # Rename the file
            mv "$file" "$directory$new_filename"
            
            # Print the old and new file names
            echo "Renamed: $filename -> $new_filename"
        fi
    done
done
