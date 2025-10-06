"""
挂环球

两个号简称：左 和 右
    左： 提供环球票的号，邀请 右 打环球
    右： 接受邀请

两个区域，左区域和右区域，其中：
    左区域： 左号所在的区域
    右区域： 右号所在的区域

开始准备：
    左：调整窗口大小
    右：调整窗口大小
    左：打开环球页面
    右：打开环球页面

流程：
    1. 左 点击 邀请.png
    2. 左 点击 好友.png
    3. 左 点击 点击 右号.png
    4. 右 点击 副本邀请.png
    5. 右 点击 接受.png
    6. 左 点击 开始游戏.png
    7. 左 等待结束 返回.png
    8. 右 点击 返回.png
"""

from datetime import datetime
import random
import threading
import time
import sys
from utils.image_utils import find, find_and_click, drag_search, retry_click
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
    close_x,
    close_guang_gao,
    check_login_other,
    force_login,
    is_game_started,
    start_game,
    exit_game,
    restart_game,
)
from .operators.bottom import (
    open_zhan_dou,
)

# 初始化日志
logger = get_logger()


class GuaHuanQiu:
    def __init__(
        self,
        max_num=20,
    ):
        self.max_num = max_num
        self.game_num = 1

    def start(self):
        logger.info("开始执行挂环球")

        total_start_time = time.time()

        while True:
            logger.info("\n" + f"= 开始执行第{self.game_num}局 =".center(50, "="))

            start_time = time.time()

            # self.ling_huan_qiu_quan()

            self.check_login_other()

            if not self._handle_invitation(start_time=start_time):
                continue  # 邀请失败时重试当前局

            self._wait_for_game_end(start_time=start_time)

            # 计算耗时
            end_time = time.time()
            elapsed = end_time - start_time
            total_elapsed = time.time() - total_start_time

            # 使用优化后的方法
            time_str = self._format_time(elapsed)
            total_time_str = self._format_time(total_elapsed)

            logger.info(
                f"第{self.game_num}/{self.max_num}局结束 - 耗时: {time_str} - 总耗时: {total_time_str}"
            )

            self.game_num += 1

            if self.game_num > self.max_num:
                logger.info(f"已经完成{self.max_num}局")
                break

            time.sleep(4)

    def _handle_invitation(self, start_time: float) -> bool:
        """
        处理环球邀请全流程

        Returns:
            bool: True 表示邀请成功，False 表示需要重试当前局
        """
        logger.info(f"第{self.game_num}/{self.max_num}局 - 左号 - 开始邀请")

        # 清理可能存在的邀请页面
        if find("images/gua_huan_qiu/yi_jian_yao_qing.png", image_region_name="zuo"):
            close_x(image_region_name="zuo")

        # 左号发起邀请
        retry_click(
            "images/gua_huan_qiu/yao_qing.png",
            click_kwargs={"image_region_name": "zuo"},
            find_kwargs={"image_region_name": "zuo"},
        )

        logger.info(f"第{self.game_num}/{self.max_num}局 - 左号 - 点击邀请成功")

        # 左 点击 好友
        click_hao_you_num = 0
        while True:
            find_and_click("images/gua_huan_qiu/hao_you.png", image_region_name="zuo")

            # 如果没有找到发布招募，说明好友点击成功
            if not find(
                "images/gua_huan_qiu/fa_bu_zhao_mu.png", image_region_name="zuo"
            ):
                logger.info(f"第{self.game_num}/{self.max_num}局 - 左号 - 点击好友成功")
                break

            if click_hao_you_num > 10:
                logger.warning(
                    f"第{self.game_num}/{self.max_num}局 - 左号 - 点击好友失败 10 次 - 重新开始"
                )
                time.sleep(4)
                return False

            click_hao_you_num += 1
            logger.warning(
                f"第{self.game_num}/{self.max_num}局 - 左号 - 点击好友失败 - 重试"
            )

        # 左号 查找右号好友（支持拖拽）
        if not find(
            "images/gua_huan_qiu/zuo_yao_qing_you.png",
            image_region_name="zuo",
            confidence=0.95,
        ):
            logger.warning(
                f"第{self.game_num}/{self.max_num}局 - 左号 没有找到 右号 好友 - 开始向下拖拽查找"
            )

            # 左号 向下拖拽找到 右号
            if not drag_search(
                base_image_path="images/gua_huan_qiu/zuo_header.png",
                search_image_path="images/gua_huan_qiu/zuo_yao_qing_you.png",
                search_image_confidence=0.95,
                drag_config_name="gua_huan_qiu_zhao_hao_you",
                max_attempts=10,
                image_region_name="zuo",
            ):
                close_x()
                logger.warning(
                    f"第{self.game_num}/{self.max_num}局 - 左号 没有找到 右号 好友 - 重试"
                )
                time.sleep(4)
                return False  # 标记需要重试

        # 左号 邀请 右号
        find_and_click(
            "images/gua_huan_qiu/zuo_yao_qing_you.png",
            offset_name="gua_huan_qiu_zuo_yao_qing",
            image_region_name="zuo",
            confidence=0.95,
        )

        logger.info(f"第{self.game_num}/{self.max_num}局 - 右号 - 接受邀请")

        # 右号 检查是否收到邀请
        check_num = 0
        while True:
            if find("images/gua_huan_qiu/fu_ben_yao_qing.png"):
                # 右号 点击 副本邀请
                retry_click(
                    click_image="images/gua_huan_qiu/fu_ben_yao_qing.png",
                    find_kwargs={"image_region_name": "default"},
                    click_kwargs={"image_region_name": "default"},
                )
                break

            check_num += 1
            time.sleep(1)

            if check_num > 10:
                logger.warning(
                    f"第{self.game_num}/{self.max_num}局 - 右号 - 没有收到邀请 - 重试"
                )
                time.sleep(4)
                return False

        # 右号 接受邀请
        find_and_click(
            "images/gua_huan_qiu/you_jie_shou_zuo_yao_qing.png",
            offset_name="gua_huan_qiu_you_jie_shou",
            image_region_name="default",
            confidence=0.95,
        )

        # 验证邀请结果
        check_num = 0
        while True:
            if find(
                "images/gua_huan_qiu/deng_dai_kai_shi.png",
                image_region_name="default",
            ):
                logger.info(f"第{self.game_num}/{self.max_num}局 - 邀请成功 - 点击开始")
                # 点击开始
                if retry_click(
                    click_image="images/gua_huan_qiu/kai_shi.png",
                    find_kwargs={"image_region_name": "zuo"},
                    click_kwargs={"image_region_name": "zuo"},
                ):
                    time_str = self._format_time(time.time() - start_time)
                    logger.info(
                        f"第{self.game_num}/{self.max_num}局 - 邀请成功 - 开始游戏 - 耗时: {time_str}"
                    )

                    return True  # 邀请成功
                else:
                    time_str = self._format_time(time.time() - start_time)
                    logger.warning(
                        f"第{self.game_num}/{self.max_num}局 - 邀请失败 - 尝试重新邀请 - 耗时: {time_str}"
                    )

                    return False

            check_num += 1

            # 超时处理
            if check_num > 10:
                time_str = self._format_time(time.time() - start_time)
                logger.warning(
                    f"第{self.game_num}/{self.max_num}局 - 邀请失败 - 等待1分钟重试 - 耗时: {time_str}"
                )

                # 等待1分钟
                time.sleep(60)

                return False  # 标记需要重试

            # 右号 重新 接受邀请
            find_and_click(
                "images/gua_huan_qiu/you_jie_shou_zuo_yao_qing.png",
                offset_name="gua_huan_qiu_you_jie_shou",
                image_region_name="default",
                confidence=0.95,
            )

    def _wait_for_game_end(self, start_time: float) -> bool:
        """
        等待游戏结束并处理返回流程

        Args:
            start_time: 当前局开始的时间戳

        Returns:
            bool: True 表示正常结束，False 表示超时
        """
        logger.info(f"第{self.game_num}/{self.max_num}局 - 开始等待结束")

        wait_num = 0
        while True:
            # 检测返回按钮
            if find("images/gua_huan_qiu/fan_hui.png", image_region_name="default"):
                # 双区域点击返回
                find_and_click(
                    "images/gua_huan_qiu/fan_hui.png",
                    image_region_name="zuo",
                )
                find_and_click(
                    "images/gua_huan_qiu/fan_hui.png",
                    image_region_name="default",
                )
                time.sleep(2)
                return True  # 正常结束

            wait_num += 1

            # 每40秒执行检查
            if wait_num % 10 == 0:
                self.check_login_other()

                wait_time = time.time() - start_time

                # 超时处理（20分钟）
                if wait_time > 1200:
                    logger.warning(
                        f"第{self.game_num}/{self.max_num}局 - 等待时间超过20分钟，强制结束"
                    )
                    return False  # 超时结束

                # 记录等待进度
                wait_time_str = self._format_time(wait_time)
                logger.info(
                    f"第{self.game_num}/{self.max_num}局 - 已等待: {wait_time_str}"
                )

            time.sleep(4)

    def check_login_other(self) -> bool:
        """
        检查是否其他账号登录
        """
        if check_login_other(region_name="zuo"):
            logger.warning("检测到 zuo 其他账号登录，结束程序")
            sys.exit(0)

        if check_login_other(region_name="default"):
            logger.warning("检测到 you 其他账号登录，结束程序")
            sys.exit(0)

    def ling_huan_qiu_quan(self):
        """
        领寰球券
        """

        if find_and_click("images/huan_qiu/huan_qiu_quan.png", image_region_name="zuo"):
            close_guang_gao(image_region_name="zuo")

        if find_and_click(
            "images/huan_qiu/huan_qiu_quan.png", image_region_name="default"
        ):
            close_guang_gao(image_region_name="default")

    def _format_time(self, seconds: float) -> str:
        """将秒数格式化为可读时间字符串（自动处理进位并优化显示）"""
        hours = seconds // 3600
        remaining_seconds = seconds % 3600
        minutes = remaining_seconds // 60
        seconds = round(remaining_seconds % 60)

        # 处理进位
        if seconds >= 60:
            seconds -= 60
            minutes += 1
        if minutes >= 60:
            minutes -= 60
            hours += 1

        # 精确转换为整数
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        # 根据时间单位存在情况动态构建字符串
        parts = []
        if hours > 0:
            parts.append(f"{hours}小时")
        if minutes > 0:
            parts.append(f"{minutes}分")
        # 仅当小时和分钟都为0时显示秒数（包括0秒情况）
        if hours == 0 and minutes == 0:
            parts.append(f"{seconds}秒")
        elif seconds > 0:  # 有分钟/小时时，仅当秒>0才显示
            parts.append(f"{seconds}秒")

        # 处理全0情况（0秒）
        return "".join(parts) if parts else "0秒"
