import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import time

from engine_service.search_engine import SearchEngine

# Đường dẫn tới dataset
dataset_folder = Path('image_db_test_db')

# Khởi tạo SearchEngine
se = SearchEngine()

total_images = 0
# Biến lưu số lượng ảnh đúng và sai
correct = 0
total = 0

# Danh sách lưu thời gian thực hiện
times = []

# Duyệt qua tất cả các thư mục con trong dataset
for product_folder in tqdm(dataset_folder.iterdir()):
    if product_folder.is_dir():
        product_id = product_folder.name
        # Duyệt qua từng ảnh trong thư mục
        for img_path in product_folder.glob('*.jpg'):
            # Đọc ảnh
            img = Image.open(img_path).resize((224, 224))
            total_images+= 1
            # Bắt đầu đo thời gian
            start_time = time.time()
            # Thực hiện tìm kiếm
            results, _ = se.search(img, size=10)
            # Kết thúc đo thời gian
            end_time = time.time()
            # Tính toán thời gian thực hiện và lưu lại
            times.append(end_time - start_time)
            product_ids = [result.parent.name for result in results]
            # Kiểm tra kết quả đầu tiên
            for i in range(4):
                if product_ids[i] == product_id:
                    correct += 1
                    break
            total += 1

# Tính toán độ chính xác
accuracy = correct / total
print(f'Dộ chính xác: {accuracy * 100:.2f}%')

# Vẽ biểu đồ độ chính xác
labels = ['4 KQ đầu tiên', 'Sau 4 KQ hoặc không có']
counts = [correct, total - correct]
colors = ['#4CAF50', '#F44336']

fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Biểu đồ tròn
ax[0].pie(counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax[0].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax[0].set_title('Độ chính xác của hệ thống tìm kiếm')

# Biểu đồ đường thể hiện thời gian
ax[1].plot(times, marker='o')
ax[1].set_title('Thời gian thực hiện hàm search()')
ax[1].set_xlabel('Lần thực hiện')
ax[1].set_ylabel('Thời gian (giây)')

print(f'Tổng số ảnh: {total_images}')
plt.tight_layout()
plt.show()
