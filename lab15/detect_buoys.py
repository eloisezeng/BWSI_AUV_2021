import numpy as np
import cv2
import matplotlib.pyplot as plt
from calculate_angles import sensor_position, get_angles

def get_angles(centers):
    angles = []
    # for center in centers:
    #     angle_for_center = get_angles(sensor_position(center[0], center[1]))
    #     angles.append(angle_for_center)
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

    g_center = np.average((np.argwhere(img_threshold_red>thresh)), axis=0)[::-1]
    r_center = np.average((np.argwhere(img_threshold_green>thresh)), axis=0)[::-1]
    g_angles = get_angles(g_center)
    r_angles = get_angles(r_center)
    return g_center, r_center, g_angles, r_angles

fig, ax = plt.subplots()
for frame_num in range(14, 16):
    img = cv2.imread(f'buoy_simulation/frame_{frame_num:02d}.jpg')
    img = np.flip(img, axis=2) # Convert BGR to RGB
    g_center, r_center, g_angles, r_angles = detect_buoys(img)
    print(g_center)
    # print(g_angles)
    # print('\n')
    # print(r_angles)
    # ax.clear()
    ax.imshow(img)
    ax.plot(g_center[0], g_center[1], 'bo')
    # for r_center in r_centers:
    #     ax.plot(r_centers[0], r_centers[1], 'ko')
    # plt.pause(0.001)
    # plt.draw()
    plt.show()
