import pyautogui
import time
from PIL import Image, ImageChops

frozenCount = 0
# Initialize the previous_screen as None
previous_screen = None

# Define a function to capture the game screen
def capture_screen():
    screenshot = pyautogui.screenshot()
    return screenshot

# Define a function to compare two screenshots for similarity
def compare_screens(screen1, screen2):
    # Convert the screenshots to grayscale for better comparison
    screen1_gray = screen1.convert('L')
    screen2_gray = screen2.convert('L')

    # Calculate the absolute difference between the two grayscale screenshots
    diff = ImageChops.difference(screen1_gray, screen2_gray)

    # Calculate the mean of the squared differences
    rms = sum(diff.getdata()) / float(screen1_gray.size[0] * screen1_gray.size[1])

    return rms

# Define a function to check for screen freezing
def check_for_freeze():
    global previous_screen  # Declare previous_screen as a global variable
    global frozenCount
    # Capture the current game screen
    current_screen = capture_screen()

    # Check if the current screen is similar to the previous screen
    if previous_screen is not None:
        similarity_score = compare_screens(previous_screen, current_screen)

        # Set a threshold for the similarity score
        # If the score drops below the threshold, it may indicate freezing
        threshold = 0.5  # Adjust as needed
        # print(similarity_score)
        if similarity_score < threshold:
            # Trigger the function for handling screen freezing
            frozenCount+=1
        else:
            frozenCount -= 1
        if(frozenCount<0):
            frozenCount=0
        if frozenCount ==3:
                return True
    # Update the previous screen with the current screen
    previous_screen = current_screen
    return False

# Define a function to handle screen freezing
def handle_freeze():
    global frozenCount
    frozenCount+=1
    print("Screen freezing detected!")
    return frozenCount

def checkFrozen():
    # Main loop to continuously monitor the game screen
    while True:
        if check_for_freeze():
            return True
        else:
            time.sleep(2)  # Adjust the interval as needed
