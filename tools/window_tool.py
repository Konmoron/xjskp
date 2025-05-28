import pygetwindow as gw

# 在导入部分添加
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger


logger = get_logger()


def get_window_by_title(title: str):
    """
    获取指定标题的窗口对象
    :param title: 窗口标题
    :return: 窗口对象或None
    """
    try:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            # logger.info(f"找到窗口: {windows}")
            for window in windows:
                logger.info(f"窗口: {window}")
        else:
            logger.warning(f"没有找到标题为 '{title}' 的窗口")
    except Exception as e:
        logger.error(f"获取窗口失败: {e}")


def resize_window(title, width, height):
    """
    调整指定标题窗口的大小
    :param title: 窗口标题
    :param width: 新宽度
    :param height: 新高度
    """
    try:
        window = gw.getWindowsWithTitle(title)[0]
        logger.info(f"找到窗口: {window}")
        window.resizeTo(width, height)
        logger.info(f"调整窗口 '{title}' 大小为 {width}x{height}")
    except IndexError:
        logger.error(f"没有找到标题为 '{title}' 的窗口")
    except Exception as e:
        logger.error(f"调整窗口大小失败: {e}")


if __name__ == "__main__":
    get_window_by_title("向僵尸开炮")
    resize_window("向僵尸开炮", 420, 770)
