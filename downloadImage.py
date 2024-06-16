import json
import os
import random
import time
from io import BytesIO

import requests
from PIL import Image


def download_image(url, folder, filename):
    if not os.path.exists(f'{os.getcwd()}/data/{folder}'):
        os.makedirs(f'{os.getcwd()}/data/{folder}')
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed to fetch image: {url}")
        return

    try:
        # Open the image file
        img_down = Image.open(BytesIO(response.content))

        # Convert the image to RGB format
        img_down = img_down.convert('RGB')

        # Resize the image to 224x224 pixels
        img_down = img_down.resize((224, 224))

        # Save the processed image back to the file
        img_down.save(f'{os.getcwd()}/data/{folder}/{filename}', 'JPEG')
    except OSError:
        print(f"Image file {url} is truncated or corrupted. Skipping this file.")


# Open the JSON file
with open('prods.json', 'r', encoding='utf-8') as file:
    # Load the contents of the file into a list
    prods = json.load(file)
    if not os.path.exists(f'{os.getcwd()}/data'):
        os.makedirs(f'{os.getcwd()}/data')
    for prod in prods:
        # Loop through each product in the list
        for img in prod['images']:
            # Loop through each image in the product
            download_image(img, prod['id'], img.split('/')[-1])
            sleep_time = random.randint(1, 3)  # Generate a random integer between 1 and 5
            print(f"Sleeping for {sleep_time} seconds")
            time.sleep(sleep_time)




