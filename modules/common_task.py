import argparse
from typing import Dict, Callable
from modules.operators.common_operations import open_chat
from utils.image_utils import find, find_and_click
from utils.logger import get_logger
import time
from .operators.bottom_nav_view import (
    open_zhan_dou,
)
    

logger = get_logger()

class CommonTask:
    def __init__(self):
        self.task_registry: Dict[str, Callable] = {
            'ads': self.watch_ads,
            'patrol': self.patrol_car,
            'coins': self.collect_coins,
            'chicken': self.collect_chicken,
            'legion': self.legion_mission,
            'gybz': self.gybz
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

    def collect_chicken(self):
        """领鸡腿任务"""
        logger.info("执行领鸡腿任务...")
        # 具体实现代码...

    def legion_mission(self):
        """军团任务"""
        logger.info("执行军团任务...")
        # 具体实现代码...
    
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
                logger.info(f"第{i+1}次 关闭【观看广告】")
                find_and_click('images/header.png', offset_name='close_guang_gao_1')
                logger.info(f"第{i+1}次 等待抽奖")
                time.sleep(5)
                find_and_click('images/header.png', offset_name='close_chou_jiang_1')
                time.sleep(1)
                logger.info(f"第{i+1}次【观影宝藏】执行完成")

        # 返回
        find_and_click('images/common_task/guan_ying_bao_zang/back.png')

def main():
    parser = argparse.ArgumentParser(description='通用任务执行器')
    parser.add_argument('--tasks', type=str, default='all',
                      help='指定要执行的任务（多个用逗号分隔），可选值：ads,patrol,coins,chicken,legion')
    args = parser.parse_args()

    CommonTask().run(args.tasks)

if __name__ == '__main__':
    main()