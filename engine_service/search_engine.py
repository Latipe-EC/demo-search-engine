import numpy as np
from pathlib import Path

from config.variable import RETRIVAL_DB_FEATURE_FOLDER
from engine_service.feature_extractor import FeatureExtractor


class SearchEngine:
    # change this code to singleton

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SearchEngine, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.features = []
        self.RETRIVAL_DB_FEATURE_FOLDER = []

        # Sử dụng rglob để tìm tất cả các tệp .npy trong thư mục con của RETRIVAL_DB_FEATURE_FOLDER
        for feature_path in Path(RETRIVAL_DB_FEATURE_FOLDER).rglob("*.npy"):
            self.features.append(np.load(feature_path))
            self.RETRIVAL_DB_FEATURE_FOLDER.append(
                Path(RETRIVAL_DB_FEATURE_FOLDER) / feature_path.relative_to(RETRIVAL_DB_FEATURE_FOLDER).with_suffix(".npy"))

        self.features = np.array(self.features)

        self.fe = FeatureExtractor()
        print(self.features.shape)

    def update_instance(self):
        self.features = []
        self.RETRIVAL_DB_FEATURE_FOLDER = []

        for feature_path in Path(RETRIVAL_DB_FEATURE_FOLDER).rglob("*.npy"):
            self.features.append(np.load(feature_path))
            self.RETRIVAL_DB_FEATURE_FOLDER.append(
                Path(RETRIVAL_DB_FEATURE_FOLDER) / feature_path.relative_to(RETRIVAL_DB_FEATURE_FOLDER).with_suffix(".npy")
            )

        self.features = np.array(self.features)
        print("Instance updated with new features.")
        print(self.features.shape)

    def search(self, img, size=9):
        query = self.fe.extract(img)
        dists = np.linalg.norm(self.features - query, axis=1)  # L2 distances to the features
        ids = np.argsort(dists)[:size]  # Top 9 results
        product_id = [self.RETRIVAL_DB_FEATURE_FOLDER[id] for id in ids]
        return product_id, dists


