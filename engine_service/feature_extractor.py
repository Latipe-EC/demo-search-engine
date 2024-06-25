import numpy as np

from tensorflow import keras
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image


from pathlib import Path
from PIL import Image

class FeatureExtractor:
  def __init__(self):
    base_model = keras.applications.VGG16(weights="imagenet")
    self.model = keras.models.Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

  def extract(self, img):
    # Resize the image
    img = img.resize((224, 224))
    # Convert the image color space
    img = img.convert('RGB')
    # Reformat the image
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    # Extract Features
    feature = self.model.predict(x)[0]
    return feature / np.linalg.norm(feature)
  