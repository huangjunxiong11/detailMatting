import glob
import os
import time


def read_file(path):
    """
    返回类别与对应视频字典
    :param path: 路径，例如‘../data/invideo’
    :return: 字典
    """
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    dirtoday = os.path.join(path, today)
    classdir = os.listdir(dirtoday)
    csv = {}
    for i, dir in enumerate(classdir):
        dirs = os.path.join(dirtoday, dir)
        mp4s = []
        mp4s += glob.glob(os.path.join(dirtoday, dir, '*.mp4'))
        mp4s += glob.glob(os.path.join(dirtoday, dir, '*.avi'))
        mp4s += glob.glob(os.path.join(dirtoday, dir, '*.mov'))
        csv[dirs] = mp4s
    return csv


def get_dir(mp4):
    """
    求得相应的输入目录
    :param mp4: 路径，例如‘"../data/invideo/2020-04-27/shu/5-3.mp4"’
    :return:例如'2020-04-27/shu/5-3'
    """
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    (dir, filename) = os.path.split(mp4)
    shu_heng = dir.split('/')[-1]
    name5_3 = filename.split('.')[0]
    path = os.path.join(today, shu_heng, name5_3)
    return path



get_dir("../data/invideo/2020-04-27/shu/5-3.mp4")














# csv = read_file('../data/invideo/')
