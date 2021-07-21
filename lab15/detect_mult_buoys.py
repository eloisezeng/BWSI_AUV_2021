import numpy as np
import cv2
import matplotlib.pyplot as plt
from calculate_angles import sensor_position, get_angles

def get_centers(thresh, img_threshold_color):
    # Convert to uint8 so we can find contours around GREEN buoys we want to detect
    img8 = (img_threshold_color * 255 / np.max(img)).astype(np.uint8)
    thresh8 = (thresh * 255 / np.max(img)).astype(np.uint8)
    thresh, img_out = cv2.threshold(img8, thresh8, 255, cv2.THRESH_BINARY)
    """The image should still have one of two possible values at each pixel."""
    contours, hierarchy = cv2.findContours(img_out, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    centers = []
    for contour in contours:
        center = np.mean(contour, axis=0)[0]
        centers.append(center)
        # ^ Need to index 0 because np.mean(contour, axis=0)...
        # returns np.array([[mean]]) not np.array([mean])
    return centers

def find_angles(centers):
    angles = []
    for center in centers:
        angle_for_center = get_angles(sensor_position(center[0], center[1]))
        angles.append(angle_for_center)
    return angles

def detect_buoys(img):
    img = cv2.boxFilter(img, -1, (5, 5))
    # Detect Green Buoy
    filter_size = (10, 10) # P: may need to change when we get closer to buoy
    rfilt = cv2.boxFilter(img[:, :, 0], cv2.CV_32F, filter_size)
    img_threshold_green = np.logical_and(rfilt > 0, rfilt < 120)
    gfilt = cv2.boxFilter(img[:, :, 1], cv2.CV_32F, filter_size)
    img_threshold_red = np.logical_and(gfilt > 0, gfilt < 150)
    thresh = 0 # img_threshold_red values are either 0 or 1... 
    # but if we used cv2.boxFilter with normalize = False, the pixel values would have values...
    # in range of 0 to the size of the filter

    # avg_red_buoy_pos = np.average((np.argwhere(img_threshold_red>thresh)), axis=0)
    # avg_green_buoy_pos = np.average((np.argwhere(img_threshold_green>thresh)), axis=0)
    # Only works if there's only one buoy corrected, so we'll need to detect contours

    g_centers = get_centers(thresh, img_threshold_green)
    r_centers = get_centers(thresh, img_threshold_red)
    g_angles = find_angles(g_centers)
    r_angles = find_angles(r_centers)
    return g_centers, r_centers, g_angles, r_angles

fig, ax = plt.subplots()
for frame_num in range(0, 20):
    img = cv2.imread(f'buoy_simulation/frame_{frame_num:02d}.jpg')
    img = np.flip(img, axis=2) # Convert BGR to RGB
    g_centers, r_centers, g_angles, r_angles = detect_buoys(img)
    print(g_angles)
    print('\n')
    print(r_angles)
    ax.clear()
    ax.imshow(img)
    for g_center in g_centers:
        ax.plot(g_center[0], g_center[1], 'bo')
    for r_center in r_centers:
        ax.plot(r_center[0], r_center[1], 'ko')
    plt.pause(0.0001)
    plt.draw()
