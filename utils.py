import re
import requests
import os

def extract_scenes(text):
    """ """
    scenes = {}
    scene_blocks = re.findall(r'(Scene \d+:\s*.*?Description:.*?)(?=Scene \d+:|$)', text, re.DOTALL)

    for block in scene_blocks:
        if block.startswith("Scene"):
            scene_number = int(re.search(r'Scene (\d+)', block).group(1))
            description = re.search(r'Description:\s*(.*)', block, re.DOTALL).group(1).strip()
            scenes[scene_number] = description
    return scenes

def download_image_from_URL(image_url, img_path = 'generated_dreams', img_num=0, recent_folder='example'):
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Open a file in binary write mode
        #TODO: Create an option to make a directory based on the date the dream was created.
        os.makedirs(f"{img_path}/{recent_folder}", exist_ok=True)
        with open(f"{img_path}/{recent_folder}/dream_frame_{img_num}.jpg", "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        print(f"Dream image {img_num} was successfully downloaded and saved.")
    else:
        print(f"Failed to retrieve the image. Status code: {response.status_code}")

    
    