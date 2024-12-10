import os
from src import config


def download_files_and_folders(drive, folder_id, local_folder_path):
    # Step 3.1: List the files and folders in the current folder
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

    for file in file_list:
        file_title = file['title']
        file_id = file['id']
        
        # Step 3.2: If it's a file, download it
        if 'mimeType' in file and file['mimeType'] != 'application/vnd.google-apps.folder':
            # Define the full path for saving the file locally
            file_path = os.path.join(local_folder_path, file_title)
            print(f"Downloading file: {file_title} to {file_path}...")
            downloaded_file = drive.CreateFile({'id': file_id})
            downloaded_file.GetContentFile(file_path)
            print(f"Downloaded {file_title} to {file_path}")
        
        # Step 3.3: If it's a folder, create the folder locally and recursively download its content
        elif 'mimeType' in file and file['mimeType'] == 'application/vnd.google-apps.folder':
            # Create the folder locally
            folder_path = os.path.join(local_folder_path, file_title)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            print(f"Entering folder: {file_title} at {folder_path}...")
            # Recursively download files and subfolders inside this folder
            download_files_and_folders(file_id, folder_path)
