import argparse
from nt import close
from typing import Dict, Callable
from utils.image_utils import drag_search, find, find_and_click, drag
from utils.logger import get_logger
import time
from .operators.bottom import (
    open_zhan_dou,
    open_jun_tuan,
    open_shop,
    open_sai_ji,
)
from .operators.common_operations import (
   close_guang_gao, 
   close_chou_jiang_1,
   close_x,
   close_x_2,
   back,
   kan_guang_gao,
)
from config import DRAG_CONFIGS
    

logger = get_logger()

class CommonTask:
    def __init__(self):
        self.task_registry: Dict[str, Callable] = {
            'ti_li': self._single_ti_li,
            'jun_tuan': self.jun_tuan,
            'gybz': self.gybz,
            'shop': self.shop,
            'huo_dong': self.huo_dong,
            'sai_ji': self.sai_ji,
            'te_hui': self.te_hui,
            'hao_you': self.hao_you,
        }

    # def run(self, tasks: str = 'all', exclude: str = None):
    #     """执行任务调度入口
    #     :param exclude: 需要排除的任务列表（逗号分隔）
    #     """
    #     selected_tasks = self._parse_tasks(tasks)
    #     exclude_list = [t.strip() for t in (exclude.split(',') if exclude else [])]
        
    #     # 过滤排除任务
    #     final_tasks = [t for t in selected_tasks if t not in exclude_list]
        
    #     # 确保ti_li任务最后执行（如果存在）
    #     if 'ti_li' in final_tasks:
    #         final_tasks.remove('ti_li')
    #         final_tasks.append('ti_li')
        
    #     logger.info(f"排除任务：{exclude_list} | 最终执行任务：{', '.join(final_tasks)}")
        
    #     task_durations = {}  # 存储任务耗时
    #     start_total = time.time()  # 总开始时间
        
    #     for task_name in final_tasks:
    #         if task_name in self.task_registry:
    #             start_time = time.time()
    #             self.task_registry[task_name]()
    #             task_durations[task_name] = time.time() - start_time
    #         else:
    #             logger.warning(f"未知任务：{task_name}")
        
    #     # 输出汇总信息
    #     total_duration = time.time() - start_total
    #     logger.info("📊 任务执行时间汇总：")
    #     for task, duration in task_durations.items():
    #         # 超过60秒的转换为分钟显示
    #         if duration >= 60:
    #             mins, secs = divmod(duration, 60)
    #             logger.info(f"→ {task}: {int(mins)}分{secs:.2f}秒")
    #         else:
    #             logger.info(f"→ {task}: {duration:.2f}秒")
        
    #     # 总耗时超过60秒时显示分钟格式
    #     if total_duration >= 60:
    #         total_mins, total_secs = divmod(total_duration, 60)
    #         logger.info(f"⏱️ 总耗时: {int(total_mins)}分{total_secs:.2f}秒")
    #     else:
    #         logger.info(f"⏱️ 总耗时: {total_duration:.2f}秒")

    def run(self, tasks: str = 'all', exclude: str = None):
        """执行任务调度入口"""
        logger.info("🎮 初始化任务队列".ljust(50, "─"))
        final_tasks = self._parse_tasks(tasks)
        exclude_list = [t.strip() for t in (exclude.split(',') if exclude else [])]
        final_tasks = [t for t in final_tasks if t not in exclude_list]

        # 确保ti_li任务最先执行（如果存在）
        if 'ti_li' in final_tasks:
            final_tasks.remove('ti_li')
            final_tasks.insert(0, 'ti_li')
            logger.info(f"⚡ 调整体力任务到队列首位")

        logger.info(f"📋 最终任务队列: {', '.join(final_tasks)}")
        logger.info(f"🗑️ 排除任务列表: {', '.join(exclude_list) if exclude_list else '无'}")

        # 记录每个任务的开始时间
        task_durations = {}  # 存储任务耗时 {'任务名': [耗时1, 耗时2]}
        total_start_time = time.time()  # 总开始时间

        # 特殊处理 ti_li 任务
        ti_li_count = 0  # 已执行体力任务次数
        ti_li_max = 3    # 最大执行次数
        ti_li_wait_start_time = None  # 等待开始时间
        ti_li_all_done, ti_li_single_done = False, False  # 体力任务执行结果
        
        try:
            logger.info("\n🚀 开始执行任务队列".ljust(50, "─"))
            while final_tasks and len(final_tasks) > 0:
                current_task = final_tasks[0]  # 
                task_start_time = time.time()  # 单个任务开始时间
            
                # 处理体力任务
                if current_task == 'ti_li':
                    if ti_li_count >= ti_li_max or ti_li_all_done:
                        final_tasks.pop(0)  # 移除已完成的体力任务
                        ti_li_wait_start_time = None
                        logger.info(f"⏹️ 体力任务已达上限({ti_li_max}次)")
                        continue
                    
                    # 执行单次体力任务
                    ti_li_all_done, ti_li_single_done = self._single_ti_li()
                    status_icon = "✅" if ti_li_single_done else "❌"
                    if ti_li_single_done and not ti_li_all_done:
                        ti_li_count += 1
                        ti_li_wait_start_time = time.time()
                        logger.info(f"{status_icon} 体力领取进度: {ti_li_count}/{ti_li_max}")
                    elif ti_li_all_done:
                        logger.info("🏁 体力任务已全部完成")
                        ti_li_wait_start_time = None
                    else:
                        logger.warning(f"{status_icon} 体力任务执行失败")
                        ti_li_wait_start_time = time.time()
                    
                    final_tasks.pop(0)  # 执行失败也移除
                # 处理其他任务
                else:
                    logger.info(f"\n▶️ 当前执行: {current_task.upper()} ".ljust(40, "─"))
                    try:
                        self.task_registry[current_task]()
                        open_zhan_dou()
                        
                        # 记录耗时
                        duration = time.time() - task_start_time
                        if current_task not in task_durations:
                            task_durations[current_task] = []
                        task_durations[current_task].append(duration)
                        
                        logger.info(f"✅ 完成 {current_task} | 耗时 {self._format_duration(duration)}")
                    except Exception as e:
                        logger.error(f"‼️ 任务异常: {str(e)}")
                    finally:
                        final_tasks.pop(0)

                # 检查是否需要重新插入体力任务
                if (ti_li_wait_start_time and (time.time() - ti_li_wait_start_time) >= 310 
                    and ti_li_count < ti_li_max
                    and 'ti_li' not in final_tasks):
                    logger.info("\n⏰ 满足冷却条件，重新插入体力任务")
                    final_tasks.insert(0, 'ti_li')
                    ti_li_wait_start_time = None

            # 处理体力未执行完的情况
            logger.info("\n🔍 检查后续体力任务".ljust(50, "─"))
            while ti_li_wait_start_time and ti_li_count < ti_li_max:
                if (time.time() - ti_li_wait_start_time) >= 310:
                    ti_li_all_done, ti_li_single_done = self._single_ti_li()
                    if ti_li_single_done and not ti_li_all_done:
                        ti_li_count += 1
                        ti_li_wait_start_time = time.time()
                    else:
                        logger.warning(f"执行体力任务失败，跳过")
                        ti_li_wait_start_time = None
                        break
                else:
                    elapsed = time.time() - ti_li_wait_start_time
                    logger.info(f"等待第{ti_li_count+1}次领取体力 | 已等待 {self._format_duration(elapsed)}")
                    time.sleep(10)
        finally:
            # 统计报告
            logger.info("\n📊 执行摘要".ljust(50, "─"))
            total_duration = time.time() - total_start_time
            
            # 任务耗时统计
            if task_durations:
                logger.info("📦 常规任务统计:")
                for task, durations in task_durations.items():
                    total = sum(durations)
                    avg = total / len(durations)
                    logger.info(
                        f"  ▪ {task.ljust(8)}: "
                        f"执行{len(durations):>2}次 | "
                        f"总耗时{self._format_duration(total):>8} | "
                        f"平均{self._format_duration(avg):>8}"
                    )
            
            # 体力任务统计
            if ti_li_count > 0:
                logger.info("\n⚡ 体力任务统计:")
                logger.info(f"  ▪ 成功执行: {ti_li_count}次")
                logger.info(f"  ▪ 冷却等待: {self._format_duration(310*(ti_li_count-1)) if ti_li_count>1 else '无'}")

            # 最终汇总
            logger.info("\n🏁 最终汇总".ljust(50, "─"))
            logger.info(f"⏱️ 总运行时间: {self._format_duration(total_duration)}")
            logger.info(f"📌 完成任务数: {sum(len(v) for v in task_durations.values()) + ti_li_count}")
            logger.info("🎉 所有任务处理完成".ljust(50, "─"))
    def _format_duration(self, seconds: float) -> str:
        """将秒数格式化为 mm'ss'' 形式"""
        mins, secs = divmod(int(seconds), 60)
        return f"{mins:02d}分{secs:02d}秒" if mins > 0 else f"{int(secs)}秒"

    def _parse_tasks(self, tasks: str) -> list:
        """解析任务参数"""
        if tasks.lower() == 'all':
            return list(self.task_registry.keys())
        return [t.strip() for t in tasks.split(',') if t.strip()]

    def huo_dong(self):
        """执行【战斗-活动】任务"""
        logger.info("执行【战斗-活动】任务...")

        open_zhan_dou()

        # 找到活动
        found = False
        find_num = 0
        while not found and find_num < 6:
            if find('images/huo_dong/button.png'):
                logger.info(f"找到【活动】")
                found = True
                break
            
            # 执行拖拽
            # 向上拖拽3次，
            # 向下拖拽3次，
            if find_num < 3:
                logger.info(f"找活动 - 向上拖拽 {find_num} 次")
                drag('images/header.png', 'zhan_dou_left_down')
            
            if find_num >= 3:
                logger.info(f"找活动 - 向下拖拽 {find_num} 次")
                drag('images/header.png', 'zhan_dou_left_up')
            
            time.sleep(1)
            find_num += 1
        
        if not found:
            logger.info(f"未找到【活动】")
            return False

        if find_and_click('images/huo_dong/button.png'):
            logger.info(f"打开【活动】")
            time.sleep(1)

        if find_and_click('images/huo_dong/zuo_zhan_ji_hua.png'):
            logger.info(f"打开【活动】-【作战计划】")
            time.sleep(1)
            if not find('images/huo_dong/qian_dao.png'):
                drag('images/huo_dong/share.png', 'zuo_zhan_ji_hua_down', confidence=0.9)

            time.sleep(1)

            if find_and_click('images/huo_dong/qian_dao.png'):
                time.sleep(1)
                logger.info(f"执行【活动】-【作战计划】-【签到】")
                close_chou_jiang_1()
            else:
                logger.info(f"未找到【活动】-【作战计划】-【签到】")

        if find_and_click('images/huo_dong/share.png'):
            logger.info(f"执行【活动】-【分享】")
            time.sleep(1)
            while find('images/huo_dong/share_1.png'):
                time.sleep(1)
                find_and_click('images/huo_dong/share_1.png')
                time.sleep(4)
                logger.info(f"【活动】-【分享】-【分享成功】")

            # 领取奖励
            while find('images/huo_dong/share_ling_qu.png'):
                time.sleep(1)
                find_and_click('images/huo_dong/share_ling_qu.png')
                time.sleep(1)
                logger.info(f"【活动】-【分享】-【领取奖励】")
                close_chou_jiang_1()
        
        if find_and_click('images/huo_dong/li_bao.png', confidence=0.9):
            logger.info(f"执行【活动】-【特惠礼包】")
            time.sleep(1)
            
            if find_and_click('images/huo_dong/li_bao_gold.png'):
                time.sleep(1)
                logger.info(f"【活动】-【特惠礼包】-【领取金币】")
                close_chou_jiang_1()
            
            if find_and_click('images/huo_dong/li_bao_ti_li.png'):
                time.sleep(35)
                logger.info(f"【活动】-【特惠礼包】-【领取体力】")
                close_guang_gao()
                close_chou_jiang_1()

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
            if not find_and_click('images/header.png', offset_name='open_ti_li'):
                logger.warning("❌ 打开体力界面失败")
                return all_done, single_done
            
            logger.info("✅ 成功进入体力界面")
            time.sleep(2)  # 等待界面稳定

            # ----------------------------
            # 步骤2：广告观看流程
            # ----------------------------
            logger.info("🔍 正在检测广告按钮...")
            if find_and_click('images/ti_li/start.png', confidence=0.8):
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
            if find('images/ti_li/end.png'):
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

    # def ti_li(self):
    #     """领体力任务"""
    #     logger.info("执行领体力任务...")
    #     time.sleep(1)
        
    #     # 打开【体力】
    #     if find_and_click('images/header.png', offset_name='open_ti_li'):
    #         time.sleep(1)
    #         logger.info(f"打开【体力】")
    #     else:
    #         logger.info(f"打开【体力】失败")
    #         return False

    #     # 领取3次
    #     for i in range(3):
    #         if find('images/ti_li/end.png', confidence=0.95):
    #             logger.info(f"领取【体力】已经执行完毕 images/ti_li/end.png")
    #             time.sleep(1)
    #             break

    #         if find_and_click('images/ti_li/start.png', confidence=0.8):
    #             logger.info(f"第{i+1}次领取体力 - 打开【观看广告】...")
    #             time.sleep(35)
    #             close_guang_gao()
    #             close_chou_jiang_1()
    #             logger.info(f"第{i+1}次领取体力成功")
    #             # 等待5分钟
    #             if i < 2:
    #                 if find('images/ti_li/end.png', confidence=0.9):
    #                     logger.info(f"领取【体力】已经执行完毕 images/ti_li/end.png")
    #                     time.sleep(1)
    #                     break
                    
    #                 logger.info(f"等待5分钟")
    #                 time.sleep(310)
        
    #     # 关闭
    #     close_x()

    def te_hui(self):
        """执行【特惠】任务"""
        logger.info("执行【特惠】任务...")
        open_zhan_dou()

        # 找到特惠
        if drag_search('images/header.png', 'images/te_hui/te_hui.png', 'zhan_dou_left_down', 3):
            logger.info(f"向下拖拽找到【特惠】")
        elif drag_search('images/header.png', 'images/te_hui/te_hui.png', 'zhan_dou_left_up', 3):
            logger.info(f"向上拖拽找到【特惠】")
        else:
            logger.info(f"向上、向下拖拽未找到【特惠】")
            return False

        if find_and_click('images/te_hui/te_hui.png'):
            logger.info(f"打开【特惠】")
            time.sleep(1)
        else:
            logger.info(f"打开【特惠】失败")
            return False

        if find_and_click('images/te_hui/mei_ri_te_hui.png'):
            logger.info(f"打开【每日特惠】")
            time.sleep(1)
        else:
            logger.info(f"打开【每日特惠】失败")
            return False

        if find_and_click('images/te_hui/start.png'):
            logger.info(f"执行【每日特惠】-【领取奖励】")
            kan_guang_gao()

        # 关闭
        back()

    def hao_you(self):
        """执行【好友】任务"""
        logger.info("\n👥 好友任务开始".ljust(50, "─"))
        open_zhan_dou()

        try:
            # ================= 打开好友界面 =================
            logger.info("🔍 正在定位好友入口...")
            if find_and_click('images/hao_you/button.png'):
                logger.info("✅ 成功进入好友界面")
            else:
                logger.warning("❌ 好友入口定位失败")
                return False
            # ================= 领取体力流程 =================
            logger.info("\n🎁 开始领取好友体力".ljust(45, "─"))
            
            # 领取体力
            if find_and_click('images/hao_you/ling_qu.png'):
                logger.info("🔘 点击领取按钮成功")
            else:
                logger.info(f"❌ 执行【好友】-【点击领取按钮】失败")
                return False

            if find_and_click('images/hao_you/yi_jian_ling_qu.png'):
                logger.info("🎉 一键领取成功")
                close_x()
            else:
                logger.info(f"❌ 执行【好友】-【一键领取】失败")
                return False
        finally:
            close_x()



    def jun_tuan(self):
        """军团任务"""
        logger.info("执行军团任务...")
        open_jun_tuan()

        # 执行军团贡献
        if find_and_click('images/jun_tuan/gong_xian.png'):
            logger.info(f"打开【军团贡献】")
            time.sleep(1)
            if find_and_click('images/jun_tuan/gong_xian_start.png'):
                logger.info(f"开始执行【军团贡献】")
                time.sleep(35)
                close_guang_gao()
                close_chou_jiang_1()
            logger.info(f"执行【军团贡献】完成")
            close_x()
        
        # 执行砍一刀
        if find_and_click('images/jun_tuan/kan_yi_dao_start.png'):
            logger.info(f"打开【砍一刀】")
            time.sleep(1)
            if find_and_click('images/jun_tuan/kan_yi_dao.png'):
                logger.info(f"开始执行【砍一刀】")
                time.sleep(1)
                close_guang_gao()
            
            close_x_2()

        # 打开任务大厅
        if find_and_click('images/jun_tuan/task.png'):
            logger.info(f"打开【任务大厅】")
            time.sleep(1)

            # 拖拽搜索辅助方法
            def drag_search(find_image, drag_config, direction, max_attempts=3):
                """统一拖拽搜索逻辑"""
                for i in range(max_attempts):
                    logger.info(f"🔄 第{i+1}次{direction}拖拽搜索")
                    time.sleep(1)
                    drag('images/header.png', drag_config)
                    time.sleep(1)
                    if find(find_image, confidence=0.9):
                        logger.info(f"🎯 找到{find_image}")
                        return True
                    time.sleep(1)
                
                logger.info(f"❌ 超过最大拖拽次数，未找到{find_image}")
                return False

            # 任务处理核心逻辑
            def handle_task(task_image, task_name, offset_name=None):
                """统一处理各类任务"""
                logger.info(f"🔍 开始查找{task_name}任务")
                
                # 组合拖拽策略
                search_pattern = [
                    ('jun_tuan_task_left_down', '向下', 2),
                    ('jun_tuan_task_left_up', '向上', 2)
                ]

                # 补偿策略
                # 找到图片之后，广告按钮可能会被遮挡，
                # 这里添加补偿策略，
                # 先向上，如果还有发现图片，则停止补偿，如果没有，则向下拖拽，
                bu_chang = [
                    ('jun_tuan_task_up_bu_chang', '补偿向上', 1),
                    ('jun_tuan_task_down_bu_chang', '补偿向下', 1)
                ]

                for config, direction, attempts in search_pattern:
                    if drag_search(task_image, config, direction, attempts):
                        logger.info(f"🎯 定位到{task_name}任务")
                        # 补偿
                        for bu_chang_config, bu_chang_direction, bu_chang_attempts in bu_chang:
                            if drag_search(task_image, bu_chang_config, bu_chang_direction, bu_chang_attempts):
                                logger.info(f"🎯 补偿之后，定位到{task_name}任务")
                                break
                        
                        find_and_click(task_image, offset_name=offset_name, confidence=0.9)
                        time.sleep(35)
                        close_guang_gao()
                        close_chou_jiang_1()
                        return True
                return False
            
            # 优先处理100钻石任务
            if not handle_task('images/jun_tuan/task_100_zuan_shi.png', 
                             '100钻石', 'jun_tuan_task_100_zuan_shi'):
                logger.warning("💎 未找到钻石任务，尝试查找宝箱任务")
                handle_task('images/jun_tuan/task_2_bao_xiang.png', 
                          '双宝箱', 'jun_tuan_task_2_bao_xiang')

            close_x()

        logger.info("🏁 军团任务执行完毕")
        open_zhan_dou()


    def shop(self):
        """商店"""
        logger.info("执行【商店】任务...")

        # 打开商店
        time.sleep(1)
        if not open_shop():
            logger.info(f"打开【商店】失败")
            return

        # 领取2次宝箱
        for i in range(2):
            if find_and_click('images/shop/bao_xiang.png'):
                logger.info(f"第{i+1}次领取宝箱")
                time.sleep(35)
                close_guang_gao()
                close_chou_jiang_1()
        
        # 拖拽到最底部
        drag('images/header.png', 'shop')

        time.sleep(1)
        find_and_click('images/shop/gold_2.png')
        close_chou_jiang_1()

        time.sleep(1)
        if find_and_click('images/shop/gold_1.png'):
            logger.info(f"领取【金币】-观看广告")
            time.sleep(35)
            close_guang_gao()
            close_chou_jiang_1()
            
        
        open_zhan_dou()

    def gybz(self):
        """观影宝藏"""
        logger.info("执行【观影宝藏】任务...")
        open_zhan_dou()

        if find_and_click('images/guan_ying_bao_zang/open.png'):
            time.sleep(1)
            logger.info(f"打开【观影宝藏】")
        else:
            logger.info(f"打开【观影宝藏】失败")
            return False

        # 执行5次
        for i in range(5):
            if find('images/guan_ying_bao_zang/end.png', confidence=0.95):
                logger.info(f"【观影宝藏】已经执行完毕 images/guan_ying_bao_zang/end.png")
                time.sleep(1)
                break

            logger.info(f"第{i+1}次执行【观影宝藏】")

            if find_and_click('images/guan_ying_bao_zang/start.png', confidence=0.9):
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
        find_and_click('images/guan_ying_bao_zang/back.png')

    def sai_ji(self):
        """执行【赛季】任务"""
        logger.info("执行【赛季】任务...")

        open_sai_ji()

        time.sleep(4)

        if find_and_click('images/sai_ji/zheng_zhan.png'):
            logger.info(f"打开【赛季-征战】")
            time.sleep(2)
            if find_and_click('images/sai_ji/add_xing_dong_num.png'):
                time.sleep(2)
                if find_and_click('images/sai_ji/kan_guang_gao.png'):
                    logger.info(f"看广告，增加行动次数")
                    kan_guang_gao()
                time.sleep(1)
                close_x()
            back()
        
        open_zhan_dou()
            

def main():
    parser = argparse.ArgumentParser(description='通用任务执行器')
    parser.add_argument('--tasks', type=str, default='all',
                      help='指定要执行的任务（多个用逗号分隔），可选值：ads,patrol,coins,chicken,legion')
    args = parser.parse_args()

    CommonTask().run(args.tasks)

if __name__ == '__main__':
    main()