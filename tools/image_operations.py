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

def click_with_offset(image_path: str, offset_name: str = '', confidence: float = 0.8) -> bool:  # 新增confidence参数
    """带偏移量的点击操作
    :param confidence: 匹配精度 (0-1)，默认0.8
    """
    pos = find_image(image_path, confidence)  # 传递confidence参数
    logger.info(f"🛠️ 准备执行点击操作 [图片: {image_path}] [偏移: {offset_name or '无'}]")

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

def calculate_offset(image_path: str, confidence: float = 0.8) -> tuple:
    """计算图片位置与点击位置的偏移量"""
    logger.info(f"🛠️ 开始计算偏移量 [图片: {image_path}]")
    
    # 查找基准图片
    base_pos = find_image(image_path, confidence)
    if not base_pos:
        logger.error("无法计算偏移：未找到基准图片")
        return None
        
    logger.info("🖱️ 请在10秒内将鼠标移动到目标位置...")
    time.sleep(10)
    
    # 获取目标位置
    target_x, target_y = pyautogui.position()
    logger.info(f"📌 记录目标位置: X={target_x} Y={target_y}")
    
    # 计算偏移量
    offset = (target_x - base_pos[0], target_y - base_pos[1])
    logger.info(f"⚖️ 计算偏移量完成: X={offset[0]} Y={offset[1]}")
    logger.info(f"✅ 偏移量配置: ({offset[0]}, {offset[1]})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='图像操作工具 v2.2', formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', required=True, help='操作模式')
    
    # 查找模式
    find_parser = subparsers.add_parser('find', help='查找图片位置')
    find_parser.add_argument('-i', '--image', required=True, help='图片路径')
    find_parser.add_argument('-c', '--confidence', type=float, default=0.8,
                           help='匹配精度 (0-1，默认0.8)')

    # 点击模式
    click_parser = subparsers.add_parser('click', help='执行点击操作')
    click_parser.add_argument('-i', '--image', required=True, help='图片路径')
    click_parser.add_argument('-o', '--offset', default='', help='偏移量名称')
    click_parser.add_argument('-c', '--confidence', type=float, default=0.8,
                           help='匹配精度 (0-1，默认0.8)')

    # 新增偏移计算模式
    offset_parser = subparsers.add_parser('get-offset', help='计算偏移量')
    offset_parser.add_argument('-i', '--image', required=True, 
                             help='基准图片路径')
    offset_parser.add_argument('-c', '--confidence', type=float, default=0.8,
                             help='匹配精度 (0-1，默认0.8)')

    args = parser.parse_args()

    if args.command == 'find':
        find_image(args.image, args.confidence)
    elif args.command == 'click':
        click_with_offset(args.image, args.offset, args.confidence)
    elif args.command == 'get-offset':
        calculate_offset(args.image, args.confidence)
