import pyautogui
import time
import random  # 添加随机模块导入
import logging
from datetime import datetime
from config import CLICK_OFFSETS  # 新增导入
import argparse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def find(image_path, timeout=3):
    """
    寻找并点击指定图片
    :param image_path: 图片路径
    :param timeout: 超时时间（秒）
    :return: 是否找到并点击成功
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                logging.info(f"找到图片：{image_path}")
                return True
        except pyautogui.ImageNotFoundException as e:
            logging.info(f"没有找到图片：{image_path}")
            return False
            break
    logging.info(f"没有找到图片：{image_path}")
    return False

def find_and_click(image_path, offset_name=None, timeout=1, x_offset=0, y_offset=0):
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
    if offset_name and offset_name in CLICK_OFFSETS:
        x_offset, y_offset = CLICK_OFFSETS[offset_name]
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
            if location:
                pyautogui.click(location.x + x_offset, location.y + y_offset)
                return True
        except pyautogui.ImageNotFoundException as e:
            break
    return False



def is_chat_open():
    if find('images/huan_qiu/is_open_chat.png'):
        logging.info(f"聊天已经打开")
        return True
    else:
        return False

def is_chat_zhao_mu_open():
    if find('images/huan_qiu/is_open_chat_zhao_mu.png'):
        logging.info(f"招募已经打开")
        return True
    else:
        return False

def open_chat():
    if find_and_click('images/huan_qiu/header.png', offset_name='open_chat'):
        time.sleep(1)
        logging.info(f"打开聊天")
        return is_chat_open()
    else:
        logging.info(f"打开聊天失败")
        return False

def close_chat():
    # 关闭聊天
    find_and_click('images/huan_qiu/is_open_chat.png', offset_name='close_chat')
    logging.info(f" 关闭聊天")
    time.sleep(1)

def open_zhao_mu():
    if find('images/huan_qiu/chat_zhao_mu.png'):
        # 点击招募
        find_and_click('images/huan_qiu/chat_zhao_mu.png', offset_name='open_zhao_mu')
        logging.info(f"打开招募")
        time.sleep(1)
        # 再次点击招募，防止招募没点到
        find_and_click('images/huan_qiu/chat_zhao_mu.png', offset_name='open_zhao_mu')
        logging.info(f"打开招募")
        time.sleep(1)
        return True
    else:
        logging.info(f" 打开招募失败, 没找到招募按钮")
        close_chat()
        return False

def close_guan_qia_select():
    if find('images/huan_qiu/guan_qia_select.png'):
        logging.info(f"关闭-关卡-选择")
        find_and_click('images/huan_qiu/guan_qia_select_back.png', offset_name='close_guan_qia_select')
        time.sleep(1)
        return True
    else:
        return False

def close_first_charge():
    if find('images/huan_qiu/first_charge.png'):
        logging.info(f"关闭-首充")
        find_and_click('images/huan_qiu/first_charge.png', offset_name='close_first_charge')
        time.sleep(1)

def check_huan_qiu_start():
    if find("images/huan_qiu/huan_qiu_start_0.png")  or find("images/huan_qiu/huan_qiu_start_1.png")  or find("images/huan_qiu/huan_qiu_start_2.png") or find("images/huan_qiu/huan_qiu_start_3.png") or find("images/huan_qiu/huan_qiu_start_4.png"):
        logging.info(f"找到寰球图片")
        return True
    else:
        logging.info(f"未找到寰球图片")
        return False

# 选择技能的时候，有可能点不到，所以要多试几次
def close_playing_game():
    # 暂停
    logging.info(f"暂停-游戏")
    find_and_click('images/huan_qiu/header.png', x_offset=-168, y_offset=49)
    time.sleep(1)

    # 退出
    logging.info(f"关闭-游戏")
    find_and_click('images/huan_qiu/exit_playing_game.png')
    time.sleep(1)

    # 返回
    logging.info(f"返回")
    if find_and_click('images/huan_qiu/game_back.png'):
        time.sleep(1)
        return True

    return False

def close_offline():
    # 暂停
    if find('images/huan_qiu/offline.png'):
        find_and_click('images/huan_qiu/offline.png', offset_name='close_offline_offline')
        time.sleep(1)
        find_and_click('images/huan_qiu/offline_end.png', offset_name='close_offline_offline_end')
        time.sleep(1)
        return True
    return False

def close_network():
    # 暂停
    if find('images/huan_qiu/offline.png'):
        find_and_click('images/huan_qiu/network_timeout.png', offset_name='network_timeout')
        time.sleep(1)
        find_and_click('images/huan_qiu/offline_end.png', offset_name='offline_end')
        time.sleep(1)
        return True
    return False

# 选择技能
# 主要选择能量系技能，这样和枪配合，任何boss都不怕
def select_ji_neng():
    if find_and_click('images/huan_qiu/ji_guang_ji_neng.png'):
        logging.info(f"发现并选择【激光技能】 images/huan_qiu/ji_guang_ji_neng.png")
    elif find_and_click('images/huan_qiu/she_xian_ji_neng.png'):
        logging.info(f"发现并选择【射线技能】 images/huan_qiu/she_xian_ji_neng.png")

def close_ji_neng_jiao_yi():
    if find_and_click('images/huan_qiu/ji_neng_jiao_yi.png', offset_name='close_ji_neng_jiao_yi'):
        logging.info(f"发现 images/huan_qiu/ji_neng_jiao_yi.png 关闭技能交易")

def start_huan_qiu_jiu_yuan(max_num=40):
    game_num = 1
    while True:
        logging.info(f"第【{game_num}】局 - 开始执行")
        time.sleep(1)

        if game_num > max_num:
            logging.info(f"第【{game_num}】局 - 已经执行了【{max_num}】次，退出")
            break

        close_first_charge()

        if open_chat():
            if is_chat_open():
                logging.info(f"第【{game_num}】局 - 进入聊天页面")
            else:
                logging.info(f"第【{game_num}】局 - 进入聊天页面 - 失败")
                time.sleep(1)

            open_zhao_mu()

            close_first_charge()

            # 点击抢寰球
            for i in range(500):
                logging.info(f"第【{game_num}】局 - 第【{i}】次抢寰球救援")
                # 判断是否抢到，如果抢到，则退出当前循环
                if i!=0 and ( check_huan_qiu_start() or find('images/huan_qiu/play_select_skills.png') ):
                    logging.info(f"第【{game_num}】局 - 当前执行 - 抢寰球 - 抢到了")
                    break

                # 如果有 聊天框，点击聊天框
                # 1. 判断有没有招募，如果有招募，点击招募，继续抢
                # 2. 如果没有招募，说明可能已经抢到了，调到判断是否结束
                if i!=0 and i%5==0 and not is_chat_open() and not is_chat_zhao_mu_open():
                    logging.info(f"第【{game_num}】局 - 当前执行 - 点击聊天")
                    open_chat()
                    if not open_zhao_mu():
                        if close_guan_qia_select():
                            open_chat()
                            open_zhao_mu()
                        else:
                            logging.info(f"第【{game_num}】局 - 当前执行 - 抢寰球 - 打开招募失败")
                            break
                
                # 关闭远征
                if i!=0 and i%5==0:
                    if find_and_click('images/huan_qiu/yuan_zheng_fang_an.png', offset_name='close_yuan_zheng_fang_an'):
                        logging.info(f"第【{game_num}】局 - 当前执行 - 抢环球 - 关闭远征")

                if i!=0 and i%5==0 and close_guan_qia_select():
                    open_chat()
                    open_zhao_mu()

                if i!=0 and i%20==0:
                    # 每20次，关闭技能交易
                    close_ji_neng_jiao_yi()

                    # 关闭首充
                    current_hour = datetime.now().hour
                    # 只在早上执行
                    if 0 <= current_hour < 10:
                        close_first_charge()

                # 抢 20 次，判断一次
                for _ in range(20):
                    find_and_click('images/huan_qiu/chat_zhao_mu_huan_qiu_1.png')
                    time.sleep(random.uniform(0.01, 0.02))
                    find_and_click('images/huan_qiu/chat_zhao_mu_huan_qiu_2.png')

            # huan_qiu_start = False
            # 抢到寰球等待7分钟再抢
            # time.sleep(360)
            # 判断是否结束
            for i in range(120):
                # if i > 15 and not huan_qiu_start:
                #     logging.info(f"第【{game_num}】局 - 当前执行 - 判断是否寰球超过了最大次数 15 次 - 结束")
                #     # 如果超过了最大次数，说明没有抢到寰球，退出
                #     if close_playing_game():
                #         logging.info(f"第【{game_num}】局 - 当前执行 - 退出游戏")
                #         break

                # if not huan_qiu_start and check_huan_qiu_start():
                #     logging.info(f"第【{game_num}】局 - 当前执行 - 寰球 - 开始了")
                #     huan_qiu_start = True

                # 如果有 聊天框，关闭聊天框
                if i !=0 and i%5 == 0 and find('images/huan_qiu/is_open_chat.png'):
                    close_chat()
                    logging.info(f"第【{game_num}】局 - 当前执行 - 关闭聊天")
                    time.sleep(1)

                if i!=0 and i%10 == 0:
                    close_offline()

                if i !=0 and i%20 == 0:
                    current_hour = datetime.now().hour
                    # 只在早上执行
                    if 0 <= current_hour < 10:
                        close_first_charge()

                logging.info(f"第【{game_num}】局 - 等待结束 - 第【{i}】次")
                if find_and_click('images/huan_qiu/game_back.png'):
                    break
                
                # 选择技能
                select_ji_neng()

                time.sleep(10)

            game_num = game_num + 1
        else:
            logging.info("寰球救援页面未找到")
            time.sleep(1)

def test_close_first_charge():
    # 测试
    logging.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/first_charge.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["close_first_charge"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def test_close_guan_qia_select():
    # 测试
    logging.info(f"开始测试")
    
    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/guan_qia_select_back.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["close_guan_qia_select"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False
    
def test_close_chat():
    # 测试
    logging.info(f" 开始测试")
    
    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/is_open_chat.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["close_chat"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False


def test_open_zhao_mu():
    # 测试
    logging.info(f" 开始测试")

    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/chat_zhao_mu.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["open_zhao_mu"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def test_find_is_huan_qiu_start():
    # 测试
    logging.info(f"开始测试")
    if find("images/huan_qiu/huan_qiu_start_3.png") or find("images/huan_qiu/huan_qiu_start_2.png"):
        logging.info(f"找到图片")
        return True
    else:
        logging.info(f"未找到图片")
        return False

def test_open_chat():
    # 测试
    logging.info(f"开始测试")

    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/header.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["open_chat"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def test_close_offline():
    # 测试
    logging.info(f"开始测试")

    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/offline.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["close_offline_offline"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def test_close_offline_end():
    # 测试
    logging.info(f" 开始测试")

    try:
        location = pyautogui.locateCenterOnScreen("images/huan_qiu/offline_end.png", confidence=0.8)
        logging.info(f"找到图片 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS["close_offline_offline_end"]
            logging.info(f" 点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def test_find_location(image_path):
     # 测试
    logging.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        logging.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
        return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def test_click_with_offset(image_path, offset_name):
    # 测试
    logging.info(f"开始测试")
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        logging.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
        if location:
            x_offset, y_offset = CLICK_OFFSETS[offset_name]
            logging.info(f"offset_name: {offset_name} x_offset={x_offset} y_offset={y_offset}")
            logging.info(f"点击图片 location: x={location.x + x_offset} y={location.y + y_offset}")
            pyautogui.click(location.x + x_offset, location.y + y_offset)
            return True
    except pyautogui.ImageNotFoundException as e:
        logging.info(f"未找到图片, 报错: {e}")
        return False

def start():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description='寰球救援自动化脚本')
    parser.add_argument('-n', '--number', type=int, default=40, 
                        help='最大执行次数，默认100')
    args = parser.parse_args()
    logging.info(f"最大执行次数：{args.number}")
    start_huan_qiu_jiu_yuan(max_num=args.number)

def test_get_click_offset():
    image_path = "images/huan_qiu/yuan_zheng_fang_an.png"
    offset_name = "close_yuan_zheng_fang_an"
    if test_find_location(image_path):
        logging.info(f"找到图片{image_path}")
        test_click_with_offset(image_path, offset_name)

def main():
    # 调整`click`函数中的`x`和`y`坐标
    # test_get_click_offset()
    
    # 开始
    start()


if __name__ == "__main__":
    main()
