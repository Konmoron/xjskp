import argparse
from typing import Dict, Callable
from utils.image_utils import find, find_and_click, drag
from utils.logger import get_logger
import time
from .operators.bottom_nav_view import (
    open_zhan_dou,
    open_jun_tuan,
    open_shop,
)
from .operators.common_operations import (
   close_guang_gao, 
   close_chou_jiang_1,
   close_x,
)
from config import DRAG_CONFIGS
    

logger = get_logger()

class CommonTask:
    def __init__(self):
        self.task_registry: Dict[str, Callable] = {
            'ads': self.watch_ads,
            'patrol': self.patrol_car,
            'coins': self.collect_coins,
            'ti_li': self.ti_li,
            'jun_tuan': self.jun_tuan,
            'gybz': self.gybz,
            'shop': self.shop,
            'huo_dong': self.huo_dong,
        }

    def run(self, tasks: str = 'all'):
        """执行任务调度入口"""
        selected_tasks = self._parse_tasks(tasks)
        
        logger.info(f"开始执行任务：{', '.join(selected_tasks)}")
        for task_name in selected_tasks:
            if task_name in self.task_registry:
                self.task_registry[task_name]()
            else:
                logger.warning(f"未知任务：{task_name}")

    def _parse_tasks(self, tasks: str) -> list:
        """解析任务参数"""
        if tasks.lower() == 'all':
            return list(self.task_registry.keys())
        return [t.strip() for t in tasks.split(',')]

    def watch_ads(self):
        """看广告任务"""
        logger.info("执行看广告任务...")
        # 具体实现代码...

    def patrol_car(self):
        """巡逻车任务"""
        logger.info("执行巡逻车任务...")
        # 具体实现代码...

    def collect_coins(self):
        """领金币任务"""
        logger.info("执行领金币任务...")
        # 具体实现代码...

    def huo_dong():
        """执行【战斗-活动】任务"""
        logger.info("执行【战斗-活动】任务...")


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
                    logger.info(f"等待5分钟")
                    time.sleep(310)
        
        # 关闭
        close_x()

    def jun_tuan(self):
        """军团任务"""
        logger.info("执行军团任务...")
        open_jun_tuan()

        # 执行军团贡献
        if find_and_click('images/jun_tuan/gong_xian.png', confidence=0.95):
            logger.info(f"打开【军团贡献】")
            time.sleep(1)
            if find_and_click('images/jun_tuan/gong_xian_start.png', confidence=0.95):
                logger.info(f"开始执行【军团贡献】")
                time.sleep(35)
                close_guang_gao()
                close_chou_jiang_1()
            logger.info(f"执行【军团贡献】完成")
            close_x()

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

        if find_and_click('images/common_task/guan_ying_bao_zang/open.png'):
            time.sleep(1)
            logger.info(f"打开【观影宝藏】")
        else:
            logger.info(f"打开【观影宝藏】失败")
            return False

        # 执行5次
        for i in range(5):
            if find('images/common_task/guan_ying_bao_zang/end.png', confidence=0.95):
                logger.info(f"【观影宝藏】已经执行完毕 images/common_task/guan_ying_bao_zang/end.png")
                time.sleep(1)
                break

            logger.info(f"第{i+1}次执行【观影宝藏】")

            if find_and_click('images/common_task/guan_ying_bao_zang/start.png', confidence=0.9):
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
        find_and_click('images/common_task/guan_ying_bao_zang/back.png')

def main():
    parser = argparse.ArgumentParser(description='通用任务执行器')
    parser.add_argument('--tasks', type=str, default='all',
                      help='指定要执行的任务（多个用逗号分隔），可选值：ads,patrol,coins,chicken,legion')
    args = parser.parse_args()

    CommonTask().run(args.tasks)

if __name__ == '__main__':
    main()