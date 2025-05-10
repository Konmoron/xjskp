from datetime import datetime
import random
import time
import sys
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
    check_login_other,
    force_login,
    is_game_started,
    start_game,
)
from .operators.bottom import (
    open_zhan_dou,
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

    def __init__(
        self,
        max_num=20,
        disable_skill=False,
        force_login=False,
        force_login_wait=10,
        force_start=True,
    ):
        self.max_num = max_num
        self.disable_skill = disable_skill
        self.game_num = 1
        self.force_start = force_start
        self.force_login = force_login
        self.force_login_wait = force_login_wait

    def start(self):
        """启动入口"""
        logger.info("".ljust(50, "─"))
        logger.info("🚀 寰球救援参数配置")
        logger.info(f"├─ 🎯 最大执行次数: {self.max_num} 局")
        logger.info(f"├─ 🛠️ 技能选择: {'🔴 禁用' if self.disable_skill else '🟢 启用'}")
        logger.info(f"├─ ⚡ 强制启动: {'🟢 启用' if self.force_start else '🔴 禁用'}")
        logger.info(
            f"├─ 🔒 强制登录: {'🟢 启用' if self.force_login else '🔴 禁用'}"
            + (f" | ⏳ 等待 {self.force_login_wait} 分钟" if self.force_login else "")
        )
        logger.info("".ljust(50, "─"))
        self._start_huan_qiu_jiu_yuan()

    def _start_huan_qiu_jiu_yuan(self):
        while True:
            if self.game_num > self.max_num:
                logger.info(
                    f"第【{self.game_num}】局 - 已经执行了【{self.max_num}】次，退出"
                )
                break

            logger.info(f"第【{self.game_num}】局 - 开始执行")
            time.sleep(1)

            close_yuan_zheng()
            close_all_x()
            open_zhan_dou()

            if open_chat():
                if is_chat_open():
                    logger.info(f"第【{self.game_num}】局 - 进入聊天页面")
                else:
                    logger.info(f"第【{self.game_num}】局 - 进入聊天页面 - 失败")
                    time.sleep(1)
                    continue

                open_zhao_mu()

                # 点击抢寰球
                if not self._qiang_huan_qiu():
                    continue

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
        for attempt in range(100):
            attempt_start = time.time()
            attempt_count = attempt + 1

            # 使用表格样式日志头

            # 抢到检测逻辑
            # 判断是否抢到，如果抢到，则退出当前循环
            if attempt != 0 and (
                check_huan_qiu_start() or find("images/huan_qiu/play_select_skills.png")
            ):
                success_flag = True
                logger.info("🎉 检测到游戏已开始，终止抢球流程")
                break

            if attempt != 0 and attempt % 2 == 0 and close_yuan_zheng():
                logger.info(
                    f"第【{self.game_num}】局 - 抢寰球 - 关闭远征并重新打开聊天"
                )
                open_chat()
                open_zhao_mu()

            # 如果有 聊天框，点击聊天框
            # 1. 判断有没有招募，如果有招募，点击招募，继续抢
            # 2. 如果没有招募，说明可能已经抢到了，调到判断是否结束
            if (
                attempt != 0
                and attempt % 2 == 0
                and not is_chat_open()
                and not is_chat_zhao_mu_open()
            ):
                logger.info(f"第【{self.game_num}】局 - 抢寰球 - 点击聊天")
                open_chat()
                if not open_zhao_mu():
                    if close_guan_qia_select():
                        open_chat()
                        open_zhao_mu()
                    else:
                        logger.info(f"第【{self.game_num}】局 - 抢寰球 - 打开招募失败")
                        continue

            if attempt != 0 and attempt % 5 == 0 and close_guan_qia_select():
                logger.info(
                    f"第【{self.game_num}】局 - 当前执行 - 抢环球 - 关闭关卡选择"
                )
                open_chat()
                open_zhao_mu()

            if attempt != 0 and attempt % 20 == 0:
                # 每20次，关闭技能交易
                close_first_charge()
                close_ji_neng_jiao_yi()

                self._handle_system_checks()

            # 抢 20 次，判断一次
            for _ in range(20):
                find_and_click(
                    "images/huan_qiu/chat_zhao_mu_huan_qiu_1.png",
                    before_sleep=0.02,
                    after_sleep=0.02,
                )
                find_and_click(
                    "images/huan_qiu/chat_zhao_mu_huan_qiu_2.png",
                    before_sleep=0.02,
                    after_sleep=0.02,
                )

            # 单次循环耗时统计
            loop_time = time.time() - attempt_start
            total_elapsed = time.time() - total_start
            total_mins, total_secs = divmod(int(total_elapsed), 60)
            total_time_str = f"{total_mins:02d}分{total_secs:02d}秒"

            logger.info(
                f"⏳ 第{self.game_num}/{self.max_num}局 | 第{attempt_count:02d}/100次抢寰球 | "
                f"总耗时{total_time_str} | "
                f"本次耗时{loop_time:.2f}秒"
            )

        # 最终统计报告
        total_time = time.time() - total_start
        mins, secs = divmod(int(total_time), 60)  # 使用divmod分解
        time_summary = f"{mins:02d}分{secs:02d}秒"  # 补零对齐
        status_icon = "✅" if success_flag else "❌"

        logger.info("📊 抢寰球统计报告")
        logger.info(
            f"├─ 最终状态: {status_icon} {'成功抢到' if success_flag else '抢球超时'}"
        )
        logger.info(f"├─ 总耗时: {time_summary}")
        logger.info(f"├─ 游戏局数: 第 {self.game_num} 局")
        logger.info(f"└─ 有效尝试: {attempt_count} 次")
        logger.info(f"🎮 结束抢寰球流程")

        return success_flag

    def _wait_for_game_end(self):
        """等待游戏结束"""
        start_time = time.time()  # 记录开始时间
        logger.info("[⏱️第%d局游戏已经开始，等待游戏结束]", self.game_num)

        max_wait_count = 200  # 最大等待次数

        for check_count in range(1, max_wait_count + 1):
            current_start_time = time.time()

            # 系统维护操作（含耗时显示）
            if check_count % 10 == 0:
                close_offline()

                self._handle_system_checks()

            # 游戏结束检测
            if find_and_click("images/huan_qiu/game_back.png"):
                total_time = time.time() - start_time
                mins, secs = divmod(int(total_time), 60)
                time_str = f"{mins:02d}分{secs:02d}秒"
                logger.info(
                    "[✅第%d/%s局成功退出] | 总耗时 %s | 第%03d/%s次检测",
                    self.game_num,
                    self.max_num,
                    time_str,
                    check_count,
                    max_wait_count,
                )
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
            time_str = f"{mins:02d}分{secs:02d}秒"
            logger.info(
                "⏳ 第%d/%d局等待结束 | 已等待%s | 第%03d/%d次检测 | 本次耗时%d秒",
                self.game_num,
                self.max_num,
                time_str,
                check_count,
                max_wait_count,
                current_elapsed_time,
            )

        total_time = time.time() - start_time
        logger.warning(
            "[⚠️第%d局超时警报] | 总耗时 %.1f秒≈%d分%d秒 | 强制终止",
            self.game_num,
            total_time,
            total_time // 60,
            int(total_time % 60),
        )
        return False

    def _handle_system_checks(self):
        """处理系统级状态检查"""
        # 登录状态检查
        if check_login_other():
            if self.force_login:
                logger.info(
                    f"第【{self.game_num}】局 - 系统检查 - 检测到【异地登录】执行强制登录"
                )
                force_login()
            else:
                logger.info(
                    f"第【{self.game_num}】局 - 系统检查 - 检测到【异地登录】退出程序"
                )
                sys.exit(0)

        # 游戏启动状态检查
        if not is_game_started():
            if self.force_start:
                logger.info(
                    f"第【{self.game_num}】局 - 系统检查 - 检测到【游戏未启动】执行强制启动"
                )
                start_game()
                time.sleep(1)
                close_all_x()
            else:
                logger.info(
                    f"第【{self.game_num}】局 - 系统检查 - 检测到【游戏未启动】退出程序"
                )
                sys.exit(0)
