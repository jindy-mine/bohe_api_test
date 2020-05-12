"""
=========================================
Author:薄咊
Time:2020/3/13  11:27
==========================================
"""
import logging
from common.handle_path import LOG_FILENAME


class HandleLogger:
    """处理日志相关模块"""

    @staticmethod
    def create_logger():
        """
        创建日志收集器
        :return: 日志收集器
        """
        # 第一步：创建一个日志收集器
        log = logging.getLogger("bohe")

        # 第二步：设置收集器收集的等级:debug等级
        log.setLevel("DEBUG")

        # 第三步：设置输出渠道以及输出渠道的等级：输出到日志文件中，输出INFO等级及以上等级的日志
        fh = logging.FileHandler(LOG_FILENAME, encoding="utf8")
        fh.setLevel("DEBUG")
        log.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setLevel("DEBUG")
        log.addHandler(sh)

        # 第四步：设置输出格式
        formats = '%(asctime)s -- [%(filename)s-->line:%(lineno)d] - %(levelname)s: %(message)s'
        # 创建一个输出格式对象
        form = logging.Formatter(formats)
        # 将输出格式添加到输出渠道
        fh.setFormatter(form)
        sh.setFormatter(form)

        return log


log = HandleLogger.create_logger()
