"""
启动函数
"""
import logging
import os
import time
from Video import frames, pictrue2video
from pictrue import matting, rudemask, rudemask2trimap
from eval import detail_trimap
from file import get_dir
from config import invideo, frame, humanseg, rudemaskpath, trimap, detailmask, result


# 日志格式编辑
def console_out(filename):
    logging.basicConfig(
        level=logging.INFO,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename=filename,  # log文件名
        filemode='w')  # 写入模式“w”或“a”


def main():
    logPath = 'log'
    try:
        os.makedirs(logPath)
    except OSError:
        pass
    filename = logPath + '/' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.log'
    console_out(filename=filename)
    run()


def run():
    logging.info('runing')
    videoname = "../data/invideo/2020-04-27/shu/5-3.mp4"
    midir = get_dir(videoname)
    fps, size = frames(video=videoname, path=os.path.join(frame, midir))
    matting(os.path.join(frame, midir), os.path.join(humanseg, midir))
    rudemask(os.path.join(humanseg, midir), os.path.join(rudemaskpath, midir))
    rudemask2trimap(os.path.join(rudemaskpath, midir), os.path.join(trimap, midir))
    detail_trimap(os.path.join(frame, midir), os.path.join(trimap, midir),
                  os.path.join(detailmask, midir))
    pass


if __name__ == '__main__':
    main()
