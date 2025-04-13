import logging
import sys
from typing import Optional

def get_logger(name: Optional[str] = None):
    """
    获取配置好的logger对象
    :param name: 模块名称 (默认使用调用模块的__name__)
    """
    logger = logging.getLogger(name or sys._getframe(1).f_globals['__name__'])
    
    # 避免重复添加handler
    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        
        logger.propagate = False
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    
    return logger