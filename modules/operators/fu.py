# import sys
# from pathlib import Path
# from tracemalloc import start
# sys.path.append(str(Path(__file__).parent.parent.parent))

import argparse
import time
from modules.operators.bottom import open_jun_tuan, open_zhan_dou
from modules.operators.common_operations import (
    close_all_x,
    close_all_x_and_back,
)
from utils.image_utils import find_and_click, find, drag, retry_click
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

    logger.info("关闭所有X，并返回")
    close_all_x_and_back()

    # 打开战斗
    logger.info("尝试打开战斗/军团界面...")
    if open_zhan_dou():
        logger.info("✅ 战斗已打开")
    elif open_jun_tuan():
        logger.info("✅ 军团已打开")

    if retry_click(
        click_image="images/header.png",
        success_image="images/fu/xuan_fu.png",
        click_kwargs={"offset_name": "header_tou_xiang"},
    ):
        logger.info("👤 发现选服按钮，头像点击成功（偏移方案：header_tou_xiang）")
    else:
        logger.error(
            "❌ 头像点击失败，可能原因：\n1. 头像被遮挡\n2. offset配置错误\n3. 图像路径不存在"
        )
        close_all_x()
        return False

    # 点击选服按钮
    # 重试6次
    if retry_click(click_image="images/fu/xuan_fu.png"):
        logger.info("🚪 选服点击成功（图像：fu/xuan_fu.png）")
    else:
        logger.error(
            "❌ 选服按钮未找到，可能原因：\n1. 未在游戏主界面\n2. 图像分辨率不匹配"
        )
        close_all_x()
        return False

    drag_num = 0
    while not find(image_path, confidence=confidence):
        if drag_num >= 2:
            logger.error(f"🔄 超过最大拖拽次数（2次），未找到目标：{image_path}")
            return False

        # 向下拖拽
        if drag_num < 1:
            logger.debug(f"🔄 第{drag_num+1}次向下拖拽搜索...")
            drag("images/header.png", drag_config_name="xuan_fu_down")
        # 向上拖拽
        else:
            logger.debug(f"🔼 第{drag_num}次向上拖拽搜索...")
            drag("images/header.png", drag_config_name="xuan_fu_up")

        drag_num += 1
        time.sleep(2)

    # 为了解决点击之后，没有响应，需要增加重试逻辑，重试6次
    if retry_click(
        click_image=image_path,
        click_kwargs={"confidence": confidence},
        find_kwargs={"confidence": confidence},
    ):
        logger.info(f"✅ 成功选择服务器 | 坐标图像：{image_path}")
    else:
        logger.error(
            f"❌ 最终点击{image_path}失败，可能原因：\n1. 图像匹配精度不足（当前：{confidence}）\n2. 元素未正确加载"
        )
        close_all_x()
        return False

    # 等待加载完成
    logger.info("⏳ 等待服务器加载（预计10秒）...")
    time.sleep(10)

    logger.info("关闭所有X")
    close_all_x()

    logger.info(f"🎉 {image_path}服切换成功！总耗时：{time.time() - start_time:.1f}秒")
    return True


def main():
    """
    服务器切换工具主入口

    参数说明：
    -i/--image     必需参数，指定目标服务器的图片路径（支持相对/绝对路径）
    -c/--confidence 可选参数，设置图像识别置信度阈值（0.5~1.0，默认0.8）

    使用示例：
    1. 基本用法：
       python.exe -m modules.operators.fu -i "images/fu/server_123.png"

    2. 指定置信度：
       python.exe -m modules.operators.fu -i "images\fu\server_456.png" -c 0.9

    3. 查看帮助：
       python.exe -m modules.operators.fu -h

    注意事项：
    • 图片路径需使用正斜杠（/）或双反斜杠（\）
    • 置信度过低可能导致误匹配，建议不低于0.9
    • 运行时需保持游戏窗口在前台可见
    """

    parser = argparse.ArgumentParser(description="服务器切换工具")
    parser.add_argument(
        "-i", "--image", required=True, help="目标服务器图片路径（必填）"
    )
    parser.add_argument(
        "-c",
        "--confidence",
        type=float,
        default=0.8,
        help="图像识别置信度（0-1，默认0.8）",
    )

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
