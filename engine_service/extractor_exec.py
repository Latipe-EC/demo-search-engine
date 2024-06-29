import os
import shutil

import numpy as np

import config.variable as configEnv

from pathlib import Path
from PIL import Image
import requests
from PIL import Image
from io import BytesIO

from engine_service.feature_extractor import FeatureExtractor


def extractor_exec_image_db():
    fe = FeatureExtractor()
    for img_path in sorted(Path(configEnv.RETRIEVAL_DB_IMAGE_FOLDER).rglob("*.jpg")):
        print(img_path)

        # Extract deep feature
        feature = fe.extract(img=Image.open(img_path))

        relative_path = img_path.relative_to(configEnv.RETRIEVAL_DB_IMAGE_FOLDER)
        feature_path = Path(configEnv.RETRIVAL_DB_FEATURE_FOLDER) / relative_path.with_suffix(".npy")
        feature_path.parent.mkdir(parents=True, exist_ok=True)
        # Save the feature
        np.save(feature_path, feature)

    # Delete all folders in configEnv.RETRIEVAL_DB_IMAGE_FOLDER when finish extracting
    for folder in Path(configEnv.RETRIEVAL_DB_IMAGE_FOLDER).iterdir():
        if folder.is_dir():
            shutil.rmtree(folder)
            print(f"Đã xóa thư mục: {folder}")


async def extractor_exec_product_image_db(untrained_product: dict):
    fe = FeatureExtractor()
    product_id = untrained_product['product_id']
    img_urls = untrained_product['image_urls']

    img_folder_path = os.path.join(configEnv.RETRIEVAL_DB_IMAGE_FOLDER, product_id)
    if os.path.exists(img_folder_path):
        shutil.rmtree(img_folder_path)
    os.makedirs(img_folder_path)

    for img_url in img_urls:
        download_image(img_url, img_folder_path)

    for img_path in sorted(Path(img_folder_path).rglob("*.jpg")):

        # Extract deep feature
        feature = fe.extract(img=Image.open(img_path))

        relative_path = img_path.relative_to(configEnv.RETRIEVAL_DB_IMAGE_FOLDER)
        feature_path = Path(configEnv.RETRIVAL_DB_FEATURE_FOLDER) / relative_path.with_suffix(".npy")
        feature_path.parent.mkdir(parents=True, exist_ok=True)
        # Save the feature
        np.save(feature_path, feature)

    # Delete all folders in img_folder_path when finish extracting
    shutil.rmtree(img_folder_path)


def download_image_db(untrained_products):
    if not os.path.exists(configEnv.RETRIEVAL_DB_IMAGE_FOLDER):
        os.makedirs(configEnv.RETRIEVAL_DB_IMAGE_FOLDER)

    for product in untrained_products:
        product_id = product['product_id']
        img_urls = product['image_urls']

        img_folder_path = os.path.join(configEnv.RETRIEVAL_DB_IMAGE_FOLDER, product_id)

        if os.path.exists(img_folder_path):
            shutil.rmtree(img_folder_path)

        # Tạo lại thư mục
        os.makedirs(img_folder_path)

        download_image(img_urls, img_folder_path)
        for img_url in img_urls:
            download_image(img_url, img_folder_path)


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
