import numpy as np
from feature_extractor import FeatureExtractor
from pathlib import Path
from PIL import Image

DATASET_PATH = "./image_db"
FEATURES_PATH = "./features_index"

def extractor_exec_image_db():
    fe = FeatureExtractor()
    for img_path in sorted(Path(DATASET_PATH).glob("*.jpg")):
        print(img_path)

        # Extract deep feature
        feature = fe.extract(img=Image.open(img_path))

        feature_path = Path(FEATURES_PATH)/(img_path.stem+".npy")
        print(feature_path)

        # Save the feature
        np.save(feature_path, feature)
