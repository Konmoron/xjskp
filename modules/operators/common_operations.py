from datetime import datetime
import pygetwindow as gw
from tqdm import tqdm
import time
from utils import logger
from utils.image_utils import find, find_and_click, drag, retry_click
from utils.logger import get_logger
from config import RESIZE_WINDOW_SIZE

logger = get_logger()


def is_chat_open():
    if find("images/huan_qiu/is_open_chat.png"):
        logger.info(f"聊天已经打开")
        return True
    else:
        return False


def is_chat_zhao_mu_open():
    if find("images/huan_qiu/is_open_chat_zhao_mu.png"):
        logger.info(f"招募已经打开")
        return True
    else:
        logger.info(f"没有找到招募图片 images/huan_qiu/is_open_chat_zhao_mu.png")
        return False


def open_chat():
    if find_and_click("images/header.png", offset_name="open_chat"):
        logger.info(f"打开聊天")
        return is_chat_open()
    else:
        logger.info(f"打开聊天失败")
        return False


def close_chat():
    # 关闭聊天
    find_and_click("images/huan_qiu/is_open_chat.png", offset_name="close_chat")
    logger.info(f" 关闭聊天")


def open_zhao_mu():
    if find("images/huan_qiu/chat_zhao_mu.png"):
        logger.info(f"找到招募图片，准备打开招募")
        # 点击招募
        find_and_click("images/huan_qiu/chat_zhao_mu.png", offset_name="open_zhao_mu")
        logger.info(f"第一次打开招募")
        # 再次点击招募，防止招募没点到
        find_and_click("images/huan_qiu/chat_zhao_mu.png", offset_name="open_zhao_mu")
        logger.info(f"第二次打开招募")
        return True
    else:
        logger.info(f"没有找到招募图片 images/huan_qiu/chat_zhao_mu.png")
        close_chat()
        return False


def close_guan_qia_select():
    if find("images/huan_qiu/guan_qia_select.png"):
        logger.info(f"发现-关卡-选择")
        find_and_click(
            "images/huan_qiu/guan_qia_select_back.png",
            offset_name="close_guan_qia_select",
        )
        logger.info(f"关闭-关卡-选择")
        return True
    else:
        return False


def close_first_charge():
    if find("images/huan_qiu/first_charge.png"):
        logger.info(f"发现-首充")
        find_and_click(
            "images/huan_qiu/first_charge.png", offset_name="close_first_charge"
        )
        logger.info(f"关闭-首充")
        time.sleep(1)


def check_huan_qiu_start():
    huan_qiu_kai_shi_images = [
        "images/ji_neng/qiang.png",
        "images/huan_qiu/huan_qiu_start_0.png",
        "images/huan_qiu/huan_qiu_start_1.png",
        "images/huan_qiu/huan_qiu_start_2.png",
        "images/huan_qiu/huan_qiu_start_3.png",
        "images/huan_qiu/huan_qiu_start_4.png",
        "images/huan_qiu/huan_qiu_start_5.png",
    ]

    for img in huan_qiu_kai_shi_images:
        if find(img):
            logger.info(f"找到游戏开始图片: {img}")
            return True
    logger.info(f"未找到游戏开始图片")
    return False


# # 选择技能的时候，有可能点不到，所以要多试几次
# def close_playing_game():
#     # 暂停
#     logger.info(f"暂停-游戏")
#     find_and_click('images/header.png', x_offset=-168, y_offset=49)
#     time.sleep(1)

#     # 退出
#     logger.info(f"关闭-游戏")
#     find_and_click('images/huan_qiu/exit_playing_game.png')
#     time.sleep(1)

#     # 返回
#     logger.info(f"返回")
#     if find_and_click('images/huan_qiu/game_back.png'):
#         time.sleep(1)
#         return True

#     return False


def close_offline():
    # 暂停
    if find("images/huan_qiu/offline.png"):
        logger.info(f"发现【离线】")
        find_and_click(
            "images/huan_qiu/offline.png", offset_name="close_offline_offline"
        )
        find_and_click(
            "images/huan_qiu/offline_end.png", offset_name="close_offline_offline_end"
        )
        logger.info(f"关闭【离线】")
        return True
    return False


# 选择技能
# 主要选择能量系技能，这样和枪配合，任何boss都不怕
def select_ji_neng():
    time.sleep(1)
    before_sleep = 0.01
    after_sleep = 0.01
    if find_and_click(
        "images/ji_neng/ji_guang.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【激光技能】")
        return True
    elif find_and_click(
        "images/ji_neng/she_xian.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【射线技能】")
        return True
    elif find_and_click(
        "images/ji_neng/qiang_lian_fa.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【枪-连发-技能】")
        return True
    elif find_and_click(
        "images/ji_neng/qiang_fen_lie_4.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【枪-4分裂-技能】")
        return True
    elif find_and_click(
        "images/ji_neng/qiang_fen_lie.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【枪-2分裂-技能】")
        return True
    elif find_and_click(
        "images/ji_neng/qiang_zeng_shang.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【枪-增伤-技能】")
        return True
    elif find_and_click(
        "images/ji_neng/qiang_bao_zha.png",
        before_sleep=before_sleep,
        after_sleep=after_sleep,
    ):
        logger.info(f"发现并选择【枪-爆炸-技能】")
        return True
    # elif find_and_click('images/ji_neng/wen_ya_dan_lian_fa.png'):
    #     logger.info(f"发现并选择【温压弹连发技能】images/ji_neng/wen_ya_dan_lian_fa.png")
    time.sleep(1)
    return False


def close_ji_neng_jiao_yi():
    if find_and_click(
        "images/huan_qiu/ji_neng_jiao_yi.png", offset_name="close_ji_neng_jiao_yi"
    ):
        logger.info(f"发现【技能交易】图片, 执行 - 关闭技能交易")


def close_yuan_zheng():
    # 只有 周五、周六、周日 才会出现 退出远征
    if datetime.now().weekday() > 4:
        if find_and_click(
            "images/huan_qiu/yuan_zheng_fang_an.png",
            offset_name="close_yuan_zheng_fang_an",
        ):
            logger.info(f"发现【远征方案】, 执行- 关闭远征-方案选择")

        if find_and_click(
            "images/huan_qiu/yuan_zheng.png", offset_name="close_yuan_zheng"
        ):
            logger.info(f"发现进入【远征】页面, 执行 - 关闭远征")
            time.sleep(1)

            if find_and_click(
                "images/huan_qiu/close_yuan_zheng_que_ren.png",
                offset_name="close_yuan_zheng_que_ren",
            ):
                logger.info(f"发现【确认-退出远征】按钮, 执行- 退出远征")
                time.sleep(1)

            return True
    return False


def close_guang_gao():
    logger.info(f"关闭【广告】")
    find_and_click("images/header.png", offset_name="close_guang_gao_1")


def close_chou_jiang_1():
    logger.info(f"关闭【抽奖】")
    find_and_click("images/header.png", offset_name="close_chou_jiang_1")


def _close_x():
    logger.info(f"关闭【X】")
    find_and_click("images/close_x.png", confidence=0.9)


def close_x_2():
    logger.info(f"关闭【X】")
    find_and_click("images/close_x_2.png", confidence=0.9)


def close_x():
    if find_and_click("images/xun_luo_che_ling_qu.png"):
        logger.info(f"巡逻车满了，领取奖励")
        close_chou_jiang_1()
        close_guang_gao()

    if (
        find_and_click("images/close_x.png")
        or find_and_click("images/close_x_2.png")
        or find_and_click("images/close_x_3.png")
    ):
        logger.info(f"关闭【X】")
        return True
    else:
        logger.info(f"没有找到【X】")
        return False


def close_all_x(max_attempts=6):
    """
    连续关闭所有可见的X控件

    适用于需要连续关闭多个同类弹窗的场景，例如：
    - 游戏中的多层级弹窗
    - 广告窗口连续出现

    Args:
        max_attempts (int): 最大尝试次数，避免无限循环
    """
    logger.info(f"关闭所有弹窗, 最大尝试次数: {max_attempts}")
    for i in range(max_attempts):
        logger.info(f"第 {i+1} 次尝试关闭【X】")
        if close_x():
            time.sleep(2)
            continue
        else:
            logger.info("所有弹窗关闭完毕")
            time.sleep(2)
            return


def back():
    if find_and_click("images/back.png"):
        return True

    return False


def close_all_x_and_back(max_attempts=6):
    for i in range(max_attempts):
        logger.info(f"第 {i+1} 次尝试关闭【X】并返回")
        if close_all_x():
            time.sleep(2)
            continue
        elif back():
            time.sleep(2)
            continue
        else:
            time.sleep(2)
            logger.info("所有弹窗关闭且已经返回")
            return


def kan_guang_gao(guang_gao_time=35, wait_fu_li=2):
    logger.info(f"看【广告】")
    time.sleep(guang_gao_time)
    close_guang_gao()
    time.sleep(wait_fu_li)
    close_chou_jiang_1()


def check_login_other():
    # 检查帐号在其他地方登录
    if find("images/login_other.png"):
        return True
    else:
        return False


def force_login(wait_time=10):
    # 强制登录
    if find("images/login_other.png") or find("images/force_login/start.png"):
        wait_time_seconds = wait_time * 60
        with tqdm(
            total=wait_time_seconds,
            desc="等待进度",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}s [{elapsed}<{remaining}]",
        ) as pbar:
            for _ in range(wait_time_seconds):
                time.sleep(1)
                pbar.update(1)

        retry_click(click_image="images/force_login/que_ding.png")
        time.sleep(1)
        retry_click(click_image="images/force_login/start.png")
        return True


def is_game_started():
    if find("images/header.png"):
        return True
    else:
        return False


def resize_window():
    """
    调整游戏窗口大小
    """
    logger.info("调整游戏窗口大小")
    window = gw.getWindowsWithTitle("向僵尸开炮")[0]
    if window:
        logger.info(f"找到游戏窗口: {window}")
        # 调整窗口大小
        logger.info(f"调整窗口大小为: {RESIZE_WINDOW_SIZE}")
        window.resizeTo(RESIZE_WINDOW_SIZE[0], RESIZE_WINDOW_SIZE[1])
        logger.info("游戏窗口大小调整完成")
    else:
        logger.error("未找到游戏窗口，请确保游戏已启动")


def start_game():
    """启动游戏"""
    find_and_click("images/start_game/icon.png", clicks=2)
    time.sleep(20)
    find_and_click("images/start_game/x_0.png")
    time.sleep(2)
    resize_window()
    time.sleep(10)
    find_and_click("images/header.png", image_region_name="game_start")

    logger.info("移动游戏到默认区域")
    for i in range(6):
        if not find("images/header.png", image_region_name="game_start"):
            break
        logger.info(f"第 {i+1} 次尝试移动游戏到默认区域")
        drag(
            "images/header.png",
            "move_game_to_default_region",
            image_region_name="game_start",
        )
        time.sleep(2)

    logger.info("游戏启动完成")


def exit_game():
    logger.info("退出游戏")
    find_and_click("images/exit_game.png")


def restart_game():
    logger.info("重新启动游戏")
    exit_game()
    start_game()
    close_all_x()
