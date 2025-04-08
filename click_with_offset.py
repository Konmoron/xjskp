import pyautogui
import logging
from config import CLICK_OFFSETS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def find_location(image_path):
    """测试查找图片位置"""
    logging.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        logging.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
        return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def click_with_offset(image_path, offset_name=''):
    """测试带偏移量的点击"""
    logging.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        logging.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
        if location:
            if offset_name != '':
                x_offset, y_offset = CLICK_OFFSETS[offset_name]
            else:
                x_offset, y_offset = 0, 0
            logging.info(f"offset_name: {offset_name} x_offset={x_offset} y_offset={y_offset}")
            logging.info(f"点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def get_click_offset(image_path, offset_name=''):
    """测试获取点击偏移量"""
    if find_location(image_path):
        logging.info(f"找到图片{image_path}")
        click_with_offset(image_path, offset_name)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使用方法: python tools/click_with_offset.py 图片路径 [偏移量名称]")
        sys.exit(1)
        
    image_path = sys.argv[1]
    offset_name = sys.argv[2] if len(sys.argv) > 2 else ''

    # 打印配置信息
    logging.info(f"图片路径: {image_path}")
    logging.info(f"偏移量名称: {offset_name}")
    logging.info(f"偏移量配置: {CLICK_OFFSETS}")
    
    if find_location(image_path):
        logging.info(f"找到图片{image_path}")
        click_with_offset(image_path, offset_name)