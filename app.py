import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from extractor_exec import extractor_exec_image_db
from search_engine import SearchEngine


from PIL import Image

# use this to extract features from images in the dataset when you first run the app
#extractor_exec_image_db()


# Create Search Engine
search_engine = SearchEngine()


img = Image.open("C:\\Users\\Admin\\Code\\Python\\image-search-engine\\iphone.jpg")
results, numerical_scores = search_engine.search(img,size=9)

for i in range(len(results)):
    im = mpimg.imread(results[i])
    plt.subplot(331 + i)
    plt.imshow(im)
    plt.text(0, 10, f'[{i}] Score: {numerical_scores[i]:.2f}', fontsize=9, color='white', backgroundcolor='black') 
    plt.axis('off')

plt.show()
