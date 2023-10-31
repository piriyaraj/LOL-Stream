import json
import os
import shutil
from usecases.upload_youtube import UploadYoutube

base = os.path.abspath('yt')
videoFolder = os.listdir(base)

def removeFolder(folder):
    try:
        # Check if the folder exists
        if os.path.exists(folder):
            # Use shutil.rmtree to remove the folder and its contents
            shutil.rmtree(folder)
            print(f"Folder '{folder}' and its contents have been removed.")
        else:
            print(f"Folder '{folder}' does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")

def videoUploader():
    for uploadPath in videoFolder:
        folder_path = os.path.join(base, uploadPath)
        
        if not os.path.isdir(folder_path):
            continue  # Skip if it's not a directory
        
        all_files = os.listdir(folder_path)
        
        if len(all_files) == 0:
            removeFolder(folder_path)
            continue
        
        video_files = [file for file in all_files if file.endswith('.mkv')]
        if len(video_files) == 0:
            removeFolder(folder_path)
            continue
        thumbnail = os.path.join(folder_path, 'thumbnail.png')
        matchData_path = os.path.join(folder_path, 'match_data.json')
        videoPath = os.path.join(folder_path, video_files[0])
        
        print("Thumbnail:", thumbnail)
        print("Match Data:", matchData_path)
        print("Video Path:", videoPath)
        
        try:
            with open(matchData_path, 'r',encoding='utf-8') as matchData:
                match_data = json.load(matchData)
                uploader = UploadYoutube(match_data, videoPath)
                uploader.upload_video()
        except Exception as e:
            print(f"Error processing folder '{folder_path}': {str(e)}")

        # Optionally remove the folder after processing
        # removeFolder(folder_path)

