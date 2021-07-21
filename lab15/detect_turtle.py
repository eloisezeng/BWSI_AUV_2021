import numpy as np
import cv2
import matplotlib.pyplot as plt
from calculate_angles import sensor_position, get_angles

def detect_turtle(img):
    imhsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    imhsv = cv2.boxFilter(imhsv, -1, (10, 10))
    img_thresh_hue = np.logical_and(imhsv[:,:,0] > 35, imhsv[:,:,0] < 255)
    img_thresh_sat = np.logical_and(imhsv[:,:,1] > 110, imhsv[:,:,1] < 200)
    img_thresh_HS = np.logical_and(img_thresh_hue, img_thresh_sat)
    # The value threshold doesn't help that much with detecting the turtle, 
    # so we don't need to include it
    img_filter = cv2.boxFilter(img_thresh_HS.astype(int), -1, (50,50), normalize=False)
    thresh = 1000 # Q: How do we choose this threshhold. Manually test.
    center = np.average((np.argwhere(img_filter>thresh)), axis=0) 
    # ^ get average pixel positions of where the pixels were greater than threshold
    center = np.flip(center) # argwhere returns indices with y first, then x.
    angles = get_angles(sensor_position(center[0], center[1]))
    return center, angles

fig, ax = plt.subplots()
for frame_num in range(1418, 1518):
    img = cv2.imread(f'turtle_frames/gopro{frame_num:05d}.jpg') # 05d means 5 digits will appear
    img = cv2.resize(img, (640, 480))
    center, angles = detect_turtle(img)
    print(angles)
    ax.clear()
    ax.imshow(img)
    ax.plot(center[0], center[1], 'bo')
    plt.pause(0.001)
    plt.draw()
