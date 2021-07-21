import cv2
import numpy as np
import matplotlib.pyplot as plt

def sensor_position(pix_x, pix_y, res_x=3280, res_y=2464): # res_x = img.shape[0]; res_y = img.shape[1]
    x = 3.68 # length of camera sensor in mm
    y = 2.76 # height of camera sensor in mm
    # adjust pixel coordinate system so (0, 0) is in the center of the camera sensor, 
    # not at the corner of the pixel frame
    sensor_pos_x_pixel = pix_x - res_x / 2
    sensor_pos_y_pixel = pix_y - res_y / 2
    sensor_pos_x = round(sensor_pos_x_pixel * x / res_x, 5)
    sensor_pos_y = round(sensor_pos_y_pixel * y / res_y, 5)
    return (sensor_pos_x, sensor_pos_y) # position of point on the sensor (mm)

def get_angles(sensor_pos):
    sensor_pos_x, sensor_pos_y = sensor_pos
    f = 3.04 # mm. f: focal length
    # r = f * tanθ
    # θ = arctan(r / f)
    horizontal_angle = np.arctan2(sensor_pos_x, f) * 180 / np.pi
    vertical_angle = np.arctan2(sensor_pos_y, f) * 180 / np.pi
    return (horizontal_angle, vertical_angle)
