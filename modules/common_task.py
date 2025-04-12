import argparse
from typing import Dict, Callable
from utils.logger import get_logger

logger = get_logger()

class CommonTask:
    def __init__(self):
        self.task_registry: Dict[str, Callable] = {
            'ads': self.watch_ads,
            'patrol': self.patrol_car,
            'coins': self.collect_coins,
            'chicken': self.collect_chicken,
            'legion': self.legion_mission
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

def main():
    parser = argparse.ArgumentParser(description='通用任务执行器')
    parser.add_argument('--tasks', type=str, default='all',
                      help='指定要执行的任务（多个用逗号分隔），可选值：ads,patrol,coins,chicken,legion')
    args = parser.parse_args()

    CommonTask().run(args.tasks)

if __name__ == '__main__':
    main()