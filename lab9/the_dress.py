import numpy as np
import matplotlib.pyplot as plt
import cv2
img = cv2.imread("The_Dress.png") # reads in the channels in (B G R) order
img = np.flip(img, axis=2)
print(img.shape)

# reshape img numpy array as a 2D vector of the RGB value for each pixel in the img
# convert to float32 bc k-means function requires this dtype
data = np.reshape(img, (img.shape[0] * img.shape[1], 3)).astype(np.float32) 
print(data.shape)
ret, labels, centers = cv2.kmeans(data, 5, None, (cv2.TERM_CRITERIA_MAX_ITER, 1000, 0.0001), 1000, 
                                  cv2.KMEANS_RANDOM_CENTERS)
print(np.round(centers))
# data[(labels==0).squeeze(),:] = centers[0]
# data[(labels==1).squeeze(),:] = centers[1]
# data[(labels==2).squeeze(),:] = centers[2]
# data[(labels==3).squeeze(),:] = centers[3]
# data[(labels==4).squeeze(),:] = centers[4]

# data[(labels==0).squeeze(),:] = np.array([66, 245, 182]) # teal
# data[(labels==1).squeeze(),:] = np.array([203, 66, 245]) # pink
data[(labels==1).squeeze(),:] = np.array([237, 128, 160])
data[(labels==2).squeeze(),:] = np.array([245, 197, 66]) # yellow
# data[(labels==3).squeeze(),:] = np.array([66, 167, 245]) # blue
data[(labels==4).squeeze(),:] = np.array([237, 64, 107]) # rose pink

new_img = np.reshape(data, img.shape).astype(np.uint8)
print(new_img.shape)

print('here')
fig, ax = plt.subplots(1, 2, figsize=(9, 6))
ax[0].imshow(img)
ax[1].imshow(new_img) # plot the image
plt.show() # show the image
new_img = np.flip(new_img, axis=2)
cv2.imwrite('new_dress2.png', new_img)
# [[248. 249. 240.] # rgb(248, 249, 240) # white
#  [104. 103. 107.] # rgb(104, 103, 107) # gray
#  [123. 133. 165.] # rgb(123, 133, 165) # dark blue
#  [184. 179. 171.] # rgb(184, 179, 171) # light gray
#  [ 83.  74.  58.]] # rgb(83,  74,  58) # brown

########################################
