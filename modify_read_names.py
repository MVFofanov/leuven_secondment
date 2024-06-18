import os
import gzip


def modify_read_names(input_file, output_file):
    basename = os.path.splitext(os.path.basename(input_file))[0]  # Extract basename of the file
    extension = os.path.splitext(input_file)[1]  # Extract extension of the file

    # Check if the file is compressed or not
    if extension == ".gz":
        with gzip.open(input_file, "rt") as f_in, gzip.open(output_file, "wt") as f_out:
            for line_num, line in enumerate(f_in, start=1):
                if line_num % 4 == 1:
                    f_out.write(f"@{basename}_{line.strip()}\n")
                else:
                    f_out.write(line)
    else:
        with open(input_file, "r") as f_in, gzip.open(output_file, "wt") as f_out:
            for line_num, line in enumerate(f_in, start=1):
                if line_num % 4 == 1:
                    f_out.write(f"@{basename}_{line.strip()}\n")
                else:
                    f_out.write(line)


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if "_R1.fastq" in filename:
                input_file_R1 = os.path.join(root, filename)
                output_file_R1 = os.path.join(root, filename.replace(".gz", "").replace("_R1.fastq", "_modified_R1.fastq.gz"))
                modify_read_names(input_file_R1, output_file_R1)

            elif "_R2.fastq" in filename:
                input_file_R2 = os.path.join(root, filename)
                output_file_R2 = os.path.join(root, filename.replace(".gz", "").replace("_R2.fastq", "_modified_R2.fastq.gz"))
                modify_read_names(input_file_R2, output_file_R2)

# Apply the function to the read/ directory
process_directory("read/")

# Example usage
#input_file = "/home/zo49sog/crassvirales/leuven_secondment/read/BE_16556_aut_ile/BE_16556_aut_ile_e.ExBee.ExHuman_R1.fastq"
#output_file = "/home/zo49sog/crassvirales/leuven_secondment/read/BE_16556_aut_ile/BE_16556_aut_ile_e.ExBee.ExHuman_modified_R1.fastq"
#modify_read_names(input_file, output_file)

#input_file = "library1_R2.fastq.gz"
#output_file = "library1_modified_R2.fastq.gz"
#modify_read_names(input_file, output_file)

# Repeat for uncompressed FASTQ files if needed
#input_file = "library2_R1.fastq"
#output_file = "library2_modified_R1.fastq"
#modify_read_names(input_file, output_file)

#input_file = "library2_R2.fastq"
#output_file = "library2_modified_R2.fastq"
#modify_read_names(input_file, output_file)

