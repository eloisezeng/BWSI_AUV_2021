import numpy as np
import matplotlib.pyplot as plt
import cv2
img = cv2.imread("two_tone.png") # reads in the channels in (B G R) order
img = np.flip(img, axis=2)
print(img.shape)
plt.imshow(img)
plt.show()
# Teal: RGB- (71, 214, 255)
# Blue: RGB- (0, 0, 254)

# reshape img numpy array as a 2D vector of the RGB value for each pixel in the img
# convert to float32 bc k-means function requires this dtype
data = np.reshape(img, (img.shape[0] * img.shape[1], 3)).astype(np.float32) 
print(data.shape)

ret, labels, centers = cv2.kmeans(data, 2, None, (cv2.TERM_CRITERIA_MAX_ITER, 1000, 0.0001), 1000, 
                                  cv2.KMEANS_RANDOM_CENTERS)

# `ret`: sum of squared distance from each point to their corresponding centers
# `label`: assignments of our data points
# `centers`: array of average value of all members in each cluster
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

# `data`: 2D vector of RGB values for each pixel
# x coordinate: give R value for each pixel that was assigned to label 0 in the k-means algorithm
# y coordinate: give G value for each pixel that was assigned to label 0 in the k-means algorithm
# z coordinate: give B value for each pixel that was assigned to label 0 in the k-means algorithm
ax.scatter(data[(labels==0).squeeze(),0], data[(labels==0).squeeze(),1], data[(labels==0).squeeze(),2],
marker='o', c='k') # k: black

# x coordinate: give R value for each pixel that was assigned to label 1 in the k-means algorithm
# y coordinate: give G value for each pixel that was assigned to label 1 in the k-means algorithm
# z coordinate: give B value for each pixel that was assigned to label 1 in the k-means algorithm
ax.scatter(data[(labels==1).squeeze(),0], data[(labels==1).squeeze(),1], data[(labels==1).squeeze(),2],
marker='o', c='r')
ax.scatter(centers[0,0], centers[0,1], centers[0,2], marker='x', c='k')
ax.scatter(centers[1,0], centers[1,1], centers[1,2], marker='x', c='r')

ax.set_xlabel('R value')
ax.set_ylabel('G value')
ax.set_zlabel('B value')
plt.show()
# Notice there's not much overlap between the two groups

print(centers)
data[(labels==0).squeeze(),:] = np.array([255, 0, 0]) # change all the blue colors to red
data[(labels==1).squeeze(),:] = np.array([0, 255, 0]) # change all the teal colors to gree
new_img = np.reshape(data, img.shape)
print(new_img.shape)
plt.imshow(new_img) # plot the image
plt.show() # show the image