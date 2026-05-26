#!/usr/bin/env python3
"""
工具模块
提供日志、文件处理等通用功能
"""
import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    设置并返回日志记录器

    Args:
        name: 日志记录器名称
        level: 日志级别

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    获取日志记录器（快捷方法）

    Args:
        name: 日志记录器名称

    Returns:
        日志记录器
    """
    return setup_logger(name)


def ensure_dir(path: Path) -> Path:
    """
    确保目录存在，不存在则创建

    Args:
        path: 目录路径

    Returns:
        目录路径
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_timestamp() -> str:
    """
    获取当前时间戳字符串

    Returns:
        格式化的时间戳
    """
    return datetime.now().strftime('%Y%m%d_%H%M%S')
