import cv2
import numpy as np

img = cv2.imread('D:/image/sample01.png')

px = img[100, 100]
print(px)

blue = img[100, 100, 0]
print(blue)

print(img.item(10,10,2))

print(img.dtype)
