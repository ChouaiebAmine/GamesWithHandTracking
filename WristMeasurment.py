import cv2
import numpy as np

image= cv2.imread('handtest.jpg',cv2.IMREAD_GRAYSCALE)

blurred_image = cv2.GaussianBlur(image,(5,5),0)
edges = cv2.Canny(blurred_image,50,60)

cv2.imshow('Edges',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()