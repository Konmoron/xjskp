from datetime import datetime
import time
from utils import logger
from utils.image_utils import find, find_and_click
from utils.logger import get_logger

logger = get_logger()

def is_chat_open():
    if find('images/huan_qiu/is_open_chat.png'):
        logger.info(f"聊天已经打开 images/huan_qiu/is_open_chat.png")
        return True
    else:
        return False

def is_chat_zhao_mu_open():
    if find('images/huan_qiu/is_open_chat_zhao_mu.png'):
        logger.info(f"招募已经打开 images/huan_qiu/is_open_chat_zhao_mu.png")
        return True
    else:
        return False

def open_chat():
    if find_and_click('images/huan_qiu/header.png', offset_name='open_chat'):
        time.sleep(1)
        logger.info(f"打开聊天")
        return is_chat_open()
    else:
        logger.info(f"打开聊天失败")
        return False

def close_chat():
    # 关闭聊天
    find_and_click('images/huan_qiu/is_open_chat.png', offset_name='close_chat')
    logger.info(f" 关闭聊天")
    time.sleep(1)

def open_zhao_mu():
    if find('images/huan_qiu/chat_zhao_mu.png'):
        logger.info(f"找到招募图片，招募已经打开 images/huan_qiu/chat_zhao_mu.png")
        # 点击招募
        find_and_click('images/huan_qiu/chat_zhao_mu.png', offset_name='open_zhao_mu')
        logger.info(f"第一次打开招募")
        time.sleep(1)
        # 再次点击招募，防止招募没点到
        find_and_click('images/huan_qiu/chat_zhao_mu.png', offset_name='open_zhao_mu')
        logger.info(f"第二次打开招募")
        time.sleep(0.5)
        return True
    else:
        logger.info(f"没有找到招募图片 images/huan_qiu/chat_zhao_mu.png")
        close_chat()
        return False

def close_guan_qia_select():
    if find('images/huan_qiu/guan_qia_select.png'):
        logger.info(f"发现-关卡-选择 images/huan_qiu/guan_qia_select.png")
        find_and_click('images/huan_qiu/guan_qia_select_back.png', offset_name='close_guan_qia_select')
        logger.info(f"关闭-关卡-选择 images/huan_qiu/guan_qia_select_back.png")
        time.sleep(1)
        return True
    else:
        return False

def close_first_charge():
    if find('images/huan_qiu/first_charge.png'):
        logger.info(f"发现-首充 images/huan_qiu/first_charge.png")
        find_and_click('images/huan_qiu/first_charge.png', offset_name='close_first_charge')
        logger.info(f"关闭-首充 images/huan_qiu/first_charge.png")
        time.sleep(1)

def check_huan_qiu_start():
    huan_qiu_kai_shi_images = [
        "images/huan_qiu/huan_qiu_start_0.png",
        "images/huan_qiu/huan_qiu_start_1.png",
        "images/huan_qiu/huan_qiu_start_2.png",
        "images/huan_qiu/huan_qiu_start_3.png",
        "images/huan_qiu/huan_qiu_start_4.png"
    ]
    
    for img in huan_qiu_kai_shi_images:
        if find(img):
            logger.info(f"找到寰球开始图片: {img}")
            return True
    logger.info(f"未找到寰球开始图片")
    return False

# 选择技能的时候，有可能点不到，所以要多试几次
def close_playing_game():
    # 暂停
    logger.info(f"暂停-游戏")
    find_and_click('images/huan_qiu/header.png', x_offset=-168, y_offset=49)
    time.sleep(1)

    # 退出
    logger.info(f"关闭-游戏")
    find_and_click('images/huan_qiu/exit_playing_game.png')
    time.sleep(1)

    # 返回
    logger.info(f"返回")
    if find_and_click('images/huan_qiu/game_back.png'):
        time.sleep(1)
        return True

    return False

def close_offline():
    # 暂停
    if find('images/huan_qiu/offline.png'):
        logger.info(f"发现【离线】images/huan_qiu/offline.png")
        find_and_click('images/huan_qiu/offline.png', offset_name='close_offline_offline')
        time.sleep(1)
        find_and_click('images/huan_qiu/offline_end.png', offset_name='close_offline_offline_end')
        time.sleep(1)
        logger.info(f"关闭【离线】images/huan_qiu/offline_end.png")
        return True
    return False

# 选择技能
# 主要选择能量系技能，这样和枪配合，任何boss都不怕
def select_ji_neng():
    if find_and_click('images/ji_neng/ji_guang.png'):
        logger.info(f"发现并选择【激光技能】images/ji_neng/ji_guang.png")
    elif find_and_click('images/ji_neng/she_xian.png'):
        logger.info(f"发现并选择【射线技能】images/ji_neng/she_xian_ji_neng.png")
    elif find_and_click('images/ji_neng/qiang_lian_fa.png'):
        logger.info(f"发现并选择【枪-连发-技能】images/ji_neng/qiang_lian_fa.png")
    elif find_and_click('images/ji_neng/qiang_fen_lie_4.png'):
        logger.info(f"发现并选择【枪-4分裂-技能】images/ji_neng/qiang_fen_lie_4.png")
    elif find_and_click('images/ji_neng/qiang_fen_lie.png'):
        logger.info(f"发现并选择【枪-2分裂-技能】images/ji_neng/qiang_fen_lie.png")
    elif find_and_click('images/ji_neng/qiang_zeng_shang.png'):
        logger.info(f"发现并选择【枪-增伤-技能】images/huan_qiu/qiang_zeng_shang.png")
    elif find_and_click('images/ji_neng/qiang_bao_zha.png'):
        logger.info(f"发现并选择【枪-爆炸-技能】images/ji_neng/qiang_bao_zha.png")
    # elif find_and_click('images/ji_neng/wen_ya_dan_lian_fa.png'):
    #     logger.info(f"发现并选择【温压弹连发技能】images/ji_neng/wen_ya_dan_lian_fa.png")

def close_ji_neng_jiao_yi():
    if find_and_click('images/huan_qiu/ji_neng_jiao_yi.png', offset_name='close_ji_neng_jiao_yi'):
        logger.info(f"发现 images/huan_qiu/ji_neng_jiao_yi.png, 执行 - 关闭技能交易")

def close_yuan_zheng():
    # 只有 周五、周六、周日 才会出现 退出远征
    if datetime.now().weekday() > 4:
        if find_and_click('images/huan_qiu/yuan_zheng_fang_an.png', offset_name='close_yuan_zheng_fang_an'):
            logger.info(f"发现 images/huan_qiu/yuan_zheng_fang_an.png, 执行- 关闭远征-方案选择")

        if find_and_click('images/huan_qiu/yuan_zheng.png', offset_name='close_yuan_zheng'):
            logger.info(f"发现 images/huan_qiu/yuan_zheng.png, 执行 - 关闭远征")
            time.sleep(1)

            if find_and_click('images/huan_qiu/close_yuan_zheng_que_ren.png', offset_name='close_yuan_zheng_que_ren'):
                logger.info(f"发现 images/huan_qiu/close_yuan_zheng_que_ren.png, 执行- 退出远征")
                time.sleep(1)
            
            return True
    return False

def close_guang_gao():
    logger.info(f"关闭【广告】")
    time.sleep(1)
    find_and_click('images/header.png', offset_name='close_guang_gao_1')
    time.sleep(1)

def close_chou_jiang_1():
    logger.info(f"关闭【抽奖】")
    time.sleep(1)
    find_and_click('images/header.png', offset_name='close_chou_jiang_1')
    time.sleep(1)

def close_x():
    logger.info(f"关闭【X】")
    time.sleep(1)
    find_and_click('images/close_x.png', confidence=0.95)
    time.sleep(1)
