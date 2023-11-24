import os


def check_file(file_path):
    try:
        with open(file_path, "r") as file:
            print(f"File opened successfully: {file_path}", end="\n")
    except FileNotFoundError:
        print(f"File not found: {file_path}", end="\n")
    except Exception as e:
        print(f"Error detected: {str(e)}", end="\n")


def check_output_image(path_image):
    if os.path.exists(path_image):
        try:
            os.remove(path_image)
            print(f"File updated successfully: {path_image}", end="\n")
        except Exception as e:
            print(f"Error deleting file: {str(e)}", end="\n")
    else:
        print(f"File not found: {path_image}", end="\n")
        print(f"File created successfully: {path_image}", end="\n")
