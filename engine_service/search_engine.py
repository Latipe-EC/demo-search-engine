import numpy as np
#fix import library error
import sys
sys.path.append('engine_service')
import extractor_exec as extrExe
import feature_extractor as featEx

from pathlib import Path


class SearchEngine:
    # change this code to singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SearchEngine, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.features = []
        self.img_paths = []

        # Sử dụng rglob để tìm tất cả các tệp .npy trong thư mục con của FEATURES_PATH
        for feature_path in Path(extrExe.FEATURES_PATH).rglob("*.npy"):
            self.features.append(np.load(feature_path))
            self.img_paths.append(Path(extrExe.DATASET_PATH) / feature_path.relative_to(extrExe.FEATURES_PATH).with_suffix(".jpg"))

        self.features = np.array(self.features)

        self.fe = featEx.FeatureExtractor()
        print(self.features.shape)

    def search(self, img, size=9):
        query = self.fe.extract(img)
        dists = np.linalg.norm(self.features - query, axis=1)  # L2 distances to the features
        ids = np.argsort(dists)[:size]  # Top 9 results
        product_id = [self.img_paths[id] for id in ids]
        return product_id, dists

function = SearchEngine()