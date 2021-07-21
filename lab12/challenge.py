import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread('message_Eloise.jpg')
t_B = img[:,:,0]
t_G = img[:,:,1]
t_R = img[:,:,2]

# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# turtle_H = img_hsv[:,:,0]
# turtle_S = img_hsv[:,:,1]
# turtle_V = img_hsv[:,:,2]

a = 100
b = 100
c = 100

# hfilt = cv2.boxFilter(img_hsv[:, :, 0], cv2.CV_32F, (a, a))
# sfilt = cv2.boxFilter(img_hsv[:, :, 1], cv2.CV_32F, (b, b))
# vfilt = cv2.boxFilter(img_hsv[:, :, 2], cv2.CV_32F, (c, c))

# fig, ax = plt.subplots(1, 3, figsize=(15, 10))
# ax[0].imshow(hfilt, cmap='Greys')
# ax[1].imshow(sfilt, cmap='Greys') # Saturation: turtle stands out most
# ax[2].imshow(vfilt, cmap='Greys')
# plt.show()

bfilt = cv2.boxFilter(img[:, :, 0], cv2.CV_32F, (a, a))
gfilt = cv2.boxFilter(img[:, :, 1], cv2.CV_32F, (b, b))
rfilt = cv2.boxFilter(img[:, :, 2], cv2.CV_32F, (c, c))
fig, ax = plt.subplots(1, 3, figsize=(15, 10))
ax[0].imshow(bfilt, cmap='Greys')
ax[1].imshow(gfilt, cmap='Greys') # Saturation: turtle stands out most
ax[2].imshow(rfilt, cmap='Greys')
plt.show()


