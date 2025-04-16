import sys
from pathlib import Path
from tracemalloc import start
sys.path.append(str(Path(__file__).parent.parent.parent))

import argparse
import time
from bottom import (
    open_jun_tuan,
    open_zhan_dou
)
from common_operations import (
   close_x,
   close_x_2,
)
from utils.image_utils import (
    find_and_click,
    find,
    drag
)
from utils.logger import get_logger

logger = get_logger()

def xuan_fu(image_path, confidence=0.8):
    """
    选择功能
    :param image_path: 功能图片路径
    :param confidence: 匹配精度
    :return: 是否切换成功
    """
    start_time = time.time()
    
    logger.info(f"🏁 启动服务器切换流程 | 目标: {image_path} | 置信度: {confidence}")

    # 打开战斗
    logger.debug("尝试打开战斗/军团界面...")
    if not open_zhan_dou() and not open_jun_tuan():
        logger.error("❌ 无法打开战斗入口，请检查游戏状态")
        return False

    # 点击头像
    time.sleep(1)
    if find_and_click('images/header.png', offset_name='header_tou_xiang'):
        logger.info("👤 头像定位成功（偏移方案：header_tou_xiang）")
        time.sleep(2)
    else:
        logger.error("❌ 头像点击失败，可能原因：\n1. 头像被遮挡\n2. offset配置错误\n3. 图像路径不存在")
        return False

    # 点击选服按钮
    if find_and_click('images/fu/xuan_fu.png'):
        time.sleep(2)
        logger.info("🚪 选服入口点击成功（图像：fu/xuan_fu.png）")
    else:
        logger.error("❌ 选服按钮未找到，可能原因：\n1. 未在游戏主界面\n2. 图像分辨率不匹配")
        return False

    drag_num = 0
    while not find(image_path, confidence=confidence):
        if drag_num >= 2:
            logger.error(f"🔄 超过最大拖拽次数（2次），未找到目标：{image_path}")
            return False

        # 向下拖拽
        if drag_num < 1:
            logger.debug(f"🔄 第{drag_num+1}次向下拖拽搜索...")
            drag('images/header.png', drag_config_name='xuan_fu_down')
        # 向上拖拽
        else:
            logger.debug(f"🔼 第{drag_num}次向上拖拽搜索...")
            drag('images/header.png', drag_config_name='xuan_fu_up')
        
        drag_num += 1
        time.sleep(2)

    if find_and_click(image_path, confidence=confidence):
        logger.info(f"✅ 成功选择服务器 | 坐标图像：{image_path}")
    else:
        logger.error(f"❌ 最终点击失败，可能原因：\n1. 图像匹配精度不足（当前：{confidence}）\n2. 元素未正确加载")
        return False

    # 等待加载完成
    logger.info("⏳ 等待服务器加载（预计8秒）...")
    time.sleep(8)

    retry_count = 0
    max_retries = 6
    while not find('images/fu/start_game.png'):
        if retry_count >= max_retries:
            logger.error(f"🛑 超过最大重试次数（{max_retries}次），启动失败")
            return False
            
        logger.warning(f"⚠️ 检测到弹窗 | 第{retry_count+1}次尝试关闭...")
        close_x()
        time.sleep(4)
        close_x_2()
        time.sleep(4)
        retry_count += 1

    logger.info(f"🎉 服务器切换成功！总耗时：{time.time() - start_time:.1f}秒")
    return True

def main():
    """
    主函数
    """
    
    parser = argparse.ArgumentParser(description='服务器切换工具')
    parser.add_argument('-i', '--image', required=True, 
                      help='目标服务器图片路径（必填）')
    parser.add_argument('-c', '--confidence', type=float, default=0.8,
                      help='图像识别置信度（0-1，默认0.8）')
    
    args = parser.parse_args()

    # 校验置信度范围
    if not 0 < args.confidence <= 1:
        print("错误：置信度必须在0到1之间")
        return

    # 执行切换操作
    if xuan_fu(args.image, args.confidence):
        print("✅ 服务器切换成功")
    else:
        print("‼️ 服务器切换失败")
        exit(1)

if __name__ == "__main__":
    main()
    
