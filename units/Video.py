import cv2
import math
import os
import logging


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

    video = cv2.VideoCapture(video)

    # 获取视频帧率
    fps = video.get(cv2.CAP_PROP_FPS)
    # 获取画面大小
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    size = (width, height)

    # 获取帧数
    frame_num = str(video.get(7))
    name = int(math.pow(10, len(frame_num)))
    ret, frame = video.read()
    while ret:
        filename = str(name) + '.png'
        absolutePath = os.path.join(path, filename)
        cv2.imwrite(absolutePath, frame)
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
    video = cv2.VideoCapture(sample)

    # 获取视频帧率
    fps = video.get(cv2.CAP_PROP_FPS)
    (folder, name) = os.path.split(avifile)
    try:
        os.makedirs(folder)
    except OSError:
        pass
    imgs = os.listdir(path)
    imgs.sort(key=lambda x: int(x[:-4]))
    name = os.path.join(path, imgs[0])
    img = cv2.imread(name)
    h, w, c = img.shape
    size = (w, h)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(avifile, fourcc, fps, size)
    for i, img in enumerate(imgs):
        img = os.path.join(path, img)
        img = cv2.imread(img)
        video_writer.write(img)
    video_writer.release()
    logging.info("success produce video {}".format(avifile))

# fps, size = frames(video="../data/invideo/2020-04-27/shu/5-3.mp4", path="../data/frame/2020-04-27/shu/5-3")
# pictrue2video(path="../data/frame/2020-04-27/shu/",avifile="../data/📛outavi/2020-04-27/shu/5.3.avi",sample="../data/invideo/2020-04-27/shu/5-3.mp4")
