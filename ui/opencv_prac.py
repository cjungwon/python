import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('D:/image/opencv_logo.png')
img2 = cv2.imread('D:/image/robot.png')
img3 = cv2.imread('D:/image/messi.png')

########################################
# making borders

# BLUE = [255, 0, 0]

# replicate = cv2.copyMakeBorder(img1, 10,10,10,10, cv2.BORDER_REPLICATE)
# reflect = cv2.copyMakeBorder(img1, 10,10,10,10, cv2.BORDER_REFLECT)
# reflect101 = cv2.copyMakeBorder(img1, 10,10,10,10, cv2.BORDER_REFLECT_101)
# wrap = cv2.copyMakeBorder(img1, 10,10,10,10, cv2.BORDER_WRAP)
# constant = cv2.copyMakeBorder(img1, 10,10,10,10, cv2.BORDER_CONSTANT, value=BLUE)

# plt.subplot(2,3,1), plt.imshow(img1, 'gray'), plt.title('original'), plt.axis('off')
# plt.subplot(2,3,2), plt.imshow(replicate, 'gray'), plt.title('replicate'), plt.axis('off')
# plt.subplot(2,3,3), plt.imshow(reflect, 'gray'), plt.title('reflect'), plt.axis('off')
# plt.subplot(2,3,4), plt.imshow(reflect101, 'gray'), plt.title('reflect_101'), plt.axis('off')
# plt.subplot(2,3,5), plt.imshow(wrap, 'gray'), plt.title('wrap'), plt.axis('off')
# plt.subplot(2,3,6), plt.imshow(constant, 'gray'), plt.title('constant'), plt.axis('off')

# plt.show()


########################################
# image blending

# img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
# dst = cv2.addWeighted(img1, 0.7, img2_resized, 0.3, 0)

# cv2.imshow('dst', dst)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

########################################
# bitwise operations

# rows, cols, channels = img1.shape
# roi = img3[0:rows, 0:cols]

# img1gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# ret, mask = cv2.threshold(img1gray, 10, 255, cv2.THRESH_BINARY)
# mask_inv = cv2.bitwise_not(mask)

# img3_bg = cv2.bitwise_and(roi, roi, mask = mask_inv)

# img1_fg = cv2.bitwise_and(img1, img1, mask = mask)

# dst = cv2.add(img3_bg, img1_fg)
# img3[0:rows, 0:cols] = dst

# cv2.imshow('res', img3)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


########################################
# simple thresholding

# img = cv2.imread('D:/image/simple_threshold.png', 0)

# ret, thresh1 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
# ret, thresh2 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY_INV)
# ret, thresh3 = cv2.threshold(img, 127,255, cv2.THRESH_TRUNC)
# ret, thresh4 = cv2.threshold(img, 127,255, cv2.THRESH_TOZERO)
# ret, thresh5 = cv2.threshold(img, 127,255, cv2.THRESH_TOZERO_INV)

# titles = ['original', 'binary', 'binary_inv', 'trunc', 'tozero', 'tozero_inv']
# images = [img, thresh1, thresh2, thresh3, thresh4, thresh5]

# for i in range(6):
#     plt.subplot(2,3,i+1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])

# plt.show()


########################################
# adaptive thresholding

# img = cv2.imread('D:/image/sudoku.png', 0)
# img = cv2.medianBlur(img, 5)

# ret, th1 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
# th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
# th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# titles = ['original', 'global thresholding (v=127)', 'adaptive mean thresholding', 'adaptive gaussian thresholding']

# images = [img, th1, th2, th3]

# for i in range(4):
#     plt.subplot(2,2,i+1), plt.imshow(images[i], 'gray')
#     plt.title(titles[i])
#     plt.xticks([]), plt.yticks([])

# plt.show()


########################################
# Otsu's binarization

# img = cv2.imread('D:/image/noisy.png', 0)

# ret1, th1 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
# ret2, th2 = cv2.threshold(img, 0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# blur = cv2.GaussianBlur(img, (5,5), 0)
# ret3, th3 = cv2.threshold(blur, 0,255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# images = [img, 0, th1, 
#           img, 0, th2,
#           blur, 0, th3]

# titles = ['original noisy image', 'histogram', 'global thresholding (v=127)', 'original noisy image', 'histogram', "Otsu's thresholding", 
#             'Gaussian filtered image', 'histogram', "Otsu's thresholding"]

# for i in range(3):
#     plt.subplot(3,3,i*3+1), plt.imshow(images[i*3], 'gray')
#     plt.title(titles[i*3]), plt.xticks([]), plt.yticks([])
#     plt.subplot(3,3,i*3+2), plt.hist(images[i*3].ravel(), 256)
#     plt.title(titles[i*3+1]), plt.xticks([]), plt.yticks([])
#     plt.subplot(3,3,i*3+3), plt.imshow(images[i*3+2], 'gray')
#     plt.title(titles[i*3+2]), plt.xticks([]), plt.yticks([])

# plt.show()


########################################
# scaling

# res = cv2.resize(img3, None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)

# cv2.imshow('res', res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


########################################
# smoothing images

# kernel = np.ones((5,5), np.float32) / 25
# dst = cv2.filter2D(img1, -1, kernel)

# plt.subplot(1,2,1), plt.imshow(img1), plt.title('original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(1,2,2), plt.imshow(dst), plt.title('averaging')
# plt.xticks([]), plt.yticks([])
# plt.show()


########################################
# Gaussian Filtering

# blur = cv2.GaussianBlur(img1, (5, 5), 0)

# plt.subplot(1,2,1), plt.imshow(img1), plt.title('original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(1,2,2), plt.imshow(blur), plt.title('blurred')
# plt.xticks([]), plt.yticks([])
# plt.show()


########################################
# Median Filtering
# img = cv2.imread('D:/image/opencv_logo2.png')

# median = cv2.medianBlur(img, 5)

# plt.subplot(1,2,1), plt.imshow(img), plt.title('original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(1,2,2), plt.imshow(median), plt.title('median')
# plt.xticks([]), plt.yticks([])
# plt.show()


########################################
# erosion

# img = cv2.imread('D:/image/j.png')
# kernel = np.ones((5,5), np.uint8)
# erosion = cv2.erode(img, kernel, iterations = 2)

# plt.subplot(1,2,1), plt.imshow(img), plt.title('original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(1,2,2), plt.imshow(erosion), plt.title('erosion')
# plt.xticks([]), plt.yticks([])
# plt.show()


########################################
# sobel and Laplacian derivatives

# img = cv2.imread('D:/image/sudoku.png', 0)

# laplacian = cv2.Laplacian(img, cv2.CV_64F)
# sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
# sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

# plt.subplot(2,2,1), plt.imshow(img, cmap = 'gray'), plt.title('original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,2), plt.imshow(laplacian, cmap = 'gray'), plt.title('laplacian')
# plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,3), plt.imshow(sobel_x, cmap = 'gray'), plt.title('sobel x')
# plt.xticks([]), plt.yticks([])
# plt.subplot(2,2,4), plt.imshow(sobel_y, cmap = 'gray'), plt.title('sobel y')
# plt.xticks([]), plt.yticks([])
# plt.show()

########################################
# Canny edge detection

# img = cv2.imread('D:/image/messi.png', 0)
# edges = cv2.Canny(img, 100, 200)

# plt.subplot(1,2,1), plt.imshow(img, cmap='gray')
# plt.title('original'), plt.xticks([]), plt.yticks([])
# plt.subplot(1,2,2), plt.imshow(edges, cmap='gray')
# plt.title('edge image'), plt.xticks([]), plt.yticks([])
# plt.show()


########################################
# contours
# p.92-93

im = cv2.imread('D:/image/noisy.png')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img = cv2.drawContours(im, contours, -1, (0,255,0), 3)

plt.subplot(1,1,1), plt.imshow(img)
plt.title('original'), plt.xticks([]), plt.yticks([])
plt.show()