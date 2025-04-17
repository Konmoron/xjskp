import argparse
from nt import close
from typing import Dict, Callable
from utils.image_utils import find, find_and_click, drag
from utils.logger import get_logger
import time
from .operators.bottom import (
    open_zhan_dou,
    open_jun_tuan,
    open_shop,
)
from .operators.common_operations import (
   close_guang_gao, 
   close_chou_jiang_1,
   close_x,
   close_x_2,
   back,
)
from config import DRAG_CONFIGS
    

logger = get_logger()

class CommonTask:
    def __init__(self):
        self.task_registry: Dict[str, Callable] = {
            'ti_li': self.ti_li,
            'jun_tuan': self.jun_tuan,
            'gybz': self.gybz,
            'shop': self.shop,
            'huo_dong': self.huo_dong,
        }

    def run(self, tasks: str = 'all', exclude: str = None):
        """执行任务调度入口
        :param exclude: 需要排除的任务列表（逗号分隔）
        """
        selected_tasks = self._parse_tasks(tasks)
        exclude_list = [t.strip() for t in (exclude.split(',') if exclude else [])]
        
        # 过滤排除任务
        final_tasks = [t for t in selected_tasks if t not in exclude_list]
        
        # 确保ti_li任务最后执行（如果存在）
        if 'ti_li' in final_tasks:
            final_tasks.remove('ti_li')
            final_tasks.append('ti_li')
        
        logger.info(f"排除任务：{exclude_list} | 最终执行任务：{', '.join(final_tasks)}")
        
        task_durations = {}  # 存储任务耗时
        start_total = time.time()  # 总开始时间
        
        for task_name in final_tasks:
            if task_name in self.task_registry:
                start_time = time.time()
                self.task_registry[task_name]()
                task_durations[task_name] = time.time() - start_time
            else:
                logger.warning(f"未知任务：{task_name}")
        
        # 输出汇总信息
        total_duration = time.time() - start_total
        logger.info("📊 任务执行时间汇总：")
        for task, duration in task_durations.items():
            # 超过60秒的转换为分钟显示
            if duration >= 60:
                mins, secs = divmod(duration, 60)
                logger.info(f"→ {task}: {int(mins)}分{secs:.2f}秒")
            else:
                logger.info(f"→ {task}: {duration:.2f}秒")
        
        # 总耗时超过60秒时显示分钟格式
        if total_duration >= 60:
            total_mins, total_secs = divmod(total_duration, 60)
            logger.info(f"⏱️ 总耗时: {int(total_mins)}分{total_secs:.2f}秒")
        else:
            logger.info(f"⏱️ 总耗时: {total_duration:.2f}秒")

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
            if find('images/huo_dong/button.png', confidence=0.9):
                logger.info(f"找到【活动】")
                found = True
                break
            
            # 执行拖拽
            # 向上拖拽3次，
            # 向下拖拽3次，
            if find_num < 3:
                logger.info(f"找活动 - 向上拖拽 {find_num} 次")
                drag('images/header.png', 'zhan_dou_left_up')
            
            if find_num >= 3:
                logger.info(f"找活动 - 向下拖拽 {find_num} 次")
                drag('images/header.png', 'zhan_dou_left_down')
            
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

    def ti_li(self):
        """领体力任务"""
        logger.info("执行领体力任务...")
        time.sleep(1)
        
        # 打开【体力】
        if find_and_click('images/header.png', offset_name='open_ti_li'):
            time.sleep(1)
            logger.info(f"打开【体力】")
        else:
            logger.info(f"打开【体力】失败")
            return False

        # 领取3次
        for i in range(3):
            if find('images/ti_li/end.png', confidence=0.95):
                logger.info(f"领取【体力】已经执行完毕 images/ti_li/end.png")
                time.sleep(1)
                break

            if find_and_click('images/ti_li/start.png', confidence=0.8):
                logger.info(f"第{i+1}次领取体力 - 打开【观看广告】...")
                time.sleep(35)
                close_guang_gao()
                close_chou_jiang_1()
                logger.info(f"第{i+1}次领取体力成功")
                # 等待5分钟
                if i < 2:
                    if find('images/ti_li/end.png', confidence=0.9):
                        logger.info(f"领取【体力】已经执行完毕 images/ti_li/end.png")
                        time.sleep(1)
                        break
                    
                    logger.info(f"等待5分钟")
                    time.sleep(310)
        
        # 关闭
        close_x()

    def jun_tuan(self):
        """军团任务"""
        logger.info("执行军团任务...")
        open_jun_tuan()

        # 执行军团贡献
        if find_and_click('images/jun_tuan/gong_xian.png', confidence=0.9):
            logger.info(f"打开【军团贡献】")
            time.sleep(1)
            if find_and_click('images/jun_tuan/gong_xian_start.png', confidence=0.9):
                logger.info(f"开始执行【军团贡献】")
                time.sleep(35)
                close_guang_gao()
                close_chou_jiang_1()
            logger.info(f"执行【军团贡献】完成")
            close_x()
        
        # 执行砍一刀
        if find_and_click('images/jun_tuan/kan_yi_dao_start.png', confidence=0.9):
            logger.info(f"打开【砍一刀】")
            time.sleep(1)
            if find_and_click('images/jun_tuan/kan_yi_dao.png'):
                logger.info(f"开始执行【砍一刀】")
                time.sleep(1)
                close_guang_gao()
            
            close_x_2()

        # 打开任务大厅
        if find_and_click('images/jun_tuan/task.png', confidence=0.9):
            logger.info(f"打开【任务大厅】")
            time.sleep(1)

            # 拖拽搜索辅助方法
            def drag_search(drag_config, direction, max_attempts=3):
                """统一拖拽搜索逻辑"""
                for i in range(max_attempts):
                    logger.info(f"🔄 第{i+1}次{direction}拖拽搜索")
                    drag('images/header.png', drag_config)
                    time.sleep(1)

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
                    drag_search(config, direction, attempts)
                    if find(task_image, confidence=0.9):

                        logger.info(f"🎯 定位到{task_name}任务")
                        # 补偿
                        for bu_chang_config, bu_chang_direction, bu_chang_attempts in bu_chang:
                            drag_search(bu_chang_config, bu_chang_direction, bu_chang_attempts)
                            if find(task_image, confidence=0.9):
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

def main():
    parser = argparse.ArgumentParser(description='通用任务执行器')
    parser.add_argument('--tasks', type=str, default='all',
                      help='指定要执行的任务（多个用逗号分隔），可选值：ads,patrol,coins,chicken,legion')
    args = parser.parse_args()

    CommonTask().run(args.tasks)

if __name__ == '__main__':
    main()