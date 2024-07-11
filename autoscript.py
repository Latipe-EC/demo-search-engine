import json
import os
import shutil
from io import BytesIO

import requests
from PIL import Image
from bson import ObjectId

# Đọc dữ liệu từ file JSON
with open('prepare.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Tạo danh sách mới chỉ chứa các trường cần thiết
filtered_data = []

for item in data:
    filtered_item = {
        "_id": {"$oid": str(ObjectId())},
        "product_id": item["product_id"],
        "product_name": item["product_name"],
        "image_urls": item["image_urls"]
    }
    filtered_data.append(filtered_item)

# Ghi dữ liệu đã lọc ra file JSON mới
with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(filtered_data, file, ensure_ascii=False, indent=4)


if not os.path.exists("image_db_test_db"):
    os.makedirs("image_db_test_db")

def download_image(image_url, image_folder):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        img_name = os.path.basename(image_url)
        img_name = os.path.splitext(img_name)[0] + '.jpg'  # Ensure the file extension is .jpg
        img_path = os.path.join(image_folder, img_name)

        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")  # Convert image to RGB mode
        resized_image = image.resize((224, 224))

        resized_image.save(img_path, format="JPEG")

        print(f"Download success: {image_url} and storage in: {img_path}")
    except requests.RequestException as e:
        print(f"Error while download {image_url}: {e}")
    except Exception as e:
        print(f"Error while process {image_url}: {e}")

for product in data:
    product_id = product['product_id']
    img_urls = product['image_urls']

    img_folder_path = os.path.join("image_db", product_id)

    if os.path.exists(img_folder_path):
        shutil.rmtree(img_folder_path)

    # Tạo lại thư mục
    os.makedirs(img_folder_path)

    for img_url in  img_urls[-1:1:-1]:
        download_image(img_url, img_folder_path)

