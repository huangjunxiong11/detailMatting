import numpy as np
import cv2 as cv

o = cv.imread('../data/frame/2020-04-29/JX/tmp1/12.jpeg')
# o = cv.resize(o, (0, 0), fx=0.5, fy=0.5)
#
# r = cv.selectROI('input', o, False)  # 返回 (x_min, y_min, w, h)
# # roi区域
# roi = o[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
# img = o.copy()
# cv.rectangle(img, (int(r[0]), int(r[1])), (int(r[0]) + int(r[2]), int(r[1]) + int(r[3])), (255, 0, 0), 2)
# # 矩形roi
# rect = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))  # 包括前景的矩形，格式为(x,y,w,h)

orgb = cv.cvtColor(o, cv.COLOR_BGR2RGB)
mask = np.zeros(o.shape[:2], np.uint8)

bgd = np.zeros((1, 65), np.float64)
fgd = np.zeros((1, 65), np.float64)

# rect = (50, 50, 400, 500)
rect = (53, 100, 502, 842)

cv.grabCut(o, mask, rect, bgd, fgd, 5, cv.GC_INIT_WITH_RECT)
# cv.imwrite('o.jpg', o)
mask2 = cv.imread('../data/frame/2020-04-29/JX/tmp1/12mask.jpg', 0)  # 0表示将图像调整为单通道的灰度图像
mask2Show = cv.imread('../data/frame/2020-04-29/JX/tmp1/12mask.jpg', -1)  # -1表示保持源格式

m2rgb = cv.cvtColor(mask2Show, cv.COLOR_BGR2RGB)

mask[mask2 == 0] = 0
mask[mask2 == 255] = 1

mask, bgd, fgd = cv.grabCut(o, mask, None, bgd, fgd, 5, cv.GC_INIT_WITH_MASK)

mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

ogc = o * mask[:, :, np.newaxis]

ogc = cv.cvtColor(ogc, cv.COLOR_BGR2RGB)

# ogc = cv.imwrite('ogc.jpg', ogc)
cv.imshow('orgb', orgb)
cv.imshow('ogc', ogc)
cv.imshow('mask2', mask2)
cv.imshow('m2rgb', m2rgb)
cv.imshow('mask', mask)
cv.waitKey()
cv.destroyAllWindows()
