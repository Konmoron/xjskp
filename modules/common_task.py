import argparse
from datetime import datetime
from typing import Dict, Callable
from utils.image_utils import drag_search, find, find_and_click, drag, retry_click
from utils.logger import get_logger
import time
from .operators.bottom import (
    open_zhan_dou,
    open_jun_tuan,
    open_shop,
    open_sai_ji,
    open_ji_di,
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


logger = get_logger()


class CommonTask:
    def __init__(self):
        self.task_registry: Dict[str, Callable] = {
            "ling_yuan_zheng_piao": self.ling_yuan_zheng_piao,
            "ti_li": self._single_ti_li,
            "jun_tuan": self.jun_tuan,
            "gybz": self.gybz,
            "shop": self.shop,
            "huo_dong": self.huo_dong,
            "sai_ji": self.sai_ji,
            "te_hui": self.te_hui,
            "hao_you": self.hao_you,
            "mail": self.mail,
            "jin_li": self.jin_li,
            "ri_li": self.ri_li,
            "tu_wei": self.tu_wei,
            "jiu_guan": self.jiu_guan,
            "shi_lian_ta": self.shi_lian_ta,
            "yuan_xian": self.yuan_xian,
            "fu_li": self.fu_li,
            "tong_xing_zheng": self.tong_xing_zheng,
            "xun_luo_che_sao_dang": self.xun_luo_che_sao_dang,
        }

        # 新增实例变量
        self.task_queue = []  # 任务队列
        self.excluded_tasks = []  # 被排除任务
        self.task_durations = {}  # 任务耗时记录
        self.total_start = 0  # 总开始时间戳

        # 体力任务相关状态
        self.ti_li_count = 0  # 已执行次数
        self.ti_li_max = 3  # 最大次数
        self.ti_li_wait_start = None  # 等待开始时间
        self.ti_li_all_done = False  # 是否全部完成
        self.ti_li_single_done = False  # 单次完成状态

    def run(self, tasks: str = "all", exclude: str = None):
        """执行任务调度入口"""
        self._init_runtime_state(tasks, exclude)

        try:
            logger.info("🚀 开始执行任务队列".ljust(50, "─"))
            self._process_main_queue()
            self._handle_remaining_tili()
        finally:
            self._generate_summary_report()

    def _init_runtime_state(self, tasks, exclude):
        """初始化运行时状态"""
        # 重置所有状态
        self.task_queue = self._parse_tasks(tasks)
        self.excluded_tasks = [
            t.strip() for t in (exclude.split(",") if exclude else [])
        ]
        self.task_durations = {}
        self.total_start = time.time()

        # 体力任务状态重置
        self.ti_li_count = 0
        self.ti_li_wait_start = None
        self.ti_li_all_done = False
        self.ti_li_single_done = False

        # 调整任务顺序
        self._adjust_task_order("hao_you", "✉️ 调整好友任务到队列末尾")
        self._adjust_task_order("mail", "📨 调整邮件任务到队列末尾")
        self._adjust_task_order("ti_li", "⚡ 调整体力任务到队列首位", front=True)

        logger.info(f"📋 最终任务队列: {', '.join(self.task_queue)}")
        logger.info(
            f"🗑️ 排除任务列表: {', '.join(self.excluded_tasks) if self.excluded_tasks else '无'}"
        )

    def _adjust_task_order(self, task_name, log_msg, front=False):
        """通用任务顺序调整方法"""
        if task_name in self.task_queue:
            self.task_queue.remove(task_name)
            if front:
                self.task_queue.insert(0, task_name)
            else:
                self.task_queue.append(task_name)
            logger.info(log_msg)

    def _process_main_queue(self):
        """处理主任务队列"""
        while self.task_queue:
            current_task = self.task_queue[0]

            if current_task == "ti_li":
                self._process_tili_task()
            else:
                self._process_regular_task(current_task)

            self._check_tili_retry()

    def _process_tili_task(self):
        """处理体力任务逻辑"""
        if self.ti_li_count >= self.ti_li_max or self.ti_li_all_done:
            self.task_queue.pop(0)
            return

        # 执行体力任务
        self.ti_li_all_done, self.ti_li_single_done = self._single_ti_li()
        self._update_tili_status()
        self.task_queue.pop(0)
        close_all_x_and_back()

    def _update_tili_status(self):
        """更新体力任务状态"""
        status_icon = "✅" if self.ti_li_single_done else "❌"

        if self.ti_li_single_done and not self.ti_li_all_done:
            self.ti_li_count += 1
            self.ti_li_wait_start = time.time()
            logger.info(f"{status_icon} 进度: {self.ti_li_count}/{self.ti_li_max}")
        elif self.ti_li_all_done:
            logger.info("🏁 体力任务全部完成")
            self.ti_li_wait_start = None
        else:
            logger.warning(f"{status_icon} 执行失败")
            self.ti_li_wait_start = time.time()

    def _process_regular_task(self, task_name):
        """处理常规任务"""
        logger.info(f"▶️ 当前执行: {task_name.upper()} ".ljust(40, "─"))
        task_start = time.time()

        try:
            self.task_registry[task_name]()
            open_zhan_dou()
            self._record_task_duration(task_name, task_start)
        except Exception as e:
            logger.error(f"‼️ 任务异常: {str(e)}")
        finally:
            self.task_queue.pop(0)
            close_all_x_and_back()
            open_zhan_dou()

    def _record_task_duration(self, task_name, start_time):
        """记录任务耗时"""
        duration = time.time() - start_time
        if task_name not in self.task_durations:
            self.task_durations[task_name] = []
        self.task_durations[task_name].append(duration)
        logger.info(f"✅ 完成 {task_name} | 耗时 {self._format_duration(duration)}")

    def _check_tili_retry(self):
        """检查体力任务重试条件"""
        if (
            not self.ti_li_all_done
            and self.ti_li_wait_start
            and (time.time() - self.ti_li_wait_start) >= 310
            and self.ti_li_count < self.ti_li_max
            and "ti_li" not in self.task_queue
        ):
            logger.info("⏰ 重新插入体力任务")
            self.task_queue.insert(0, "ti_li")
            self.ti_li_wait_start = None

    def _handle_remaining_tili(self):
        """处理剩余体力任务"""
        logger.info("🔍 检查后续体力任务".ljust(50, "─"))
        while (
            not self.ti_li_all_done
            and self.ti_li_wait_start
            and self.ti_li_count < self.ti_li_max
        ):
            if (time.time() - self.ti_li_wait_start) >= 310:
                self.ti_li_all_done, self.ti_li_single_done = self._single_ti_li()
                if self.ti_li_single_done and not self.ti_li_all_done:
                    self.ti_li_count += 1
                    self.ti_li_wait_start = time.time()
                else:
                    logger.warning("执行失败，跳过")
                    self.ti_li_wait_start = None
                    break
            else:
                elapsed = time.time() - self.ti_li_wait_start
                logger.info(
                    f"等待第{self.ti_li_count+1}次领取 | 已等待 {self._format_duration(elapsed)}"
                )
                time.sleep(10)

    def _generate_summary_report(self):
        """生成总结报告"""
        logger.info("📊 执行摘要".ljust(50, "─"))
        total_duration = time.time() - self.total_start

        # 常规任务统计
        if self.task_durations:
            logger.info("📦 常规任务统计:")
            for task, durations in self.task_durations.items():
                total = sum(durations)
                avg = total / len(durations)
                logger.info(
                    f"  ▪ {task.ljust(8)}: "
                    f"执行{len(durations):>2}次 | "
                    f"总耗时{self._format_duration(total):>8} | "
                    f"平均{self._format_duration(avg):>8}"
                )

        # 体力任务统计
        if self.ti_li_count > 0:
            logger.info("⚡ 体力任务统计:")
            logger.info(f"  ▪ 成功执行: {self.ti_li_count+1}次")
            if self.ti_li_count > 1:
                logger.info(
                    f"  ▪ 冷却等待: {self._format_duration(310*(self.ti_li_count-1))}"
                )

        # 最终汇总
        logger.info("🏁 最终汇总".ljust(50, "─"))
        logger.info(f"⏱️ 总运行时间: {self._format_duration(total_duration)}")
        logger.info(
            f"📌 完成任务数: {sum(len(v) for v in self.task_durations.values()) + self.ti_li_count}"
        )
        logger.info("🎉 所有任务处理完成".ljust(50, "─"))

    def _format_duration(self, seconds: float) -> str:
        """将秒数格式化为 mm'ss'' 形式"""
        mins, secs = divmod(int(seconds), 60)
        return f"{mins:02d}分{secs:02d}秒" if mins > 0 else f"{int(secs)}秒"

    def _parse_tasks(self, tasks: str) -> list:
        """解析任务参数"""
        if tasks.lower() == "all":
            return list(self.task_registry.keys())
        return [t.strip() for t in tasks.split(",") if t.strip()]

    def ri_li(self):
        """执行【战斗-日历】任务"""
        logger.info("执行【战斗-日历】任务...")
        open_zhan_dou()

        if find_and_click("images/ri_li/button.png"):
            logger.info(f"打开【战斗-日历】")
        else:
            logger.info(f"未找到【战斗-日历】")
            return False

        if find_and_click("images/ri_li/ling_qu.png"):
            logger.info(f"打开【战斗-日历】-【领取奖励】")
            close_chou_jiang_1()

        close_x()

    def tu_wei(self):
        """执行【战斗-七日突围】任务"""
        logger.info("执行【战斗-七日突围】任务...")
        open_zhan_dou()

        # 找到活动按钮
        if drag_search(
            "images/header.png", "images/tu_wei/button.png", "zhan_dou_left_down", 3
        ):
            logger.info(f"向下拖拽找到【战斗-七日突围】")
        elif drag_search(
            "images/header.png", "images/tu_wei/button.png", "zhan_dou_left_up", 3
        ):
            logger.info(f"向上拖拽找到【战斗-七日突围】")
        else:
            logger.info(f"向上、向下拖拽未找到【战斗-七日突围】")
            return False

        if find_and_click("images/tu_wei/button.png", after_sleep=2):
            logger.info(f"打开【战斗-七日突围】")
            close_chou_jiang_1()

        time.sleep(1)
        back()

    def fu_li(self):
        """执行【战斗-福利】任务"""
        logger.info("执行【战斗-福利】任务...")
        open_zhan_dou()

        if find_and_click("images/fu_li/button.png", after_sleep=2):
            logger.info(f"打开【战斗-福利】")
            close_chou_jiang_1()

        time.sleep(1)
        back()

    def mail(self):
        """执行【邮件】任务"""
        logger.info("执行【邮件】任务...")
        open_zhan_dou()
        try:
            # ================= 打开好友界面 =================
            if retry_click(
                "images/zhan_dou_right.png", success_image="images/hao_you/button.png"
            ):
                logger.info("✅ 打开战斗右侧折叠")
            else:
                logger.warning("❌ 战斗右侧折叠失败")
                return False

            if find_and_click("images/mail/button.png"):
                logger.info(f"打开【邮件】")
            else:
                logger.info(f"未找到【邮件】")
                return False

            if find_and_click("images/mail/ling_qu.png"):
                logger.info(f"打开【邮件】-【领取奖励】")
                close_chou_jiang_1()
        finally:
            close_x()
            logger.info("关闭战斗右侧折叠")
            if find("images/hao_you/button.png"):
                find_and_click("images/zhan_dou_right.png")

    def jin_li(self):
        """执行【锦鲤】任务"""
        logger.info("执行【锦鲤】任务...")
        open_zhan_dou()

        # 找到活动按钮
        if drag_search(
            "images/header.png", "images/jin_li/button.png", "zhan_dou_left_down", 3
        ):
            logger.info(f"向下拖拽找到【锦鲤】")
        elif drag_search(
            "images/header.png", "images/jin_li/button.png", "zhan_dou_left_up", 3
        ):
            logger.info(f"向上拖拽找到【锦鲤】")
        else:
            logger.info(f"向上、向下拖拽未找到【锦鲤】")
            return False

        if find_and_click("images/jin_li/button.png"):
            logger.info(f"打开【锦鲤】")

        if find_and_click("images/jin_li/fu_li.png"):
            logger.info(f"打开【锦鲤】-【免费福利】")
        else:
            logger.info(f"未找到【锦鲤】-【免费福利】")

        if find_and_click("images/jin_li/ling_qu.png", after_sleep=2):
            logger.info(f"打开【锦鲤】-【免费福利】-【领取奖励】")
            close_chou_jiang_1()

        close_x()

    def huo_dong(self):
        """执行【战斗-活动】任务"""
        logger.info("执行【战斗-活动】任务...")

        open_zhan_dou()

        # 找到活动按钮
        if drag_search(
            "images/header.png", "images/huo_dong/button.png", "zhan_dou_left_down", 3
        ):
            logger.info(f"向下拖拽找到【活动】")
        elif drag_search(
            "images/header.png", "images/huo_dong/button.png", "zhan_dou_left_up", 3
        ):
            logger.info(f"向上拖拽找到【活动】")
        else:
            logger.info(f"向上、向下拖拽未找到【活动】")
            return False

        if find_and_click("images/huo_dong/button.png"):
            logger.info(f"打开【活动】")
            time.sleep(1)

        if find_and_click("images/huo_dong/zuo_zhan_ji_hua.png"):
            logger.info(f"打开【活动】-【作战计划】")
            time.sleep(1)
            if not find("images/huo_dong/qian_dao.png"):
                drag(
                    "images/huo_dong/share.png", "zuo_zhan_ji_hua_down", confidence=0.9
                )

            time.sleep(1)

            if find_and_click("images/huo_dong/qian_dao.png"):
                time.sleep(1)
                logger.info(f"执行【活动】-【作战计划】-【签到】")
                close_chou_jiang_1()
            else:
                logger.info(f"未找到【活动】-【作战计划】-【签到】")

        if find_and_click("images/huo_dong/share.png"):
            logger.info(f"执行【活动】-【分享】")
            time.sleep(1)
            while find("images/huo_dong/share_1.png"):
                time.sleep(1)
                find_and_click("images/huo_dong/share_1.png")
                time.sleep(4)
                logger.info(f"【活动】-【分享】-【分享成功】")

            # 领取奖励
            while find("images/huo_dong/share_ling_qu.png"):
                time.sleep(1)
                find_and_click("images/huo_dong/share_ling_qu.png")
                time.sleep(1)
                logger.info(f"【活动】-【分享】-【领取奖励】")
                close_chou_jiang_1()

        if find_and_click("images/huo_dong/li_bao.png", confidence=0.9):
            logger.info(f"执行【活动】-【特惠礼包】")
            time.sleep(1)

            if find_and_click("images/huo_dong/li_bao_gold.png"):
                time.sleep(1)
                logger.info(f"【活动】-【特惠礼包】-【领取金币】")
                close_chou_jiang_1()

            if find_and_click("images/huo_dong/li_bao_ti_li.png"):
                time.sleep(35)
                logger.info(f"【活动】-【特惠礼包】-【领取体力】")
                close_guang_gao()
                close_chou_jiang_1()

        back()

    def tong_xing_zheng(self):
        """执行【战斗-通行证】任务"""
        logger.info("执行【战斗-通行证】任务...")

        open_zhan_dou()

        if find_and_click("images/tong_xing_zheng/button.png"):
            logger.info(f"打开【通行证】")
            time.sleep(1)
        else:
            logger.info(f"未找到【通行证】按钮")
            return False

        if find_and_click("images/huo_dong/zuo_zhan_ji_hua.png"):
            logger.info(f"打开【活动】-【作战计划】")
            time.sleep(1)
            if not find("images/huo_dong/qian_dao.png"):
                logger.info(f"未找到【签到】按钮，向下拖拽查找")
                drag(
                    "images/tong_xing_zheng/tong_xing_zheng.png",
                    "zuo_zhan_ji_hua_down",
                    confidence=0.85,
                )

            time.sleep(1)

            if find_and_click("images/huo_dong/qian_dao.png"):
                time.sleep(1)
                logger.info(f"执行【通行证】-【作战计划】-【签到】")
                close_chou_jiang_1()
            else:
                logger.info(f"未找到【通行证】-【作战计划】-【签到】")

        back()

    def _single_ti_li(self):
        """执行单个体力任务（带状态跟踪）"""
        logger.info("🏃♀️ 开始执行单次体力任务流程...")
        all_done, single_done = False, False

        try:
            # ----------------------------
            # 步骤1：打开体力界面
            # ----------------------------
            logger.info("🖱️ 尝试打开体力界面...")
            if not find_and_click("images/header.png", offset_name="open_ti_li"):
                logger.warning("❌ 打开体力界面失败")
                return all_done, single_done

            logger.info("✅ 成功进入体力界面")
            time.sleep(2)  # 等待界面稳定

            # ----------------------------
            # 步骤2：广告观看流程
            # ----------------------------
            logger.info("🔍 正在检测广告按钮...")
            if find_and_click("images/ti_li/start.png", confidence=0.8):
                logger.info("🔄 开始观看广告（预计需要35秒）...")
                kan_guang_gao()
                logger.info(f"✅ 广告观看完成")
                single_done = True
            else:
                logger.warning("⚠️ 未找到广告按钮")

            # ----------------------------
            # 步骤3：完成状态检测
            # ----------------------------
            logger.info("🔍 检查体力领取状态...")
            if find("images/ti_li/end.png"):
                logger.info("🎉 体力任务已全部完成")
                all_done = True
            else:
                logger.info("⏳ 仍有可领取体力次数")
        except Exception as e:
            logger.error(f"‼️ 任务执行异常: {str(e)}")
        finally:
            close_x()
            logger.info("🚪 关闭体力界面")
            return all_done, single_done

    def te_hui(self):
        """执行【特惠】任务"""
        logger.info("执行【特惠】任务...")
        open_zhan_dou()

        try:

            # 找到特惠
            if drag_search(
                "images/header.png", "images/te_hui/te_hui.png", "zhan_dou_left_down", 3
            ):
                logger.info(f"向下拖拽找到【特惠】")
            elif drag_search(
                "images/header.png", "images/te_hui/te_hui.png", "zhan_dou_left_up", 3
            ):
                logger.info(f"向上拖拽找到【特惠】")
            else:
                logger.info(f"向上、向下拖拽未找到【特惠】")
                return False

            if find_and_click("images/te_hui/te_hui.png"):
                logger.info(f"打开【特惠】")
                time.sleep(1)
            else:
                logger.info(f"打开【特惠】失败")
                return False

            if find_and_click("images/te_hui/mei_ri_te_hui.png"):
                logger.info(f"打开【每日特惠】")
                time.sleep(1)
            else:
                logger.info(f"打开【每日特惠】失败")
                return False

            if find_and_click("images/te_hui/start.png"):
                logger.info(f"执行【每日特惠】-【领取奖励】")
                kan_guang_gao()
        finally:
            # 关闭
            back()

    def hao_you(self):
        """执行【好友】任务"""
        logger.info("👥 好友任务开始".ljust(50, "─"))
        open_zhan_dou()

        try:
            # ================= 打开好友界面 =================
            if retry_click(
                "images/zhan_dou_right.png", success_image="images/hao_you/button.png"
            ):
                logger.info("✅ 打开战斗右侧折叠")
            else:
                logger.warning("❌ 战斗右侧折叠失败")
                return False

            logger.info("🔍 正在定位好友入口...")
            if find_and_click("images/hao_you/button.png"):
                logger.info("✅ 成功进入好友界面")
            else:
                logger.warning("❌ 好友入口定位失败")
                return False
            # ================= 领取体力流程 =================
            logger.info("🎁 开始领取好友体力".ljust(45, "─"))

            # 领取体力
            if find_and_click("images/hao_you/ling_qu.png"):
                logger.info("🔘 点击领取按钮成功")
            else:
                logger.info(f"❌ 执行【好友】-【点击领取按钮】失败")
                return False

            if find_and_click("images/hao_you/yi_jian_ling_qu.png"):
                logger.info("🎉 一键领取成功")
                close_x()
            else:
                logger.info(f"❌ 执行【好友】-【一键领取】失败")
                return False
        finally:
            close_x()
            logger.info("关闭战斗右侧折叠")
            if find("images/hao_you/button.png"):
                find_and_click("images/zhan_dou_right.png")

    def jun_tuan(self):
        """军团任务"""
        logger.info("执行军团任务...")
        open_jun_tuan()
        time.sleep(2)

        try:
            # 执行军团贡献
            if find_and_click("images/jun_tuan/gong_xian.png"):
                logger.info(f"打开【军团贡献】")
                time.sleep(1)
                if find_and_click("images/jun_tuan/gong_xian_start.png"):
                    logger.info(f"开始执行【军团贡献】")
                    kan_guang_gao()
                logger.info(f"执行【军团贡献】完成")
                close_x()

            # 执行砍一刀
            if find_and_click("images/jun_tuan/kan_yi_dao_start.png"):
                logger.info(f"打开【砍一刀】")
                time.sleep(1)
                if retry_click(click_image="images/jun_tuan/kan_yi_dao.png"):
                    close_guang_gao()
                    logger.info(f"执行【砍一刀】完成")
                    time.sleep(1)

                close_x()

            # 打开任务大厅
            if find_and_click("images/jun_tuan/task.png"):
                logger.info(f"打开【任务大厅】")
                time.sleep(1)

                # 拖拽搜索辅助方法
                def drag_search(
                    find_image,
                    drag_config,
                    direction,
                    max_attempts=3,
                    find_before_drag=True,
                ):
                    """统一拖拽搜索逻辑"""
                    if find_before_drag and find(find_image, confidence=0.9):
                        logger.info(f"🎯 找到{find_image}")
                        return True

                    for i in range(max_attempts):
                        logger.info(f"🔄 第{i+1}次{direction}拖拽搜索")
                        time.sleep(1)
                        drag("images/header.png", drag_config)
                        time.sleep(2)
                        if find(find_image, confidence=0.9):
                            logger.info(f"🎯 找到{find_image}")
                            return True

                    logger.info(f"❌ 超过最大拖拽次数，未找到{find_image}")
                    return False

                # 任务处理核心逻辑
                def handle_task(task_image, task_name, offset_name=None):
                    """统一处理各类任务"""
                    logger.info(f"🔍 开始查找{task_name}任务")

                    # 组合拖拽策略
                    search_pattern = [
                        ("jun_tuan_task_left_down", "向下", 2),
                        ("jun_tuan_task_left_up", "向上", 2),
                    ]

                    # 补偿策略
                    # 找到图片之后，广告按钮可能会被遮挡，
                    # 这里添加补偿策略，
                    # 先向上，如果还有发现图片，则停止补偿，如果没有，则向下拖拽，
                    bu_chang = [
                        ("jun_tuan_task_up_bu_chang", "补偿向上", 1),
                        ("jun_tuan_task_down_bu_chang", "补偿向下", 1),
                    ]

                    for config, direction, attempts in search_pattern:
                        if drag_search(task_image, config, direction, attempts):
                            logger.info(f"🎯 定位到{task_name}任务")
                            # 补偿
                            for (
                                bu_chang_config,
                                bu_chang_direction,
                                bu_chang_attempts,
                            ) in bu_chang:
                                if drag_search(
                                    task_image,
                                    bu_chang_config,
                                    bu_chang_direction,
                                    bu_chang_attempts,
                                    find_before_drag=False,
                                ):
                                    logger.info(f"🎯 补偿之后，定位到{task_name}任务")
                                    break

                            time.sleep(2)
                            find_and_click(
                                task_image, offset_name=offset_name, confidence=0.9
                            )
                            time.sleep(35)
                            close_guang_gao()
                            close_chou_jiang_1()
                            return True
                    return False

                if find("images/jun_tuan/ren_wu_da_ting_start.png"):
                    logger.info(f"找到【任务大厅】-【广告按钮】")

                    # 优先处理100钻石任务（带重试机制）
                    max_retries = 1  # 最大重试次数
                    task_success = False

                    for attempt in range(max_retries + 1):
                        logger.info(f"💎 第{attempt+1}次尝试处理100钻石任务")
                        if handle_task(
                            "images/jun_tuan/task_100_zuan_shi.png",
                            "100钻石",
                            "jun_tuan_task_100_zuan_shi",
                        ):
                            task_success = True
                            break
                        time.sleep(2)  # 重试前等待

                    if not task_success:
                        logger.warning("💎 未找到钻石任务，尝试查找宝箱任务")
                        for attempt in range(max_retries + 1):
                            logger.info(f"💎 第{attempt+1}次尝试处理查找宝箱任务")
                            if handle_task(
                                "images/jun_tuan/task_2_bao_xiang.png",
                                "双宝箱",
                                "jun_tuan_task_2_bao_xiang",
                            ):
                                task_success = True
                                break
                            time.sleep(2)  # 重试前等待
                else:
                    logger.warning("❌ 未找到【任务大厅】-【广告按钮】-不执行任务")

                close_x()

            # 军团联赛-驻守
            # 周二、周四、周六执行
            if datetime.now().weekday() in {1, 3, 5}:
                logger.info(
                    f"⏸️ 当前为 {datetime.now().strftime('%A')}为军团联赛驻守日期"
                )
                if find_and_click("images/jun_tuan/wan_fa_da_ting/button.png"):
                    logger.info(f"打开【玩法大厅】")
                    if find_and_click("images/jun_tuan/wan_fa_da_ting/jin_ru.png"):
                        logger.info(f"打开【军团联赛】")
                        if find("images/jun_tuan/wan_fa_da_ting/jun_tuan_lian_sai.png"):
                            if find_and_click(
                                "images/jun_tuan/wan_fa_da_ting/1_hao_ta.png",
                                confidence=0.9,
                            ) or find_and_click(
                                "images/jun_tuan/wan_fa_da_ting/1_hao_ta_0.png"
                            ):
                                logger.info(f"打开【1号塔】")
                                if find_and_click(
                                    "images/jun_tuan/wan_fa_da_ting/zhu_shou.png"
                                ):
                                    logger.info(f"驻守【1号塔】")
                                else:
                                    logger.info(f"未找到【驻守】按钮，可能已经驻守")
                                close_x()
                        else:
                            logger.info(f"未找到【军团联赛】")
                        back()
                    back()
        finally:
            logger.info("🏁 军团任务执行完毕")
            close_all_x_and_back()
            open_zhan_dou()

    def jiu_guan(self):
        """酒馆"""
        # 仅周日执行
        if datetime.now().weekday() != 6:
            logger.info("酒馆仅周日执行")
            return

        open_zhan_dou()

        if find_and_click("images/ji_di.png"):
            time.sleep(1)
            if find_and_click("images/jiu_guan/jiu_guan.png"):
                time.sleep(1)
                if find_and_click("images/jiu_guan/zhao_mu.png"):
                    while True:
                        if find_and_click("images/jiu_guan/10.png"):
                            time.sleep(1)
                        else:
                            find_and_click("images/jiu_guan/que_ren.png")
                            break

                back()

        open_zhan_dou()

    def shop(self):
        """商店"""
        logger.info("执行【商店】任务...")

        # 打开商店
        time.sleep(1)
        open_shop()

        # 领取卡片
        i = 0
        while True:
            if find_and_click("images/shop/bao_xiang.png"):
                logger.info(f"第{i+1}次领取卡牌")
                kan_guang_gao()
                time.sleep(2)
                back()
            else:
                logger.info(f"没有找到卡牌按钮，卡牌任务结束")
                break

        # 拖拽到能看到紫色宝箱
        drag("images/header.png", "shop_bao_xiang")

        i = 0
        while True:
            if find_and_click("images/shop/bao_xiang.png"):
                logger.info(f"第{i+1}次领取宝箱")
                time.sleep(35)
                close_guang_gao()
                close_chou_jiang_1()
            else:
                logger.info(f"没有找到宝箱按钮，宝箱任务结束")
                break

        time.sleep(4)

        # 拖拽到最底部
        drag("images/header.png", "shop")

        time.sleep(1)
        find_and_click("images/shop/gold_2.png")
        close_chou_jiang_1()

        time.sleep(1)
        if find_and_click("images/shop/gold_1.png"):
            logger.info(f"领取【金币】-观看广告")
            time.sleep(35)
            close_guang_gao()
            close_chou_jiang_1()

        # 执行 每日特惠
        if find_and_click("images/shop/mei_ri_te_hui.png"):
            logger.info(f"执行【每日特惠】")
            time.sleep(2)
            if find_and_click("images/shop/mei_ri_te_hui_mian_fei.png"):
                kan_guang_gao()

        # 执行 特惠礼包
        if find_and_click("images/shop/te_hui_li_bao.png"):
            logger.info(f"执行【特惠礼包】")
            if find_and_click("images/shop/te_hui_li_bao_mian_fei_1.png"):
                kan_guang_gao()

            if find_and_click("images/shop/te_hui_li_bao_mian_fei_2.png"):
                close_chou_jiang_1()

        open_zhan_dou()

    def gybz(self):
        """观影宝藏"""
        logger.info("执行【观影宝藏】任务...")
        open_zhan_dou()

        # 找到特惠
        if drag_search(
            "images/header.png",
            "images/guan_ying_bao_zang/open.png",
            "zhan_dou_left_down",
            3,
        ):
            logger.info(f"向下拖拽找到【观影宝藏】")
        elif drag_search(
            "images/header.png",
            "images/guan_ying_bao_zang/open.png",
            "zhan_dou_left_up",
            3,
        ):
            logger.info(f"向上拖拽找到【观影宝藏】")
        else:
            logger.info(f"向上、向下拖拽未找到【观影宝藏】")
            return False

        if find_and_click("images/guan_ying_bao_zang/open.png"):
            time.sleep(1)
            logger.info(f"打开【观影宝藏】")
        else:
            logger.info(f"打开【观影宝藏】失败")
            return False

        # 执行5次
        for i in range(5):
            if find("images/guan_ying_bao_zang/end.png", confidence=0.95):
                logger.info(
                    f"【观影宝藏】已经执行完毕 images/guan_ying_bao_zang/end.png"
                )
                time.sleep(1)
                break

            logger.info(f"第{i+1}次执行【观影宝藏】")

            if find_and_click(
                "images/guan_ying_bao_zang/start_1.png"
            ) or find_and_click("images/guan_ying_bao_zang/start.png"):
                logger.info(f"第{i+1}次 打开【观看广告】...")
                time.sleep(35)

                close_guang_gao()
                logger.info(f"第{i+1}次 等待抽奖")
                time.sleep(5)
                close_chou_jiang_1()

                time.sleep(1)
                logger.info(f"第{i+1}次【观影宝藏】执行完成")

        # 返回
        time.sleep(1)
        back()

    def yuan_xian(self):
        """
        执行【极速院线】任务
        """

        logger.info("执行【极速院线】任务...")
        open_zhan_dou()

        # 找到特惠
        if drag_search(
            "images/header.png",
            "images/yuan_xian/open.png",
            "zhan_dou_left_down",
            3,
        ):
            logger.info(f"向下拖拽找到【极速院线】")
        elif drag_search(
            "images/header.png",
            "images/yuan_xian/open.png",
            "zhan_dou_left_up",
            3,
        ):
            logger.info(f"向上拖拽找到【极速院线】")
        else:
            logger.info(f"向上、向下拖拽未找到【极速院线】")
            return False

        if find_and_click("images/yuan_xian/open.png"):
            time.sleep(1)
            logger.info(f"打开【极速院线】")
        else:
            logger.info(f"打开【极速院线】失败")
            return False

        # 签到
        logger.info(f"执行【极速院线-观影签到】任务")
        if not find("images/yuan_xian/ling_qu.png") and not find(
            "images/yuan_xian/guang_gao.png"
        ):
            drag(
                "images/yuan_xian/qian_dao.png", "zuo_zhan_ji_hua_down", confidence=0.8
            )
        if find_and_click("images/yuan_xian/ling_qu.png"):
            time.sleep(2)
            close_guang_gao()
        time.sleep(2)
        if find_and_click("images/yuan_xian/guang_gao.png"):
            kan_guang_gao()

        time.sleep(2)
        logger.info(f"执行【极速院线-观影宝藏】任务")
        if find_and_click("images/yuan_xian/gybz.png"):
            # 执行5次
            for i in range(5):
                if find("images/guan_ying_bao_zang/end.png", confidence=0.95):
                    logger.info(
                        f"【观影宝藏】已经执行完毕 images/guan_ying_bao_zang/end.png"
                    )
                    time.sleep(1)
                    break

                logger.info(f"第{i+1}次执行【观影宝藏】")

                if find_and_click(
                    "images/guan_ying_bao_zang/start_1.png"
                ) or find_and_click("images/guan_ying_bao_zang/start.png"):
                    logger.info(f"第{i+1}次 打开【观看广告】...")
                    time.sleep(35)

                    close_guang_gao()
                    logger.info(f"第{i+1}次 等待抽奖")
                    time.sleep(5)
                    close_chou_jiang_1()

                    time.sleep(1)
                    logger.info(f"第{i+1}次【观影宝藏】执行完成")
        else:
            logger.info(f"没有找到【极速院线-观影宝藏】任务")

        logger.info(f"执行【极速院线-观影便利店】任务")
        i = 1
        if find_and_click("images/yuan_xian/bian_li_dian.png"):
            while True:
                if not find("images/yuan_xian/guang_gao.png"):
                    logger.info(f"【极速院线-观影便利店】执行完成")
                    break
                if i > 20:
                    logger.info(f"【极速院线-观影便利店】超过20次，停止执行")
                    break

                find_and_click("images/yuan_xian/guang_gao.png")
                logger.info(f"第{i}次执行【极速院线-观影便利店】")
                kan_guang_gao()
                i = i + 1
        else:
            logger.info(f"未找到【极速院线-观影便利店】")

        close_all_x_and_back()

    def ling_yuan_zheng_piao(self):
        """
        周五/周六/周日 执行【领-远征-票】任务
        """
        if datetime.now().weekday() < 4:
            logger.info("领-远征-票任务仅周五/周六/周日执行")
            return False

        logger.info("执行【领-远征-票】任务...")

        open_ji_di()

        if not find_and_click("images/li_lian_da_ting.png"):
            logger.info(f"未找到【历练大厅】入口")
            return False

        logger.info(f"打开【历练大厅】")
        time.sleep(1)

        if find_and_click("images/yuan_zheng/button.png", confidence=0.9):
            logger.info(f"打开【远征】")
            time.sleep(1)

            for i in range(3):
                if (
                    find_and_click("images/yuan_zheng/mian_fei_1.png")
                    or find_and_click("images/yuan_zheng/mian_fei_2.png")
                    or find_and_click("images/yuan_zheng/mian_fei_3.png")
                ):
                    logger.info(f"执行【远征】-【领取奖励】")
                    time.sleep(1)
                    close_guang_gao()
                    break
                else:
                    time.sleep(1)

            close_yuan_zheng()

        back()

    def shi_lian_ta(self):
        """执行【试炼塔】任务"""
        logger.info("执行【试炼塔】任务...")

        open_ji_di()

        if not find_and_click("images/li_lian_da_ting.png"):
            logger.info(f"未找到【历练大厅】入口")
            return False

        logger.info(f"打开【历练大厅】")
        time.sleep(1)

        drag("images/header.png", "shi_lian_ta")
        time.sleep(4)

        if find_and_click("images/shi_lian_ta/tiao_zhan.png"):
            time.sleep(1)
            # 点击底部header区域，避免被遮挡
            find_and_click("images/header.png", offset_name="header_click_bottom")

            logger.info(f"打开【元素试炼】")
            time.sleep(1)
            if retry_click("images/shi_lian_ta/he_xin.png"):
                logger.info(f"打开【核心试炼塔】")
                time.sleep(1)
                if find_and_click("images/shi_lian_ta/gua_ji.png"):
                    logger.info(f"执行【核心试炼塔】-【挂机】")
                    time.sleep(1)
                    if find_and_click("images/shi_lian_ta/ling_qu.png"):
                        logger.info(f"执行【核心试炼塔】-【领取奖励】")
                        time.sleep(1)
                        close_guang_gao()
                    close_all_x()
                back()
            back()
        back()

    def xun_luo_che_sao_dang(self):
        """执行【巡逻车-扫荡】任务"""
        logger.info("执行【巡逻车-扫荡】任务...")

        open_zhan_dou()

        # 打开巡逻车

        if find_and_click("images/sao_dang/xun_luo_che.png"):
            logger.info(f"打开【巡逻车】")
            time.sleep(1)

            kuai_su_num = 0
            while True:
                if find_and_click("images/sao_dang/kuai_su.png"):
                    time.sleep(2)
                    logger.info(f"第{kuai_su_num+1}次执行【巡逻车-扫荡】-快速")
                    close_chou_jiang_1()
                    time.sleep(2)
                    kuai_su_num += 1

                if find("images/sao_dang/kan_guang_gao.png"):
                    logger.info(f"【巡逻车-扫荡】-【快速扫荡】任务完成")
                    time.sleep(2)
                    break

            kan_guang_gao_num = 0
            start_time = time.time()
            while True:
                find_and_click("images/sao_dang/kan_guang_gao.png")

                time.sleep(4)

                if find("images/sao_dang/kan_guang_gao.png"):
                    logger.info(f"【巡逻车-扫荡】任务完成")
                    break
                else:
                    logger.info(f"第{kan_guang_gao_num+1}次执行【巡逻车-扫荡】-看广告")
                    kan_guang_gao()
                    time.sleep(1)
                    kan_guang_gao_num += 1

                time.sleep(2)

                if time.time() - start_time > 300:
                    logger.info(f"等待超过300秒，退出【巡逻车-扫荡】任务")
                    break

            close_x()

    def sai_ji(self):
        """执行【赛季】任务"""
        open_sai_ji()
        logger.info("执行【赛季】任务")

        if find_and_click("images/sai_ji/ka_pi_ba_la.png"):
            logger.info(f"打开【赛季-卡皮巴拉】")
            time.sleep(4)
            if find_and_click("images/sai_ji/an_pai.png"):
                if find("images/sai_ji/start.png"):
                    time.sleep(1)
                    find_and_click("images/sai_ji/fan_ying.png")
                    time.sleep(1)
                    find_and_click("images/sai_ji/fan_ying.png")
                    time.sleep(1)
                    find_and_click("images/sai_ji/start.png")

                back()

            back()

        time.sleep(4)

        # 或者使用具名常量
        SAI_JI_DAYS = {4, 5, 6}

        if datetime.now().weekday() in SAI_JI_DAYS and find_and_click(
            "images/sai_ji/zheng_zhan.png"
        ):
            logger.info(f"打开【赛季-征战】")
            time.sleep(2)
            if find_and_click("images/sai_ji/add_xing_dong_num.png"):
                time.sleep(2)
                if find_and_click("images/sai_ji/kan_guang_gao.png"):
                    logger.info(f"看广告，增加行动次数")
                    kan_guang_gao()
                time.sleep(1)
                close_x()
            back()

        close_all_x_and_back()

        open_zhan_dou()


def main():
    parser = argparse.ArgumentParser(description="通用任务执行器")
    parser.add_argument(
        "--tasks",
        type=str,
        default="all",
        help="指定要执行的任务（多个用逗号分隔），可选值：ads,patrol,coins,chicken,legion",
    )
    args = parser.parse_args()

    CommonTask().run(args.tasks)


if __name__ == "__main__":
    main()
