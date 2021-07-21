import numpy as np
import matplotlib.pyplot as plt
import cv2 

img = cv2.imread("baby_shark.jpg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H_shark = img_hsv[:, :, 0]
S_shark = img_hsv[:, :, 1]
V_shark = img_hsv[:, :, 2]
fig, ax = plt.subplots(1, 3, figsize=(15, 10))
ax[0].plot(H_shark, cmap='hsv')
ax[1].plot(S_shark, cmap='Blues')
ax[2].plot(V_shark, cmap='gray')
plt.show()