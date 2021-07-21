import numpy as np
import cv2

noise = np.random.randn(1024, 1)
n = 5 # number of filters
for i in range(1, n + 1):
    noise_smoothed = cv2.boxFilter(noise, cv2.CV_32F, (1, i))
    print(np.var(noise_smoothed))

