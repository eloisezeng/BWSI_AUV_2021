import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('cactus.jpg')
img = np.flip(img, 2)
print(img.shape)

res_x=3280
res_y=2464

plt.imshow(img)
plt.plot(1750, 950, 'bo', markersize=5) # anchor point for cactus (top of pot)
plt.plot(1750, 1700, 'yo', markersize=5) # dot at the bottom of pot
plt.plot(2870, 1050, 'ro', markersize=5) # anchor point for water
# plt.plot(2870, 1600, 'ro', markersize=5) # bottom of water
plt.plot(res_x / 2, res_y / 2, 'go', markersize=5) # CCSO
plt.show()


def sensor_position(pix_x, pix_y, res_x=res_x, res_y=res_y): # res_x = img.shape[0]; res_y = img.shape[1]
    x = 3.68 # length of camera sensor in mm
    y = 2.76 # height of camera sensor in mm
    # adjust pixel coordinate system so (0, 0) is in the center of the camera sensor, 
    # not at the corner of the pixel frame
    sensor_pos_x_pixel = pix_x - res_x / 2
    sensor_pos_y_pixel = pix_y - res_y / 2
    sensor_pos_x = round(sensor_pos_x_pixel * x / res_x, 5)
    sensor_pos_y = round(sensor_pos_y_pixel * y / res_y, 5)
    return (sensor_pos_x, sensor_pos_y) # position of point on the sensor (mm)

cactus_sensor_pos = sensor_position(1750, 950)
water_sensor_pos = sensor_position(2870, 1050)
# water_sensor_pos_bottom = sensor_position(2870, 1600)
print("cactus_sensor_pos", cactus_sensor_pos)
# print("water_sensor_pos", water_sensor_pos)

def get_angles(sensor_pos_x, sensor_pos_y):
    f = 3.04 # mm. f: focal length
    # r = f * tanθ
    # θ = arctan(r / f)
    horizontal_angle = np.arctan2(sensor_pos_x, f) * 180 / np.pi
    vertical_angle = np.arctan2(sensor_pos_y, f) * 180 / np.pi
    return (horizontal_angle, vertical_angle)
cactus_angles = get_angles(cactus_sensor_pos[0], cactus_sensor_pos[1])
water_angles = get_angles(water_sensor_pos[0], water_sensor_pos[1]) # angles for top of water
# water_angles_bottom = get_angles(water_sensor_pos_bottom[0], water_sensor_pos_bottom[1])
print("cactus_angles", cactus_angles)
print("water_angles", water_angles)
# print("water_angles_bottom", water_angles_bottom)

# Calculate height of the CCSO (Camera Coordinate System Origin)
# dist_sensor2pot = 62 cm
# blue_dot_height = 18 cm
theta = abs(cactus_angles[1]) # vertical angle from sensor to blue dot on the pot
# x = blue_dot_height - height of CCSO = 18 - height of CCSO
# height of CCSO = 18 - x
# tanθ = x / 62
# x = 62 * tanθ
# height of CCSO = 18 - 62 * tanθ
ccso_height = 18 - 62 * np.tan(theta * np.pi / 180) # convert to radians for the np.tan function
print(round(ccso_height, 2))

# sanity check that 11.56 cm is realistic
# Check that ratio between calculated height of CCSO and height of blue dot is similar 
# to the ratio between the heights in pixels
ratio = ccso_height / 18
print(ratio)
pixel_height_CCSO = (1700 - res_y / 2) # 1700 is y coordinate at bottom of pot. 
# res_y / 2 is y coordinate of center of camera sensor
pixel_height_bluedot = 1700 - 950
pixel_ratio = pixel_height_CCSO / pixel_height_bluedot
print(pixel_ratio)
# ratio and pixel_ratio are roughly equal

# Measure height of water bottle
# Assume floor is level
# Water bottle is not on carpet
carpet_thickness = 1.5 # cm
# Dist from bottom of water bottle to CCSO = 11.57 + 1.5 cm
# x = height of water bottle - (11.57 + 1.5)
dist_water2sensor = np.sqrt((62 + 49) ** 2 + 51 ** 2)
# tanθ = x / dist_water2sensor
x = dist_water2sensor * np.tan(abs(water_angles[1]) * np.pi / 180) 
water_height = round(x + (ccso_height + carpet_thickness), 2)
print(water_height)



