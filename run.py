"""
启动函数
"""
import logging
import os
import time


# 日志格式编辑
def console_out(logFilename):
    logging.basicConfig(
        level=logging.INFO,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename=logFilename,  # log文件名
        filemode='w')  # 写入模式“w”或“a”


def main():
    logPath = 'log'
    try:
        os.makedirs(logPath)
    except OSError:
        pass
    logFilename = logPath + '/' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()) + '.log'
    console_out(logFilename=logFilename)
    run()


def run():
    logging.info('nice')
    pass


if __name__ == '__main__':
    main()
