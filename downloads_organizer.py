import os
import shutil
import time

# Define base Downloads directory
downloads_dir = '/Users/boraytuna/Downloads'

# Define categorized subdirectories
subdirectories = ["Images", "Music", "Videos", "Documents", "Code", "Other"]
for subdir in subdirectories:
    os.makedirs(os.path.join(downloads_dir, subdir), exist_ok=True)

# File extension categories
image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg"]
music_extensions = [".mp3", ".wav", ".aiff", ".aac", ".flac", ".m4a", ".ogg"]
video_extensions = [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"]
doc_extensions = [".txt", ".pdf", ".docx", ".doc", ".xlsx", ".pptx", ".csv", ".odt"]
code_extensions = [".py", ".java", ".js", ".ts", ".cpp", ".c", ".cs", ".swift", ".html", ".css", ".lua", ".php", ".rb", ".go", ".rs", ".json", ".xml"]

def has_code_files(dir_path):
    """Check if a directory contains any code files."""
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if any(file.endswith(ext) for ext in code_extensions):
                return True
    return False

def move_file_safely(src_path, target_folder, filename):
    """Move file without overwriting by renaming duplicates."""
    target_path = os.path.join(target_folder, filename)
    if not os.path.exists(target_path):
        shutil.move(src_path, target_path)
    else:
        base, ext = os.path.splitext(filename)
        i = 1
        while True:
            new_filename = f"{base}_{i}{ext}"
            new_target_path = os.path.join(target_folder, new_filename)
            if not os.path.exists(new_target_path):
                shutil.move(src_path, new_target_path)
                break
            i += 1

while True:
    for item in os.listdir(downloads_dir):
        if item.startswith('.'):
            continue  # Skip hidden/system files

        item_path = os.path.join(downloads_dir, item)

        # Skip already sorted folders
        if item in subdirectories:
            continue

        # File handling
        if os.path.isfile(item_path):
            extension = os.path.splitext(item)[1].lower()
            if extension in image_extensions:
                target_dir = os.path.join(downloads_dir, "Images")
            elif extension in music_extensions:
                target_dir = os.path.join(downloads_dir, "Music")
            elif extension in video_extensions:
                target_dir = os.path.join(downloads_dir, "Videos")
            elif extension in doc_extensions:
                target_dir = os.path.join(downloads_dir, "Documents")
            elif extension in code_extensions:
                target_dir = os.path.join(downloads_dir, "Code")
            else:
                target_dir = os.path.join(downloads_dir, "Other")

            move_file_safely(item_path, target_dir, item)

        # Folder handling
        elif os.path.isdir(item_path):
            if has_code_files(item_path):
                target_dir = os.path.join(downloads_dir, "Code")
            else:
                target_dir = os.path.join(downloads_dir, "Other")

            move_file_safely(item_path, target_dir, item)

    time.sleep(60)  # Re-check every 60 seconds