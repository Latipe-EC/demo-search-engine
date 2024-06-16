import numpy as np
import feature_extractor as featEx
from pathlib import Path
from PIL import Image

DATASET_PATH = "./image_db"
FEATURES_PATH = "./features_index"

def extractor_exec_image_db():
    fe = featEx.FeatureExtractor()
    for img_path in sorted(Path(DATASET_PATH).rglob("*.jpg")):
        print(img_path)

        # Extract deep feature
        feature = fe.extract(img=Image.open(img_path))

        # Tạo đường dẫn tương ứng trong thư mục features_index
        relative_path = img_path.relative_to(DATASET_PATH)
        feature_path = Path(FEATURES_PATH) / relative_path.with_suffix(".npy")

        # Tạo các thư mục con nếu chúng chưa tồn tại
        feature_path.parent.mkdir(parents=True, exist_ok=True)

        print(feature_path)

        # Save the feature
        np.save(feature_path, feature)

# Chạy hàm để thực hiện trích xuất đặc trưng
#extractor_exec_image_db()
