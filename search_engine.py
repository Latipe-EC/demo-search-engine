from extractor_exec import FeatureExtractor
import numpy as np
from pathlib import Path
from extractor_exec import DATASET_PATH
from extractor_exec import FEATURES_PATH

class SearchEngine:
    # change this code to singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SearchEngine, cls).__new__(cls)
        return cls.instance
    
    def __init__(self):
        self.features = []
        self.img_paths = []

        for feature_path in Path(FEATURES_PATH).glob("*.npy"):
            self.features.append(np.load(feature_path))
            self.img_paths.append(Path(DATASET_PATH)/(feature_path.stem+".jpg"))
        self.features = np.array(self.features)

        self.fe=FeatureExtractor()
        self.features = self.features
        print(self.features.shape)

    def search(self,img,size=9):
        query = self.fe.extract(img)
        dists = np.linalg.norm(self.features - query, axis=1) # L2 distances to the features
        ids = np.argsort(dists)[:size] # Top 9 results
        scores = [self.img_paths[id] for id in ids]
        return scores, dists

    