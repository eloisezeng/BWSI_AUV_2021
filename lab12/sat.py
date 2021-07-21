import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('baby_turtle.jpg')
img = np.flip(img, axis=2)
img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
turtle_H = img_hsv[:,:,0]
turtle_S = img_hsv[:,:,1]
turtle_V = img_hsv[:,:,2]

sfilt = cv2.boxFilter(img_hsv[:, :, 1], cv2.CV_32F, (40, 40))

fig, ax = plt.subplots(1, 2, figsize=(16, 6))
ax[0].imshow(turtle_S, cmap='Blues')
ax[1].imshow(sfilt, cmap='Blues') # Saturation: turtle stands out most
plt.show()