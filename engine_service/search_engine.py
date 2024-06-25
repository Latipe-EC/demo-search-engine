import numpy as np
from pathlib import Path

from engine_service.extractor_exec import FEATURES_PATH, DATASET_PATH
from engine_service.feature_extractor import FeatureExtractor


class SearchEngine:
    # change this code to singleton

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SearchEngine, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.features = []
        self.features_path = []

        # Sử dụng rglob để tìm tất cả các tệp .npy trong thư mục con của FEATURES_PATH
        for feature_path in Path(FEATURES_PATH).rglob("*.npy"):
            self.features.append(np.load(feature_path))
            self.features_path.append(
                Path(FEATURES_PATH) / feature_path.relative_to(FEATURES_PATH).with_suffix(".npy"))

        self.features = np.array(self.features)

        self.fe = FeatureExtractor()
        print(self.features.shape)

    def update_instance(self):
        self.features = []
        self.features_path = []

        for feature_path in Path(FEATURES_PATH).rglob("*.npy"):
            self.features.append(np.load(feature_path))
            self.features_path.append(
                Path(FEATURES_PATH) / feature_path.relative_to(FEATURES_PATH).with_suffix(".npy")
            )

        self.features = np.array(self.features)
        print("Instance updated with new features.")
        print(self.features.shape)

    def search(self, img, size=9):
        query = self.fe.extract(img)
        dists = np.linalg.norm(self.features - query, axis=1)  # L2 distances to the features
        ids = np.argsort(dists)[:size]  # Top 9 results
        product_id = [self.features_path[id] for id in ids]
        return product_id, dists


