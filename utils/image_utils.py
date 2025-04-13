import pyautogui
import time
from config import CLICK_OFFSETS, GLOBAL_REGION
from .logger import get_logger

logger = get_logger()

def find(image_path, confidence=0.8, timeout=3):
    """
    寻找并点击指定图片
    :param image_path: 图片路径
    :param confidence: 匹配精度（0.0到1.0）
    :param timeout: 超时时间（秒）
    :return: 是否找到并点击成功
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=GLOBAL_REGION)
            if location:
                return True
        except pyautogui.ImageNotFoundException as e:
            break
    return False

def find_and_click(image_path, offset_name=None, timeout=1, x_offset=0, y_offset=0, confidence=0.8):
    """
    寻找并点击指定图片
    :param image_path: 图片路径
    :param timeout: 超时时间（秒）
    :param offset_name: 预设偏移量名称
    :param x_offset: x轴偏移量（正数向右，负数向左）
    :param y_offset: y轴偏移量（正数向下，负数向上）
    :return: 是否找到并点击成功
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=GLOBAL_REGION)
            if location:
                if offset_name and offset_name in CLICK_OFFSETS:
                    x_offset, y_offset = CLICK_OFFSETS[offset_name]
                else:
                    x_offset, y_offset = 0, 0
                
                pyautogui.click(location.x + x_offset, location.y + y_offset)
                return True
        except pyautogui.ImageNotFoundException as e:
            break
    return False

def drag(
    image_path: str,
    offset: tuple[int, int],
    dx: int,
    dy: int,
    times: int = 1,
    timeout: float = 1.0,
    interval: float = 0.5
):
    """
    根据图像定位执行多次拖拽操作
    :param image_path: 基准图片路径
    :param offset: 偏移量 (x, y)
    :param dx: 水平拖拽距离（正数向右）
    :param dy: 垂直拖拽距离（正数向下）
    :param times: 拖拽次数，默认为1
    :param timeout: 查找图片超时时间
    :param interval: 拖拽间隔时间
    """
    try:
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=0.8,
            region=GLOBAL_REGION
        )
        
        if not location:
            logger.warning(f"未找到基准图片: {image_path}")
            return False

        # 计算起始坐标（应用偏移量）
        start_x = location.x + offset[0]
        start_y = location.y + offset[1]
        
        # 执行多次拖拽
        for _ in range(times):
            pyautogui.moveTo(start_x, start_y)
            pyautogui.dragRel(dx, dy, duration=timeout, button='left')
            logger.info(f"拖拽完成 [{dx},{dy}] 剩余次数: {times-_-1}")
            time.sleep(interval)
            
        return True
        
    except Exception as e:
        logger.error(f"拖拽操作异常: {str(e)}")
        return False