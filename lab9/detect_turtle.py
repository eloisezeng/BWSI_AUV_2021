import numpy as np
import matplotlib.pyplot as plt
import cv2
img = cv2.imread("baby_turtle.jpg") # reads in the channels in (B G R) order
print(img.shape)
red_turtle = img[:, :, 2]
green_turtle = img[:, :, 1]
blue_turtle = img[:, :, 0]

# show individual r, g, b components
fig, ax = plt.subplots(1, 3, figsize=(15, 10))
ax[0].imshow(red_turtle, cmap="Reds")
ax[1].imshow(green_turtle, cmap="Greens")
ax[2].imshow(blue_turtle, cmap="Blues")
plt.show()

# show individual h, s, v components
dst = img.shape # dst stands for destination. Make the destination of img_hsv be the same size as the src
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
H_turtle = img_hsv[:, :, 0]
S_turtle = img_hsv[:, :, 1]
V_turtle = img_hsv[:, :, 2]

fig, ax = plt.subplots(1, 3, figsize=(15, 10))
h = ax[0].imshow(H_turtle, cmap="hsv") # What we perceive as color
s = ax[1].imshow(S_turtle, cmap="Blues") # Intensity of color, e.g. light blue vs bold blue
v = ax[2].imshow(V_turtle, cmap="gray") # position on a scale from black to white

fig.colorbar(h, ax=ax[0], shrink=0.2)
fig.colorbar(s, ax=ax[1], shrink=0.2)
fig.colorbar(v, ax=ax[2], shrink=0.2)
plt.show()

# define range of green color in HSV, which is the color of turtle
# Hue ranges from [0, 179]
# Saturation ranges from [0, 255]
# Value ranges from [0, 255]

lower_green = (40, 70, 50)
upper_green = (80, 255, 100)

# Threshold the HSV image to get only green colors
mask = cv2.inRange(img_hsv, lower_green, upper_green)
print(mask.shape) # 1080, 1920
img_cp = img

# Bitwise-AND mask and original image
# Combine mask with copy of image (so only valid green colors show up in og image)
res = cv2.bitwise_and(img, img, mask=mask)
print(res.shape)
res = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
fig, ax = plt.subplots()
ax.imshow(res, cmap="hsv") # What we perceive as color
plt.show()