# 简化后的主入口文件
from modules.huan_qiu import HuanQiu
from modules.common_task import CommonTask
from utils.logger import get_logger
import argparse

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description='主程序入口')
    group = parser.add_mutually_exclusive_group(required=False)  # 修改为不强制要求参数
    
    # 寰球救援参数组
    group.add_argument('--huanqiu', action='store_true')
    # 新增帮助说明
    parser.add_argument('-n', '--number', type=int, default=40,
                      help='寰球救援执行次数（默认40次）')
    parser.add_argument('--disable-skill', action='store_true',
                      help='寰球救援-禁用技能选择功能')

    # 通用任务参数组
    group.add_argument('--tasks', type=str, nargs='?', const='all')
    parser.add_argument('--exclude', type=str, default=None, 
                      help='需要排除的任务列表，逗号分隔（如：ads,ti_li）')

    args = parser.parse_args()

    # 1. 都指定了，都执行
    # 2. 都没指定，默认执行寰球救援
    # 3. 只指定了一个，执行对应的任务

    # 新增无参数时的默认逻辑
    if not args.huanqiu and args.tasks is None:
        logger.info("检测到未指定任务，默认执行寰球救援")
        args.huanqiu = True

    if args.tasks is not None:
        logger.info(f"执行任务：{args.tasks}")
        CommonTask().run(
            args.tasks if args.tasks != '' else 'all',
            exclude=args.exclude
        )

    if args.huanqiu:
        HuanQiu(max_num=args.number, disable_skill=args.disable_skill).start()

if __name__ == "__main__":
    main()