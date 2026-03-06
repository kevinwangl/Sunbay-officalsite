import logging
import sys

def setup_logger(name: str = "sunbay") -> logging.Logger:
    """配置日志器"""
    logger = logging.getLogger(name)
    
    if logger.handlers:  # 避免重复配置
        return logger
    
    # 延迟导入避免循环依赖
    try:
        from .config import settings
        log_level = getattr(logging, settings.LOG_LEVEL, logging.INFO)
    except:
        log_level = logging.INFO
    
    logger.setLevel(log_level)
    
    # 控制台输出
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    
    # 格式：时间 | 级别 | 模块 | 消息
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-7s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# 全局日志器
logger = setup_logger()
