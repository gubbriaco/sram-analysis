import os


def check_file(buffer_raw_file_path):
    try:
        with open(buffer_raw_file_path, "r") as file:
            print(f"File opened successfully: {buffer_raw_file_path}", end="\n")
    except FileNotFoundError:
        print(f"File not found: {buffer_raw_file_path}", end="\n")
    except Exception as e:
        print(f"Error detected: {str(e)}", end="\n")


def check_output_image(buffer_simulation_path_image):
    if os.path.exists(buffer_simulation_path_image):
        try:
            os.remove(buffer_simulation_path_image)
            print(f"File updated successfully: {buffer_simulation_path_image}", end="\n")
        except Exception as e:
            print(f"Error deleting file: {str(e)}", end="\n")
    else:
        print(f"File not found: {buffer_simulation_path_image}", end="\n")
        print(f"File created successfully: {buffer_simulation_path_image}", end="\n")
