import cv2
import numpy as np
from skimage import measure,draw
from scipy import optimize,ndimage
import matplotlib.pyplot as plt
import imutils

image = cv2.imread('handtest.jpg')
image = imutils.resize(image,width = 1700)

cv2.namedWindow('Original',cv2.WINDOW_NORMAL)
cv2.imshow('Original',image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(image.shape[0], image.shape[1]) #Height = 0 , Width = 1

#image segmentation

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray,(5,5),0)

#binary threshold
_, thresh1 = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# Truncate + binary Threshold
_, thresh2 = cv2.threshold(blurred, 0, 255, cv2.THRESH_TRUNC | cv2.THRESH_OTSU)
_, thresh2 = cv2.threshold(thresh2, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

#Adaptive
area = 71
c = 4
thresh3 = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,area,c)

fig,(ax1,ax2,ax3) =plt.subplots(1,3 , figsize= (16,10))

ax1.title.set_text('binary threshold')
ax2.title.set_text('Truncate + binary threshold')
ax3.title.set_text('Adaptive')

ax1.imshow(thresh1)
ax2.imshow(thresh2)
ax3.imshow(thresh3)
plt.show()