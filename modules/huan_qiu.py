from datetime import datetime
import random
import time

from utils.image_utils import find, find_and_click
from utils.logger import get_logger
from .operators.common_operations import (
    close_first_charge,
    close_ji_neng_jiao_yi,
    open_chat,
    is_chat_open,
    is_chat_zhao_mu_open,
    open_zhao_mu,
    close_guan_qia_select,
    close_yuan_zheng,
    check_huan_qiu_start,
    select_ji_neng,
    close_offline,
)

# 初始化日志
logger = get_logger()

class HuanQiu:
    def __init__(self, max_num=40, disable_skill=False):
        self.max_num = max_num
        self.disable_skill = disable_skill
    
    def start(self):
        """启动入口"""
        logger.info(f"最大执行次数：{self.max_num}")
        logger.info(f"技能选择功能状态：{'禁用' if self.disable_skill else '启用'}")
        self._start_huan_qiu_jiu_yuan()

    def _start_huan_qiu_jiu_yuan(self):
        game_num = 1
        while True:
            logger.info(f"第【{game_num}】局 - 开始执行")
            time.sleep(1)

            if game_num > self.max_num:
                logger.info(f"第【{game_num}】局 - 已经执行了【{self.max_num}】次，退出")
                break

            close_first_charge()

            close_ji_neng_jiao_yi()

            close_yuan_zheng()

            if open_chat():
                if is_chat_open():
                    logger.info(f"第【{game_num}】局 - 进入聊天页面")
                else:
                    logger.info(f"第【{game_num}】局 - 进入聊天页面 - 失败")
                    time.sleep(1)

                open_zhao_mu()

                close_first_charge()

                # 点击抢寰球
                self._qiang_huan_qiu(game_num)

                # 判断是否结束
                self._wait_for_game_end(game_num)
                
                game_num = game_num + 1
            else:
                logger.info("寰球救援页面未找到")
                time.sleep(1)
    
    def _qiang_huan_qiu(self, game_num: int):
        """抢寰球"""
        logger.info("抢寰球")
        # 抢寰球
        for i in range(100):
            logger.info(f"第【{game_num}】局 - 第【{i}】次抢寰球救援")
            # 判断是否抢到，如果抢到，则退出当前循环
            if i!=0 and ( check_huan_qiu_start() or find('images/huan_qiu/play_select_skills.png') ):
                logger.info(f"第【{game_num}】局 - 抢寰球 - 已经开始游戏")
                break

            # 如果有 聊天框，点击聊天框
            # 1. 判断有没有招募，如果有招募，点击招募，继续抢
            # 2. 如果没有招募，说明可能已经抢到了，调到判断是否结束
            if i!=0 and i%2==0 and not is_chat_open() and not is_chat_zhao_mu_open():
                logger.info(f"第【{game_num}】局 - 抢寰球 - 点击聊天")
                open_chat()
                if not open_zhao_mu():
                    if close_guan_qia_select():
                        open_chat()
                        open_zhao_mu()
                    else:
                        logger.info(f"第【{game_num}】局 - 抢寰球 - 打开招募失败")
                        break
            
            if i!=0 and i%2==0 and close_yuan_zheng():
                logger.info(f"第【{game_num}】局 - 抢寰球 - 关闭远征并重新打开聊天")
                open_chat()
                open_zhao_mu()

            if i!=0 and i%5==0 and close_guan_qia_select():
                logger.info(f"第【{game_num}】局 - 当前执行 - 抢环球 - 关闭关卡选择")
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
                find_and_click('images/huan_qiu/chat_zhao_mu_huan_qiu_1.png', before_sleep=0.01, after_sleep=0.01)
                find_and_click('images/huan_qiu/chat_zhao_mu_huan_qiu_2.png', before_sleep=0.01, after_sleep=0.01)

    def _wait_for_game_end(self, game_num: int):
        """等待游戏结束"""
        logger.info("等待游戏结束...")
        for i in range(90):
            # if i > 15 and not huan_qiu_start:
            #     logger.info(f"第【{game_num}】局 - 当前执行 - 判断是否寰球超过了最大次数 15 次 - 结束")
            #     # 如果超过了最大次数，说明没有抢到寰球，退出
            #     if close_playing_game():
            #         logger.info(f"第【{game_num}】局 - 当前执行 - 退出游戏")
            #         break

            # if not huan_qiu_start and check_huan_qiu_start():
            #     logger.info(f"第【{game_num}】局 - 当前执行 - 寰球 - 开始了")
            #     huan_qiu_start = True

            if i!=0 and i%10 == 0:
                close_offline()

            logger.info(f"第【{game_num}】局 - 第【{i}】次等待游戏结束")
            if find_and_click('images/huan_qiu/game_back.png'):
                time.sleep(1)
                return True
            
            # 选择技能
            if not self.disable_skill:
                select_ji_neng()

            time.sleep(10)

        return False
    
