import paddlehub as hub
import os
import cv2 as cv
import random
import numpy as np


def matting(input_dir, output_dir):
    """
    对帧图片进行批量抠图
    :param input_dir: 帧的路径例如'../data/frame/2020-04-27/shu/'
    :param output_dir: 输出路径例如'../data/humanseg/2020-04-27/shu'
    :return: 无返回值
    """
    humanseg = hub.Module(name='deeplabv3p_xception65_humanseg')
    files = [input_dir + i for i in os.listdir(input_dir)]
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    humanseg.segmentation(data={'image': files}, output_dir=output_dir)  # 抠图


# matting('../data/frame/2020-04-27/shu/', '../data/humanseg/2020-04-27/shu')


def rudemask(input_dir, output_dir):
    """
    获取图片第四透明通道
    :param input_dir:
    :param output_dir:
    :return:
    """
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]

    for i, file in enumerate(files):
        img = cv.imread(file, -1)
        rgba = cv.split(img)[3]
        ori_name = os.path.basename(file)
        # save_name = os.path.splitext(ori_name)[0] + ".png"
        save_path = os.path.join(output_dir, ori_name)
        cv.imwrite(save_path, rgba)


# rudemask('../data/humanseg/2020-04-27/shu', '../data/rudemask/2020-04-27/shu')


def rudemask2trimap(input_dir, output_dir):
    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    files = [os.path.join(input_dir, i) for i in os.listdir(input_dir)]

    for i, file in enumerate(files):
        alpha = cv.imread(file)
        k_size = random.choice(range(1, 5))
        iterations = np.random.randint(1, 20)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (k_size, k_size))
        dilated = cv.dilate(alpha, kernel, iterations)
        eroded = cv.erode(alpha, kernel, iterations)
        trimap = np.zeros(alpha.shape)
        trimap.fill(128)
        trimap[eroded >= 255] = 255
        trimap[dilated <= 0] = 0
        ori_name = os.path.basename(file)
        # save_name = os.path.splitext(ori_name)[0] + ".png"
        save_path = os.path.join(output_dir, ori_name)
        cv.imwrite(save_path, trimap)


# rudemask2trimap('../data/rudemask/2020-04-27/shu', '../data/trimap/2020-04-27/shu')
