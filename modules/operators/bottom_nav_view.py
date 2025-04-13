from datetime import datetime
import time
from utils import logger
from utils.image_utils import find, find_and_click
from utils.logger import get_logger

logger = get_logger()

def open_zhan_dou():
    if find_and_click('images/zhan_dou.png'):
        time.sleep(1)
        logger.info(f"打开战斗")
        return True
    
    return False

def open_jun_tuan():
    if find_and_click('images/jun_tuan.png'):
        time.sleep(1)
        logger.info(f"打开【军团】")
        return True

    return False

def open_shop():
    if find_and_click('images/shop.png'):
        time.sleep(1)
        logger.info(f"打开【商店】")
        return True

    return False