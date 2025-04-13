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

    args = parser.parse_args()

    # 新增无参数时的默认逻辑
    if not args.huanqiu and args.tasks is None:
        logger.info("检测到未指定任务，默认执行寰球救援")
        args.huanqiu = True

    if args.huanqiu:
        HuanQiu(max_num=args.number, disable_skill=args.disable_skill).start()
    elif args.tasks is not None:
        CommonTask().run(args.tasks if args.tasks != '' else 'all')

if __name__ == "__main__":
    main()