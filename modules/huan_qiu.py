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
    close_all_x,
)

# 初始化日志
logger = get_logger()

class HuanQiu:
    """
    寰球救援任务处理器
    
    Attributes:
        game_num (int): 当前正在执行的游戏局数（从1开始计数）
        max_num (int): 最大允许执行局数
        disable_skill (bool): 是否禁用技能选择功能
    """
    def __init__(self, max_num=40, disable_skill=False):
        self.max_num = max_num
        self.disable_skill = disable_skill
        self.game_num = 1
    
    def start(self):
        """启动入口"""
        logger.info(f"最大执行次数：{self.max_num}")
        logger.info(f"技能选择功能状态：{'禁用' if self.disable_skill else '启用'}")
        self._start_huan_qiu_jiu_yuan()

    def _start_huan_qiu_jiu_yuan(self):
        while True:
            logger.info(f"第【{self.game_num}】局 - 开始执行")
            time.sleep(1)

            if self.game_num > self.max_num:
                logger.info(f"第【{self.game_num}】局 - 已经执行了【{self.max_num}】次，退出")
                break

            close_all_x()

            close_yuan_zheng()

            if open_chat():
                if is_chat_open():
                    logger.info(f"第【{self.game_num}】局 - 进入聊天页面")
                else:
                    logger.info(f"第【{self.game_num}】局 - 进入聊天页面 - 失败")
                    time.sleep(1)

                open_zhao_mu()

                close_all_x()

                # 点击抢寰球
                self._qiang_huan_qiu()

                # 判断是否结束
                self._wait_for_game_end()
                
                self.game_num = self.game_num + 1
            else:
                logger.info("寰球救援页面未找到")
                time.sleep(1)
    
    def _qiang_huan_qiu(self):
        """抢寰球"""
        """执行抢寰球操作（带时间统计和美化日志）"""
        logger.info("🎮 开始抢寰球流程".ljust(50, "─"))
        total_start = time.time()
        attempt_count = 0
        success_flag = False
        # 抢寰球
        for attempt  in range(100):
            attempt_start = time.time()
            attempt_count = attempt + 1

            # 使用表格样式日志头
            logger.info(f"\n🔍 第 [{attempt_count:02d}/100] 次尝试".ljust(50, "─"))
            logger.info(f"├─ 当前游戏局数: 第 {self.game_num} 局")
            logger.info(f"├─ 累计尝试次数: {attempt_count} 次")
            logger.info(f"└─ 已耗时: {time.time()-total_start:.1f}s")

            # 抢到检测逻辑
            # 判断是否抢到，如果抢到，则退出当前循环
            if attempt!=0 and ( check_huan_qiu_start() or find('images/huan_qiu/play_select_skills.png') ):
                success_flag = True
                logger.info("🎉 检测到游戏已开始，终止抢球流程")
                break
            
            if attempt!=0 and i%2==0 and close_yuan_zheng():
                logger.info(f"第【{self.game_num}】局 - 抢寰球 - 关闭远征并重新打开聊天")
                open_chat()
                open_zhao_mu()

            # 如果有 聊天框，点击聊天框
            # 1. 判断有没有招募，如果有招募，点击招募，继续抢
            # 2. 如果没有招募，说明可能已经抢到了，调到判断是否结束
            if attempt!=0 and attempt%2==0 and not is_chat_open() and not is_chat_zhao_mu_open():
                logger.info(f"第【{self.game_num}】局 - 抢寰球 - 点击聊天")
                open_chat()
                if not open_zhao_mu():
                    if close_guan_qia_select():
                        open_chat()
                        open_zhao_mu()
                    else:
                        logger.info(f"第【{self.game_num}】局 - 抢寰球 - 打开招募失败")
                        continue

            if attempt!=0 and attempt%5==0 and close_guan_qia_select():
                logger.info(f"第【{self.game_num}】局 - 当前执行 - 抢环球 - 关闭关卡选择")
                open_chat()
                open_zhao_mu()

            if attempt!=0 and attempt%20==0:
                # 每20次，关闭技能交易
                close_all_x()

            # 抢 20 次，判断一次
            for _ in range(20):
                find_and_click('images/huan_qiu/chat_zhao_mu_huan_qiu_1.png', before_sleep=0.01, after_sleep=0.01)
                find_and_click('images/huan_qiu/chat_zhao_mu_huan_qiu_2.png', before_sleep=0.01, after_sleep=0.01)
            
            # 单次循环耗时统计
            loop_time = time.time() - attempt_start
            logger.info(f"⏳ 单次循环耗时: {loop_time:.2f}s")
        
        # 最终统计报告
        total_time = time.time() - total_start
        time_summary = f"{total_time//60:.0f}分{total_time%60:.1f}秒"
        status_icon = "✅" if success_flag else "❌"
        
        logger.info("\n📊 抢寰球统计报告".ljust(50, "─"))
        logger.info(f"├─ 最终状态: {status_icon} {'成功抢到' if success_flag else '抢球超时'}")
        logger.info(f"├─ 总耗时: {time_summary} ({total_time:.1f}秒)")
        logger.info(f"├─ 游戏局数: 第 {self.game_num} 局")
        logger.info(f"└─ 有效尝试: {attempt_count} 次")
        logger.info("".ljust(50, "─") + "\n")

    def _wait_for_game_end(self):
        """等待游戏结束"""
        start_time = time.time()  # 记录开始时间
        logger.info("[⏱️第%d局游戏已经开始，等待游戏结束]", self.game_num)
        
        for check_count in range(1, 201):
            current_start_time = time.time()

            # 系统维护操作（含耗时显示）
            if check_count % 10 == 0:
                close_offline()
            
            # 游戏结束检测
            if find_and_click('images/huan_qiu/game_back.png'):
                total_time = time.time() - start_time
                logger.info("[✅第%d局游戏成功退出] | 总耗时 %.1f秒 | 第%d次检测",
                            self.game_num, total_time, check_count)
                time.sleep(1)
                return True

            # 技能管理系统
            if not self.disable_skill:
                skill_start_time = time.time()  # 记录技能选择开始时间
                select_ji_neng()
                skill_elapsed_time = time.time() - skill_start_time
                # logger.info("[第%d局游戏] | 第%d次检测 | 技能选择耗时 %d 秒",
                #         self.game_num, check_count, skill_elapsed_time)

            time.sleep(5)

            current_elapsed_time = time.time() - current_start_time
            # 主状态监测（带动态等待时间）
            elapsed_time = time.time() - start_time
            mins, secs = divmod(int(elapsed_time), 60)
            time_str = f"{mins:d}分{secs:d}秒"
            # logger.info("[第%d局游戏] | 第%d次检测是否结束 | 本次检测耗时 %d 秒 | 已等待 %s",
            #         self.game_num, check_count, current_elapsed_time, time_str)
            logger.info("[第%d局游戏] | 第%d次检测是否结束 | 已等待 %s",
                    self.game_num, check_count, time_str)

        total_time = time.time() - start_time
        logger.warning("[⚠️第%d局超时警报] | 总耗时 %.1f秒≈%d分%d秒 | 强制终止",
                    self.game_num, total_time, total_time//60, int(total_time%60))
        return False
    
