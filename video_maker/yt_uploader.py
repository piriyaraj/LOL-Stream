import logging
import json
import os
import shutil
import time
from usecases.upload_youtube import UploadYoutube

base = os.path.abspath('yt')
videoFolder = os.listdir(base)
recordVideoFolder = r"Z:\Gameplay"
logging.basicConfig(filename='../LoL stream.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def removeFolder(folder):
    try:
        # Check if the folder exists
        if os.path.exists(folder):
            # Use shutil.rmtree to remove the folder and its contents
            shutil.rmtree(folder)
            print(f"Folder '{folder}' and its contents have been removed.")
            logging.info(
                f"yt_uploader(removeFolder): Folder '{folder}' and its contents have been removed.")
        else:
            print(f"Folder '{folder}' does not exist.")
            logging.warning(
                f"yt_uploader(removeFolder): Folder '{folder}' does not exist.")
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"yt_uploader(removeFolder): Error: {str(e)}")

count = 1
def moveVideo(sourceFolder, destFolder):
    global count
    try:
        # Check if the source folder exists
        if not os.path.exists(sourceFolder):
            print(f"Source folder '{sourceFolder}' does not exist.")
            logging.warning(
                f"yt_uploader(moveVideo): Source folder '{sourceFolder}' does not exist.")
            return

        # Check if the destination folder exists, and if not, create it
        if not os.path.exists(destFolder):
            os.makedirs(destFolder)

        # Get a list of all files in the source folder
        files_to_move = os.listdir(sourceFolder)

        # Move each file to the destination folder
        # for file in files_to_move:
        file = files_to_move[-1]
        source_path = os.path.join(sourceFolder, file)
        dest_path = os.path.join(destFolder, file)
        shutil.move(source_path, dest_path)
        print(f"Moved '{file}' to '{destFolder}'")
        logging.info(
            f"yt_uploader(moveVideo): Moved '{file}' to '{destFolder}'")

    except Exception as e:
        if "being used by another process:" in str(e):
            time.sleep(10)
            if count <=3:
                moveVideo(sourceFolder, destFolder)
                count += 1
        else:
            print(f"Error: {str(e)}")


def videoUploader(new_folder_path):
    moveVideo(recordVideoFolder, new_folder_path)
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

        logging.info("yt_uploader(videoUploader): Thumbnail: %s", thumbnail)
        logging.info("yt_uploader(videoUploader): Match Data: %s",
                     matchData_path)
        logging.info("yt_uploader(videoUploader): Video Path: %s", videoPath)

        try:
            with open(matchData_path, 'r', encoding='utf-8') as matchData:
                match_data = json.load(matchData)
                uploader = UploadYoutube(match_data, videoPath, thumbnail)
                uploader.upload_video()
        except Exception as e:
            print(f"yt_uploader(videoUploader): {str(e)}")
            logging.error(
                f"yt_uploader(videoUploader): Error processing folder '{folder_path}': {str(e)}")

        # Optionally remove the folder after processing
        removeFolder(folder_path)


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
    videoUploader(r"yt\test_folder")
    pass
