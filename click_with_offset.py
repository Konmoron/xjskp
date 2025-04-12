import pyautogui
# import logger
from config import CLICK_OFFSETS

from utils.logger import get_logger

# 初始化日志
logger = get_logger()

def find_location(image_path):
    """测试查找图片位置"""
    logger.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        logger.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
        return True
    except pyautogui.ImageNotFoundException as e:
        logger.info(f"未找到图片, 报错: {e}")
        return False

def click_with_offset(image_path, offset_name=''):
    """测试带偏移量的点击"""
    logger.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        logger.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
        if location:
            if offset_name != '':
                x_offset, y_offset = CLICK_OFFSETS[offset_name]
            else:
                x_offset, y_offset = 0, 0
            logger.info(f"offset_name: {offset_name} x_offset={x_offset} y_offset={y_offset}")
            logger.info(f"点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logger.info(f"未找到图片, 报错: {e}")
        return False

def get_click_offset(image_path, offset_name=''):
    """测试获取点击偏移量"""
    if find_location(image_path):
        logger.info(f"找到图片{image_path}")
        click_with_offset(image_path, offset_name)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使用方法: python click_with_offset.py 图片路径 [偏移量名称]")
        sys.exit(1)
        
    image_path = sys.argv[1]
    offset_name = sys.argv[2] if len(sys.argv) > 2 else ''

    # 打印配置信息
    logger.info(f"图片路径: {image_path}")
    logger.info(f"偏移量名称: {offset_name}")
    logger.info(f"偏移量配置: {CLICK_OFFSETS}")
    
    if find_location(image_path):
        logger.info(f"找到图片{image_path}")
        click_with_offset(image_path, offset_name)