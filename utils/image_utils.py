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
    x_offset: int,
    y_offset: int,
    drag_x: int,
    drag_y: int,
    times: int = 1,
    duration: float = 1,
    confidence: float = 0.8
):
    """
    根据图像定位执行多次拖拽操作
    :param image_path: 基准图片路径
    :param x_offset: 基准图片相对于屏幕左上角的x偏移量
    :param y_offset: 基准图片相对于屏幕左上角的y偏移量
    :param drag_x: 水平拖拽距离（正数向右）
    :param drag_y: 垂直拖拽距离（正数向下）
    :param times: 拖拽次数，默认为1
    :param duration: 查找图片超时时间
    :param confidence: 匹配精度
    """
    try:
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=confidence,
            region=GLOBAL_REGION
        )
        
        if not location:
            logger.warning(f"未找到基准图片: {image_path}")
            return False

        # 计算起始坐标（应用偏移量）
        start_x = location.x + x_offset
        start_y = location.y + y_offset
        
        # 执行多次拖拽
        for i in range(times):
            logger.info(f"开始第{i+1}次拖拽 [{drag_x},{drag_y}]")
            pyautogui.moveTo(start_x, start_y)
            time.sleep(1)
            pyautogui.dragRel(drag_x, drag_y, duration=duration, button='left')
            logger.info(f"第{i+1}拖拽完成 [{drag_x},{drag_y}]")
            time.sleep(1)
            
        return True
        
    except Exception as e:
        logger.error(f"拖拽操作异常: {str(e)}")
        return False