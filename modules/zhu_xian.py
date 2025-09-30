from .operators.bottom import (
    open_zhan_dou,
)
from .operators.common_operations import (
    close_guang_gao,
    close_chou_jiang_1,
    close_x,
    close_x_2,
    close_all_x,
    close_all_x_and_back,
    back,
    kan_guang_gao,
    close_yuan_zheng,
)
from utils.image_utils import find_and_click, retry_click, find
from utils.logger import get_logger
import time
import random

logger = get_logger()


class ZhuXian:
    """
    主线关卡
    """

    def __init__(
        self,
        max_num=20,
        force_login=False,
        force_login_wait=10,
        force_start=True,
    ):
        self.max_num = max_num
        self.game_num = 1
        self.force_start = force_start
        self.force_login = force_login
        self.force_login_wait = force_login_wait

    def start(self):
        """启动入口"""
        logger.info("".ljust(50, "─"))
        logger.info("🚀 主线关卡参数配置")
        logger.info(f"├─ 🎯 最大执行次数: {self.max_num} 局")
        logger.info(f"├─ ⚡ 强制启动: {'🟢 启用' if self.force_start else '🔴 禁用'}")
        logger.info(
            f"├─ 🔒 强制登录: {'🟢 启用' if self.force_login else '🔴 禁用'}"
            + (f" | ⏳ 等待 {self.force_login_wait} 分钟" if self.force_login else "")
        )
        logger.info("".ljust(50, "─"))
        self._start()

    def _start(self):
        open_zhan_dou()

        total_start_time = time.time()

        for i in range(self.max_num):
            start_time = time.time()  # 记录开始时间

            logger.info(f"第【{self.game_num}】局 - 开始执行第【{i + 1}】关")

            time.sleep(2)

            retry_click("images/zhu_xian/start.png")
            # 检测是否在战斗界面
            if find("images/zhu_xian/zhan_dou.png"):
                logger.info(f"检测到【战斗】界面，重新点击开始游戏")
                retry_click("images/zhu_xian/start.png")
            # 头选宝石不算
            find_and_click("images/zhu_xian/ji_neng.png", offset_name="select_ji_neng")

            self._wait_for_game_end()

            end_time = time.time()
            elapsed = end_time - start_time
            time_str = f"{int(elapsed // 60)}分{int(round(elapsed % 60))}秒"

            total_elapsed = time.time() - total_start_time
            total_time_str = (
                f"{int(total_elapsed // 60)}分{int(round(total_elapsed % 60))}秒"
            )

            logger.info(
                f"第【{self.game_num}】局 - 耗时: {time_str} - 总耗时: {total_time_str}"
            )

            self.game_num += 1

    def _wait_for_game_end(self):
        """等待游戏结束"""
        num = 0
        while True:
            if find_and_click(
                "images/zhu_xian/ji_neng.png", offset_name="select_ji_neng"
            ):
                logger.info(f"第{self.game_num}局，已选择技能{num+1}次")
                num += 1

                if num >= 4:
                    logger.info(
                        f"第{self.game_num}局，已经选择{num}次技能, 退出当前游戏"
                    )
                    self._exit_current_game()
                    break
                else:
                    continue

            if find_and_click("images/zhu_xian/fan_hui.png"):
                logger.info(f"第{self.game_num}局，失败退出")
                time.sleep(2)
                break
                # self._exit_current_game()

            time.sleep(0.5)

    def _exit_current_game(self):
        """退出当前游戏"""
        # 人类操作间隔通常集中在2-3秒
        time.sleep(random.triangular(1, 5, 2.5))

        find_and_click("images/zhu_xian/ji_neng.png", offset_name="select_ji_neng")

        logger.info(f"第{self.game_num}局，退出当前游戏")
        find_and_click("images/header.png", offset_name="exit_current_game")

        # 再次判断选择技能
        find_and_click("images/zhu_xian/ji_neng.png", offset_name="select_ji_neng")

        # logger.info("退出")
        find_and_click("images/zhu_xian/exit.png")

        # 等待
        # time.sleep(2)
        if find_and_click("images/zhu_xian/shuang_bei.png"):
            logger.info("领取双倍奖励")
            kan_guang_gao()

        # logger.info("返回")
        find_and_click("images/zhu_xian/fan_hui.png")

        find_and_click("images/zhu_xian/dian_ji_ping_mu.png")
