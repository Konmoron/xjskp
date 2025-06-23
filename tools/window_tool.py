import pygetwindow as gw
import time

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


def close_window(title):
    """
    关闭指定标题的窗口
    :param title: 窗口标题
    """
    try:
        window = gw.getWindowsWithTitle(title)[0]
        logger.info(f"找到窗口: {window}")
        window.close()
        logger.info(f"关闭窗口 '{title}'")
    except IndexError:
        logger.error(f"没有找到标题为 '{title}' 的窗口")
    except Exception as e:
        logger.error(f"关闭窗口失败: {e}")


def show_window(title):
    """
    显示指定标题的窗口
    :param title: 窗口标题
    """
    try:
        window = gw.getWindowsWithTitle(title)[0]
        logger.info(f"找到窗口: {window}")
        window.activate()
        window.show()
        window.restore()
        logger.info(f"激活窗口 '{title}'")
    except IndexError:
        logger.error(f"没有找到标题为 '{title}' 的窗口")
    except Exception as e:
        logger.error(f"激活窗口失败: {e}")


def minimize_window(title):
    """
    隐藏指定标题的窗口
    :param title: 窗口标题
    """
    try:
        window = gw.getWindowsWithTitle(title)[0]
        logger.info(f"找到窗口: {window}")
        window.minimize()
        time.sleep(1)
        window.hide()
        logger.info(f"隐藏窗口 '{title}'")
        # window.restore()  # 恢复窗口状态
        # logger.info(f"恢复窗口 '{title}'")
        time.sleep(1)
        window.close()
        logger.info(f"关闭窗口 '{title}'")
    except IndexError:
        logger.error(f"没有找到标题为 '{title}' 的窗口")
    except Exception as e:
        logger.error(f"隐藏窗口失败: {e}")


if __name__ == "__main__":
    get_window_by_title("向僵尸开炮")
    # resize_window("向僵尸开炮", 420, 770)
    close_window("向僵尸开炮")

    time.sleep(2)

    get_window_by_title("腾讯应用宝")
    minimize_window("腾讯应用宝")
    time.sleep(2)
    # show_window("腾讯应用宝")
    # close_window("腾讯应用宝")
