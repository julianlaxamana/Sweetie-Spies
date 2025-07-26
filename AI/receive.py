
# TODO: import your module
import requests
import os
import sys
from send_to_openai import describe
import time

# Get the folder where the script is located, done for you
script_dir = os.path.dirname(os.path.abspath(__file__))
react_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

filename = os.path.join(react_dir, "frontend/src/downloaded_image.jpg")
audiofile = os.path.join(react_dir, "frontend/src/description.wav")

url = "http://10.136.56.102/capture"

# Function to download the image from esp32, given to you
def download_image():
    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Image saved to: {filename}")
    else:
        print("Failed to download image. Status code:", response.status_code)

# TODO: Download the image and get a response from openai

def get_description():
    download_image()
    time.sleep(1)
    download_image()
    return describe(filename, audiofile)

if __name__ == "__main__":
    get_description()
    
# TODO: How to control when to take photo?

