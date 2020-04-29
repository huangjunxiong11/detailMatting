import cv2 as cv
import math
import os
import logging
import numpy as np
from PIL import Image


def frames(video, path):
    """
    视频提取为图片并返回视频帧数和尺寸
    :param video: 视频文件路径”../data/invideo/2020-04-27/shu/5-3.mp4“
    :param path: 图片文件夹路径”../data/frame/2020-04-27/shu/“
    :return: fps=25, size=(720, 1280)
    """
    logging.info('start extract video {}'.format(video))
    try:
        os.makedirs(path)
    except OSError:
        pass

    video = cv.VideoCapture(video)

    # 获取视频帧率
    fps = video.get(cv.CAP_PROP_FPS)
    # 获取画面大小
    width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)

    # 获取帧数
    frame_num = str(video.get(7))
    name = int(math.pow(10, len(frame_num)))
    ret, frame = video.read()
    while ret:
        filename = str(name) + '.png'
        absolutePath = os.path.join(path, filename)
        cv.imwrite(absolutePath, frame)
        ret, frame = video.read()
        name += 1
    video.release()
    logging.info("success produce pictrue in folder {}".format(path))
    return fps, size


def pictrue2video(path, avifile, sample):
    """
    用图片生成视频
    :param path: 图片文件夹路径”../data/frame/2020-04-27/shu/“
    :param avifile: 生成视频文件”../data/📛outavi/2020-04-27/shu/5.3.avi“
    :param sample: 所参照帧数的视频“../data/invideo/2020-04-27/shu/5-3.mp4”
    :return: 无返回值
    """
    logging.info("start produce video {}".format(avifile))
    video = cv.VideoCapture(sample)

    # 获取视频帧率
    fps = video.get(cv.CAP_PROP_FPS)
    (folder, name) = os.path.split(avifile)
    try:
        os.makedirs(folder)
    except OSError:
        pass
    imgs = os.listdir(path)
    imgs.sort(key=lambda x: int(x[:-4]))
    name = os.path.join(path, imgs[0])
    img = cv.imread(name)
    h, w, c = img.shape
    size = (w, h)
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    video_writer = cv.VideoWriter(avifile, fourcc, fps, size)
    for i, img in enumerate(imgs):
        img = os.path.join(path, img)
        img = cv.imread(img)
        video_writer.write(img)
    video_writer.release()
    logging.info("success produce video {}".format(avifile))


# fps, size = frames(video="../data/invideo/2020-04-27/shu/5-3.mp4", path="../data/frame/2020-04-27/shu/5-3")
# pictrue2video(path="../data/frame/2020-04-27/shu/",avifile="../data/📛outavi/2020-04-27/shu/5.3.avi",sample="../data/invideo/2020-04-27/shu/5-3.mp4")
def setImageBg(frame, grounp, detailmask, output_dir):
    """

    :param frame: 原图路径
    :param bg: 背景图路径
    :param detailmask: 掩码路径
    :param output_dir: 输出路径
    :return:
    """
    input_dir = os.listdir(frame)
    input_dir.sort(key=lambda x: int(x[:-4]))

    detailMask = os.listdir(detailmask)
    detailMask.sort(key=lambda x: int(x[:-4]))

    try:
        os.makedirs(output_dir)
    except OSError:
        pass
    b = cv.imread(grounp)
    for i in range(len(input_dir)):
        a = os.path.join(frame, input_dir[i])
        mask = os.path.join(detailmask, detailMask[i])
        a = cv.imread(a)
        dst = cv.bitwise_and()
        save_path = "{}/{:>04d}.png".format(output_dir, i)
        cv.imwrite(save_path, dst)


if __name__ == '__main__':
    setImageBg("../data/frame/2020-04-27/shu/5-3", "../data/grounp/2020-04-27/shu/bg.jpg",
               "../data/detailmask/2020-04-27/shu/5-3", "../data/out/2020-04-27/shu/5-3")