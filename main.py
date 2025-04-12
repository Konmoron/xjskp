# 简化后的主入口文件
from modules.huan_qiu import HuanQiu
from modules.common_task import CommonTask
from utils.logger import get_logger
import argparse

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description='主程序入口')
    group = parser.add_mutually_exclusive_group(required=True)
    
    # 寰球救援参数组
    group.add_argument('--huanqiu', action='store_true')
    parser.add_argument('-n', '--number', type=int, default=40,
                      help='寰球救援执行次数（仅--huanqiu时有效）')
    parser.add_argument('--disable-skill', action='store_true',  # 移动到此
                      help='禁用技能选择功能（仅--huanqiu时有效）')
    
    # 通用任务参数组
    group.add_argument('--tasks', type=str, nargs='?', const='all')
    
    args = parser.parse_args()

    if args.huanqiu:
        # 传递参数到HuanQiu类
        HuanQiu(max_num=args.number, disable_skill=args.disable_skill).start()
    elif args.tasks is not None:
        CommonTask().run(args.tasks if args.tasks != '' else 'all')

if __name__ == "__main__":
    main()