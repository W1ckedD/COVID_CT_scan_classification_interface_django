import cv2
import numpy as np

def preprocess_img(img_dir):
  img = cv2.imread(img_dir)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = img / 255
  img = cv2.resize(img, (256, 256))
  img = np.reshape(img, (1, 256, 256, 1))
  
  return img