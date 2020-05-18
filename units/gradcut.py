import cv2 as cv
import numpy as np

src = cv.imread("../data/frame/2020-04-29/JX/tmp1/12.jpeg")
src = cv.resize(src, (0, 0), fx=0.5, fy=0.5)
r = cv.selectROI('input', src, False)  # 返回 (x_min, y_min, w, h)

# roi区域
roi = src[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
img = src.copy()
cv.rectangle(img, (int(r[0]), int(r[1])), (int(r[0]) + int(r[2]), int(r[1]) + int(r[3])), (255, 0, 0), 2)

# 原图mask
mask = np.zeros(src.shape[:2], dtype=np.uint8)
mask1 = cv.imread('../data/frame/2020-04-29/JX/tmp1/11111.jpg', 0)  # 0表示将图像调整为单通道的灰度图像
mask1 = cv.resize(mask1, (0, 0), fx=0.5, fy=0.5)

mask[mask1 == 0] = 0
mask[mask1 == 255] = 1

# 矩形roi
rect = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))  # 包括前景的矩形，格式为(x,y,w,h)

bgdmodel = np.zeros((1, 65), np.float64)  # bg模型的临时数组  13 * iterCount
fgdmodel = np.zeros((1, 65), np.float64)  # fg模型的临时数组  13 * iterCount

# cv.grabCut(src, mask, rect, bgdmodel, fgdmodel, 11, mode=cv.GC_INIT_WITH_RECT)
mask, bgd, fgd = cv.grabCut(src, mask, None, bgdmodel, fgdmodel, 5, cv.GC_INIT_WITH_MASK)

# 提取前景和可能的前景区域
mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
background = cv.imread("../data/frame/2020-04-29/JX/tmp1/3.jpeg")

h, w, ch = src.shape
background = cv.resize(background, (w, h))
cv.imwrite("../data/gradcut/backgrounp/backgrounp-100000.png", background)

mask = np.zeros(src.shape[:2], dtype=np.uint8)
bgdmodel = np.zeros((1, 65), np.float64)
fgdmodel = np.zeros((1, 65), np.float64)

cv.grabCut(src, mask, rect, bgdmodel, fgdmodel, 5, mode=cv.GC_INIT_WITH_RECT)
mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')

# 高斯模糊
se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
cv.dilate(mask2, se, mask2)
mask2 = cv.GaussianBlur(mask2, (5, 5), 0)
cv.imshow('background-mask', mask2)
cv.imwrite('../data/gradcut/mask2/100000.png', mask2)

# 虚化背景
background = cv.GaussianBlur(background, (0, 0), 15)
mask2 = mask2 / 255.0
a = mask2[..., None]

# 融合方法 com = a*fg + (1-a)*bg
result = a * (src.astype(np.float32)) + (1 - a) * (background.astype(np.float32))

cv.imshow("result", result.astype(np.uint8))
cv.imwrite("../data/gradcut/result/result-100000.png", result.astype(np.uint8))

cv.waitKey(0)
cv.destroyAllWindows()
