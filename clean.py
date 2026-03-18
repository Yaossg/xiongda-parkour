import os

def clean_output_directory():
    output_dir = "out"
    if not os.path.exists(output_dir):
        print(f"{output_dir} does not exist. No files to clean.")
        return
    
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

if __name__ == "__main__":
    clean_output_directory()