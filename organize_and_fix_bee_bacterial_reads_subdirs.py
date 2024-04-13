import os
import shutil

def move_files_to_first_directory(root_dir):
    for root, dirs, files in os.walk(root_dir):
        # Skip the first iteration since root is already the first subdirectory
        if root == root_dir:
            continue
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = os.path.join(root_dir, file)
            if os.path.exists(destination_path):
                # Append a number to the filename to make it unique
                base_name, extension = os.path.splitext(file)
                i = 1
                while os.path.exists(os.path.join(root_dir, f"{base_name}_{i}{extension}")):
                    i += 1
                destination_path = os.path.join(root_dir, f"{base_name}_{i}{extension}")
            shutil.move(source_path, destination_path)

def main():
    working_dir = '/home/zo49sog/crassvirales/leuven_secondment'
    input_dir = 'read'
    input_path = os.path.join(working_dir, input_dir)

    move_files_to_first_directory(input_path)

if __name__ == "__main__":
    print("Moving files to the first subdirectory...")
    main()
    print("Files moved successfully!")

