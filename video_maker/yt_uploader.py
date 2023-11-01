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
                uploader = UploadYoutube(match_data, videoPath,thumbnail)
                uploader.upload_video()
        except Exception as e:
            print(f"Error processing folder '{folder_path}': {str(e)}")

        # Optionally remove the folder after processing
        # removeFolder(folder_path)

if __name__ == '__main__':
    # Create a folder inside the 'yt' directory
    new_folder_name = 'test_folder'
    new_folder_path = os.path.join(base, new_folder_name)
    os.makedirs(new_folder_path, exist_ok=True)

    # Create dummy files inside the new folder
    with open(os.path.join(new_folder_path, 'thumbnail.png'), 'w') as thumbnail_file:
        thumbnail_file.write('Thumbnail content')

    match_data = {
        'title': 'Test Video',
        'description': 'This is a test video',
        # Add other required fields
    }
    with open(os.path.join(new_folder_path, 'match_data.json'), 'w', encoding='utf-8') as match_data_file:
        json.dump(match_data, match_data_file)

    with open(os.path.join(new_folder_path, 'test.mkv'), 'w') as test_video_file:
        test_video_file.write('Test video content')

    # Call the videoUploader function
    videoUploader()
    pass