import cv2
import numpy as np
from matplotlib import pyplot as plt

# img1 = cv2.imread('D:/image/opencv_logo.png')
# img2 = cv2.imread('D:/image/robot.png')
# img3 = cv2.imread('D:/image/messi.png')

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

img = cv2.imread('D:/image/sudoku.png', 0)
img = cv2.medianBlur(img, 5)

ret, th1 = cv2.threshold(img, 127,255, cv2.THRESH_BINARY)
th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

titles = ['original', 'global thresholding (v=127)', 'adaptive mean thresholding', 'adaptive gaussian thresholding']

images = [img, th1, th2, th3]

for i in range(4):
    plt.subplot(2,2,i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])

plt.show()


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
# perspective transformation

# img = cv2.imread('D:/image/sudoku.png')
# row, cols, ch = img.shape

# pts1 = np.float32([ [48, 56], [330, 44], [20, 349], [350, 346] ])
# pts2 = np.float32([ [0, 0], [300, 0], [0, 300], [300, 300] ])

# M = cv2.getPerspectiveTransform(pts1, pts2)

# dst = cv2.warpPerspective(img, M, (300, 300))

# plt.subplot(1,2,1), plt.imshow(img), plt.title('input')
# plt.subplot(1,2,2), plt.imshow(dst), plt.title('output')
# plt.show()

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

# im = cv2.imread('D:/image/noisy.png')
# imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# img = cv2.drawContours(im, contours, -1, (0,0,255), 3)

# plt.subplot(1,1,1), plt.imshow(img)
# plt.title('original'), plt.xticks([]), plt.yticks([])
# plt.show()


########################################
# template matching

# img = cv2.imread('D:/image/messi.png', 0)
# img2 = img.copy()
# template = cv2.imread('D:/image/messi_face.png', 0)

# w, h = template.shape[::-1]

# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# for meth in methods:
#     img = img2.copy()
#     method = eval(meth)

#     res = cv2.matchTemplate(img, template, method)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

#     if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#         top_left = min_loc
#     else:
#         top_left = max_loc
    
#     bottom_right = (top_left[0] + w, top_left[1] + h)

#     cv2.rectangle(img, top_left, bottom_right, 255, 2)

#     plt.subplot(1,2,1), plt.imshow(res, cmap='gray')
#     plt.title('matching result'), plt.xticks([]), plt.yticks([])
#     plt.subplot(1,2,2), plt.imshow(img, cmap='gray')
#     plt.title('detected point'), plt.xticks([]), plt.yticks([])
#     plt.suptitle(meth)

#     plt.show()


########################################
# template matching with multiple objects

# img_rgb = cv2.imread('D:/image/mario.png')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('D:/image/mario_coin.png', 0)
# w, h = template.shape[::-1]

# res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
# threshold = 0.8

# loc = np.where(res >= threshold)
# for pt in zip(*loc[::-1]):
#     cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

# cv2.imshow('res', img_rgb)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


########################################
# hough transform

# img = cv2.imread('D:/image/sudoku.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# lines = cv2.HoughLines(edges, 1, np.pi/180, 150)
# for line in lines:
#     rho, theta = line[0]
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a * rho
#     y0 = b * rho
#     x1 = int(x0 + 1000 * (-b))
#     y1 = int(y0 + 1000 * (a))
#     x2 = int(x0 - 1000 * (-b))
#     y2 = int(y0 - 1000 * (a))

#     cv2.line(img, (x1, y1), (x2, y2), (0,0,255), 2)

# cv2.imshow('edges', edges)
# cv2.imshow('houghlines', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


########################################
# probabilistic hough transform

# img = cv2.imread('D:/image/sudoku.png')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)
# minLineLength = 100
# maxLineGap = 10

# lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     cv2.line(img, (x1, y1), (x2, y2), (0,255,0), 2)

# cv2.imshow('houghline', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


########################################
# hough circle transform

# img = cv2.imread('D:/image/opencv_logo.png', 0)
# img = cv2.medianBlur(img, 5)
# cimg = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

# circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 50, param1=50, param2=30, minRadius=0, maxRadius=0)

# circles = np.uint16(np.around(circles))
# for i in circles[0, :]:
#     cv2.circle(cimg, (i[0], i[1]), i[2], (0,255,0), 2)
#     cv2.circle(cimg, (i[0], i[1]), 3, (0,0,255), 3)

# cv2.imshow('detected circles', cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()