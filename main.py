# 简化后的主入口文件
from modules.huan_qiu import HuanQiu
import time
from tqdm import tqdm
from modules.common_task import CommonTask
from modules.bao_xiang import BaoXiang
from utils.logger import get_logger
import argparse
from config import FU_CONFIGS
from modules.operators.fu import xuan_fu
from modules.operators.bottom import (
    open_zhan_dou
)
from modules.operators.common_operations import (
   close_x,
   close_x_2,
)
from utils.image_utils import (
    find
)

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description='主程序入口')
    # 新增服务器切换参数
    parser.add_argument('--fu', action='store_true', 
                      help='启用多服务器切换模式（需要配置FU_CONFIGS）')
    parser.add_argument('--wait-time', type=int, default=60,
                  help='通用等待时间（单位：分钟，默认10分钟）')
    parser.add_argument('--wait', action='store_true', 
                  help='等待多久开始游戏（默认60分钟）')

    # group = parser.add_mutually_exclusive_group(required=False)  # 修改为不强制要求参数
    
    # 寰球救援参数组
    parser.add_argument('--huanqiu', action='store_true')
    # 新增帮助说明
    parser.add_argument('-n', '--number', type=int, default=40,
                      help='寰球救援执行次数（默认40次）')
    parser.add_argument('--disable-skill', action='store_true',
                      help='寰球救援-禁用技能选择功能')

    # 通用任务参数组
    parser.add_argument('--tasks', type=str, nargs='?', const='all')
    parser.add_argument('--exclude', type=str, default=None, 
                      help='需要排除的任务列表，逗号分隔（如：ads,ti_li）')

    parser.add_argument('--bao-xiang', action='store_true')
    parser.add_argument('--bao-xiang-num', type=int, default=10,
                      help='宝箱10连抽的次数（默认10次）')

    args = parser.parse_args()

    # 1. 都指定了，都执行
    # 2. 都没指定，默认执行寰球救援
    # 3. 只指定了一个，执行对应的任务

    # 新增无参数时的默认逻辑
    if not args.huanqiu and args.tasks is None and not args.bao_xiang:
        logger.info("🔍 检测到未指定任务，默认执行寰球救援")
        args.huanqiu = True

    # 打印参数
    logger.info("📦 运行时参数配置")
    logger.info(f"├─ ⏳ 等待逻辑: {'🟢 启用' if args.wait else '🔴 禁用'}")
    logger.info(f"│  └─ 等待时长: {args.wait_time}分钟")
    logger.info(f"├─ 🌐 多服务器模式: {'' if args.fu else '不'}启用")
    logger.info(f"├─ 🚀 寰球救援任务: {'✅ 启用' if args.huanqiu else '❌ 禁用'}")
    logger.info(f"│  ├─ 执行次数: {args.number}次")
    logger.info(f"│  └─ 技能系统: {'🔴 禁用' if args.disable_skill else '🟢 启用'}")
    logger.info(f"├─ 🛠️ 通用任务: {'✅ 启用' if args.tasks is not None else '❌ 禁用'}")
    logger.info(f"│  └─ 排除项目: {args.exclude or '无'}")
    logger.info(f"├─ 宝箱任务: {'✅ 启用' if args.bao_xiang else '❌ 禁用'}")
    logger.info(f"   └─ 10连抽次数: {args.bao_xiang_num}次")

    if args.wait:
        try:
            wait_minutes = args.wait_time
            wait_seconds = wait_minutes * 60
            start_time = time.time()

            logger.info(f"⏳ 开始等待 {args.wait_time} 分钟...")
            with tqdm(total=wait_seconds, desc="等待进度", unit="s") as pbar:
                for _ in range(wait_seconds):
                    time.sleep(1)
                    pbar.update(1)
        except KeyboardInterrupt:
            used_time = time.time() - start_time
            logger.warning(f"\n⚠️ 用户主动中断等待 (已等待 {used_time:.1f} 秒)")
        finally:
            logger.info("✅ 等待阶段完成\n")

    # 增加 close_x
    open_zhan_dou()
    retry_count = 0
    max_retries = 6
    while not ( find('images/fu/start_game.png') or find('images/fu/start_game_1.png') ):
        if retry_count >= max_retries:
            logger.error(f"🛑 超过最大重试次数（{max_retries}次），启动失败")
            return False

        logger.warning(f"⚠️ 未找到【开始游戏】按钮 | 第{retry_count+1}次尝试关闭弹窗...")
        close_x()
        time.sleep(4)
        open_zhan_dou()
        retry_count += 1

    def run():
        """统一任务执行方法"""
        if args.bao_xiang:
            logger.info(f"🎁 开始执行 宝箱 任务 | 璀璨宝箱10连抽次数: {args.bao_xiang_num}")
            BaoXiang(max_num=args.bao_xiang_num).run()
            logger.info("✅ 宝箱任务执行完毕")

        # 执行常规任务
        if args.tasks is not None:
            logger.info(f"🛠️ 开始执行通用任务 | 任务列表: {args.tasks or 'all'} | 排除任务: {args.exclude or '无'}")
            CommonTask().run(
                args.tasks if args.tasks != '' else 'all',
                exclude=args.exclude
            )
            logger.info("✅ 通用任务执行完毕")

        # 执行寰球救援任务
        if args.huanqiu:
            logger.info(f"🚚 启动寰球救援 | 次数: {args.number} | 禁用技能: {'是' if args.disable_skill else '否'}")
            HuanQiu(max_num=args.number, disable_skill=args.disable_skill).start()
            logger.info("🎉 寰球救援任务完成")

    if args.fu:
        if not FU_CONFIGS:
            logger.error("‼️ 配置错误：未在config.py中配置FU_CONFIGS，多服务器模式不可用")
            return
            
        logger.info(f"🌐 进入多服务器模式 | 已配置服务器: {len(FU_CONFIGS)}个")
        for idx, config in enumerate(FU_CONFIGS, 1):
            server_name = config.get('name', '未命名')
            logger.info(f"🔄 [{idx}/{len(FU_CONFIGS)}] 正在切换服务器: {server_name}")
            
            if xuan_fu(config['image_path'], config.get('confidence', 0.8)):
                logger.info(f"🔗 服务器 {server_name} 连接成功")
                run()
            else:
                logger.error(f"💥 服务器 {server_name} 切换失败，跳过后续操作")
                continue
    else:
        logger.info("🏃 进入单服务器模式")
        run()

if __name__ == "__main__":
    main()