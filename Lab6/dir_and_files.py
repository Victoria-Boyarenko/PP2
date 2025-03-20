import os
import shutil

#1
def list_directories_and_files(path):
    directories = []
    files = []
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            directories.append(item)
        elif os.path.isfile(full_path):
            files.append(item)
    print("Directories:", directories)
    print("Files:", files)
    print("All contents:", os.listdir(path))

#2
def check_path_access(path):
    print(f"Exists: {os.path.exists(path)}")
    print(f"Readable: {os.access(path, os.R_OK)}")
    print(f"Writable: {os.access(path, os.W_OK)}")
    print(f"Executable: {os.access(path, os.X_OK)}")

#3
def test_path_existence(path):
    if os.path.exists(path):
        full_path = os.path.abspath(path)
        print(f"Path exists: {full_path}")
        print(f"Filename: {os.path.basename(full_path)}")
        print(f"Directory: {os.path.dirname(full_path)}")
    else:
        print("Path does not exist.")

#4
def count_lines_in_file(filepath):
    try:
        with open(filepath, 'r') as file:
            print("Number of lines:", sum(1 for line in file))
    except FileNotFoundError:
        print("File not found.")

#5
def write_list_to_file(filepath, data):
    with open(filepath, 'w') as file:
        for item in data:
            file.write(f"{item}\n")
    print("List written to file.")

#6
def generate_text_files():
    for letter in range(65, 91):   
        filename = f"{chr(letter)}.txt"
        with open(filename, 'w') as file:
            file.write(f"This is file {filename}\n")
    print("26 text files created.")

#7
def copy_file_content(src, dst):
    try:
        shutil.copy(src, dst)
        print(f"Contents copied from {src} to {dst}")
    except FileNotFoundError:
        print("Source file not found.")

#8
def delete_file(filepath):
    if not os.path.exists(filepath):
        print("File does not exist.")
    elif not os.access(filepath, os.W_OK):
        print("No permission to delete the file.")
    else:
        os.remove(filepath)
        print(f"File {filepath} deleted.")



list_directories_and_files(".")
print()

check_path_access("D:\C++\reprezent")
print()

test_path_existence("dir_and_files.py")
print()

count_lines_in_file("D:\\C++\\reprezent\\Lab6\\dir_and_files.py")
print()

write_list_to_file("output.txt", ["apple", "banana", "cherry"])
print()

generate_text_files()
print()

copy_file_content("A.txt", "B.txt")
print()

delete_file("D.txt")
