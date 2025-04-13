import pyautogui
import sys
from pathlib import Path
import time
import argparse
sys.path.append(str(Path(__file__).parent.parent))
from config import (CLICK_OFFSETS, GLOBAL_REGION)
from utils.logger import get_logger

logger = get_logger()

def find_image(image_path: str, confidence: float = 0.8) -> tuple:  # 添加confidence参数
    """查找图片位置
    :param confidence: 匹配精度 (0-1)，默认0.8
    """
    logger.info(f"🔍 开始查找图片 [{image_path}], confidence={confidence}")
    try:
        start_time = time.time()
        location = pyautogui.locateCenterOnScreen(image_path, region=GLOBAL_REGION, confidence=confidence)
        elapsed = round(time.time() - start_time, 2)
        
        logger.info(f"✅ 成功匹配 [{image_path}]")
        logger.debug(f"匹配耗时: {elapsed}s | 屏幕坐标: X={location.x} Y={location.y}")
        return (location.x, location.y)
    except pyautogui.ImageNotFoundException:
        logger.warning(f"❌ 图片匹配失败，可能原因：")
        logger.warning("1. 图片被遮挡或未显示在屏幕上")
        logger.warning(f"2. 图片路径错误: {image_path}")
        logger.warning("3. 屏幕分辨率与截图时不一致")
        return None
    except Exception as e:
        logger.error(f"‼️ 发生意外错误: {str(e)}")
        return None

def click_with_offset(image_path: str, offset_name: str = '', confidence: float = 0.95) -> bool:  # 新增confidence参数
    """带偏移量的点击操作
    :param confidence: 匹配精度 (0-1)，默认0.95
    """
    pos = find_image(image_path, confidence)  # 传递confidence参数
    logger.info(f"🛠️ 准备执行点击操作 [图片: {image_path}] [偏移: {offset_name or '无'}]")
    
    pos = find_image(image_path)
    if not pos:
        logger.error("⚠️ 点击操作中止：未找到目标图片")
        return False

    x, y = pos
    logger.debug(f"原始坐标获取: X={x} Y={y}")
    
    # 处理偏移量
    if offset_name:
        if offset_name not in CLICK_OFFSETS:
            logger.warning(f"⚠️ 未配置的偏移量名称: {offset_name}，将使用默认(0,0)")
        x_offset, y_offset = CLICK_OFFSETS.get(offset_name, (0, 0))
        logger.info(f"📏 应用偏移量配置 [{offset_name}]: X+{x_offset}, Y+{y_offset}")
    else:
        x_offset, y_offset = 0, 0
        logger.debug("未指定偏移量名称，使用默认坐标")

    target_x = x + x_offset
    target_y = y + y_offset
    logger.info(f"🎯 最终点击坐标: X={target_x} Y={target_y}")
    
    try:
        logger.debug("执行点击前等待 0.5 秒...")
        time.sleep(0.5)
        pyautogui.click(target_x, target_y)
        logger.info("👆 点击操作成功完成")
        return True
    except Exception as e:
        logger.error(f"‼️ 点击执行失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 修改参数解析部分
    parser = argparse.ArgumentParser(description='图像操作工具 v2.1')
    parser.add_argument('-i', '--image', required=True, help='图片路径（必须参数）')
    parser.add_argument('-o', '--offset', default='', help='偏移量名称')  # Changed to optional flag
    parser.add_argument('-c', '--confidence', type=float, default=0.8,
                      help='匹配精度 (0-1)，默认0.95')
    
    args = parser.parse_args()
    
    if args.offset:
        click_with_offset(args.image, args.offset, args.confidence)
    else:
        find_image(args.image, args.confidence)