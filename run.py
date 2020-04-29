"""
启动函数
"""
import logging
import os
import time
from Video import frames, pictrue2video
from pictrue import matting, rudemask, rudemask2trimap, get_matting
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
    onerun()


def onerun():
    logging.info('runing')
    videoname = "data/invideo/2020-04-29/JX/tmp3.MP4"
    midir = get_dir(videoname)

    # fps, size = frames(video=videoname, path=os.path.join(frame, midir))

    framePath = os.path.join(frame, midir)
    humansegPath = os.path.join(humanseg, midir)
    rudemaskPath = os.path.join(rudemaskpath, midir)
    trimapPath = os.path.join(trimap, midir)
    detailmaskPath = os.path.join(detailmask, midir)
    resultPath = os.path.join(result, midir)

    matting(framePath, humansegPath)
    # rudemask(humansegPath, rudemaskPath)
    # rudemask2trimap(rudemaskPath, trimapPath)
    # detail_trimap(framePath, trimapPath, detailmaskPath)
    # get_matting(framePath, detailmaskPath, resultPath)

    pass


if __name__ == '__main__':
    main()
