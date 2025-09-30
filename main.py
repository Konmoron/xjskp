import sys
from modules.huan_qiu import HuanQiu
from modules.zhu_xian import ZhuXian
import time
from tqdm import tqdm
from modules.common_task import CommonTask
from modules.bao_xiang import BaoXiang
from utils.logger import get_logger
import argparse
from config import FU_CONFIGS
from modules.operators.fu import xuan_fu
from modules.operators.bottom import open_zhan_dou
from modules.operators.common_operations import (
    close_all_x_and_back,
    close_all_x,
    check_login_other,
    force_login,
    is_game_started,
    start_game,
    exit_game,
)
from utils.image_utils import find

logger = get_logger()


class TaskExecutor:
    """任务执行器"""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        # 添加游戏启动时间记录（需要在main函数中传递）
        self.game_start_time = time.time()

    def run_bao_xiang(self):
        """宝箱任务"""
        if not self.args.bao_xiang:
            return
        BaoXiang(max_num=self.args.bao_xiang_num).run()
        logger.info("🎁 宝箱任务执行完毕")

    def run_common_tasks(self):
        """通用任务"""
        if self.args.tasks is None:
            return
        CommonTask().run(self.args.tasks or "all", exclude=self.args.exclude)
        logger.info("🛠️ 通用任务执行完毕")

    def run_huan_qiu(self):
        """寰球救援"""
        if not self.args.huanqiu:
            return
        CommonTask().run("ling_yuan_zheng_piao,shi_lian_ta", "")
        HuanQiu(
            max_num=self.args.number,
            disable_skill=self.args.disable_skill,
            force_login=not self.args.disable_force_login,
            force_login_wait=self.args.force_login_wait or 10,
            force_start=not self.args.disable_force_start,
        ).start()

        close_all_x_and_back()
        CommonTask().run("ling_yuan_zheng_piao,shi_lian_ta", "")
        logger.info("🚀 寰球救援任务完成")

    def run_zhu_xian(self):
        """主线关卡任务"""
        if self.args.zhu_xian is None:
            return
        ZhuXian(
            max_num=self.args.zhu_xian,
            force_login=not self.args.disable_force_login,
            force_login_wait=self.args.force_login_wait or 10,
            force_start=not self.args.disable_force_start,
        ).start()
        logger.info("🏆 主线任务执行完毕")

    def execute(self):
        """统一执行入口"""
        self.run_bao_xiang()
        self.run_common_tasks()
        self.run_huan_qiu()
        self.run_zhu_xian()

        # 添加运行时间判断（30分钟 = 1800秒）
        if time.time() - self.game_start_time >= 1800:
            exit_game()
            logger.info("✅ 程序退出")
            time.sleep(30)
        else:
            logger.info("⏳ 游戏运行时间未达30分钟，保持运行")


def print_runtime_config(args: argparse.Namespace):
    """可视化输出运行时参数"""
    # 修改服务器显示逻辑
    fu_config = {
        "name": "🌐 多服务器",
        "status": args.fu is not None,
        "detail": (
            "未启用"
            if args.fu is None
            else (
                f"指定服务器: {args.fu}"
                if args.fu != "all"
                else f"启用 | 共{len(FU_CONFIGS)}个服务器"
            )
        ),
    }

    config_map = {
        "⏳ 等待逻辑": (
            args.wait is not None,
            f"{args.wait}分钟" if args.wait is not None else "未启用",
        ),
        "🌐 多服务器": (fu_config["status"], fu_config["detail"]),
        "🔒 强制登录": (
            not args.disable_force_login,
            (
                f"等待{args.force_login_wait}分钟后强制登录"
                if not args.disable_force_login
                else "禁用"
            ),
        ),
        "🚀 寰球救援": (
            args.huanqiu,
            f"次数:{args.number} 选择技能:{'禁用' if args.disable_skill else '启用'}",
        ),
        "🏆 主线任务": (args.zhu_xian is not None, f"次数:{args.zhu_xian or 20}"),
        "🎁 宝箱任务": (args.bao_xiang, f"10连抽x{args.bao_xiang_num}次"),
        "🛠️ 通用任务": (
            args.tasks is not None,
            f"任务列表:{args.tasks or 'all'} 排除:{args.exclude or '无'}",
        ),
        "⚡ 强制启动": (
            not args.disable_force_start,
            f"启用" if not args.disable_force_start else "禁用",
        ),
        "⚡ 结束退出": (
            not args.disable_exit,
            "是" if not args.disable_exit else "否",
        ),
    }

    logger.info("📦 运行时参数配置".ljust(50, "─"))
    for desc, (status, detail) in config_map.items():
        status_icon = "🟢" if status else "🔴"
        logger.info(f"├─ {desc}: {status_icon} | {detail}")
    logger.info("".ljust(50, "─"))


def run_multi_server_mode(args: argparse.Namespace):
    """多服务器模式运行"""
    # 解析服务器列表
    if args.fu == "all" or args.fu is None:
        target_servers = FU_CONFIGS
    else:
        # 解析指定的服务器列表
        target_servers = []
        requested_servers = args.fu.split(",")

        for config in FU_CONFIGS:
            if config.get("name") in requested_servers:
                target_servers.append(config)
                requested_servers.remove(config.get("name"))

        # 检查未找到的服务器
        if requested_servers:
            logger.warning(f"⚠️ 未找到以下服务器配置: {','.join(requested_servers)}")

    logger.info(f"🌐 进入多服务器模式 | 即将连接服务器: {target_servers}")

    # logger.info(f"🌐 进入多服务器模式 | 已配置服务器: {len(FU_CONFIGS)}个")

    for idx, config in enumerate(target_servers, 1):
        if not is_game_started():
            logger.info("游戏未启动，启动游戏")
            start_game()

        logger.info("关闭所有弹窗, 最大尝试次数: 6")
        close_all_x_and_back()

        server_name = config.get("name", "未命名服务器")
        logger.info(f"🔄 [{idx}/{len(FU_CONFIGS)}] 正在连接: {server_name}")

        try:
            if xuan_fu(config["image_path"], config.get("confidence", 0.8)):
                logger.info(f"🔗 服务器连接成功 | {server_name}")
                TaskExecutor(args).execute()
            else:
                logger.error(f"💥 服务器连接失败 | {server_name}")
        except Exception as e:
            logger.error(f"‼️ 服务器异常 | {server_name}: {str(e)}")
            continue


def parse_arguments() -> argparse.Namespace:
    """命令行参数解析"""
    parser = argparse.ArgumentParser(
        description="自动化任务调度系统 v2.0",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # 参数分组
    server_group = parser.add_argument_group("服务器设置")
    server_group.add_argument(
        "--fu",
        type=str,
        nargs="?",
        const="all",
        help="启用多服务器切换模式（需配置FU_CONFIGS），可指定服务器列表（如：--fu server1,server2）",
    )

    task_group = parser.add_argument_group("任务设置")
    task_group.add_argument("--huanqiu", action="store_true", help="启用寰球救援任务")
    task_group.add_argument("--bao-xiang", action="store_true", help="启用宝箱任务")
    task_group.add_argument(
        "--tasks",
        type=str,
        nargs="?",
        const="all",
        help='通用任务列表（多个用逗号分隔，"all"为全部任务）',
    )
    task_group.add_argument(
        "--zhu-xian",
        type=int,
        default=None,
        nargs="?",
        const=20,
        help="启用主线任务，可指定执行次数（默认20次）",
    )

    common_group = parser.add_argument_group("通用设置")
    common_group.add_argument(
        "--wait",
        type=int,
        default=None,
        nargs="?",
        const=60,
        help="启用启动等待（默认60分钟，可指定时长如--wait 30）",
    )
    common_group.add_argument(
        "--exclude", type=str, default=None, help="排除的任务列表（如：ads,ti_li）"
    )
    common_group.add_argument(
        "-n", "--number", type=int, default=20, help="寰球救援执行次数（默认30次）"
    )
    common_group.add_argument(
        "--bao-xiang-num", type=int, default=10, help="宝箱10连抽的次数（默认10次）"
    )
    common_group.add_argument(
        "--disable-skill", action="store_true", help="寰球救援-禁用技能选择功能"
    )
    common_group.add_argument(
        "--force-login-wait",
        type=int,
        default=10,
        help="如帐号在其他地方登录，强制登录，默认10分钟后强制登录",
    )
    common_group.add_argument(
        "--disable-force-login", action="store_true", help="禁止强制登录"
    )
    common_group.add_argument(
        "--disable-force-start", action="store_true", help="禁止强制启动游戏"
    )
    common_group.add_argument(
        "--disable-exit", action="store_true", help="任务结束之后不退出"
    )
    common_group.add_argument(
        "--platform",
        type=str,
        choices=["bao", "shou", "guan"],
        default="bao",
        help="指定游戏运行平台: bao(腾讯应用宝), shou(腾讯手游助手), guan(腾讯电脑管家)",
    )

    return parser.parse_args()


def validate_arguments(args: argparse.Namespace):
    """参数验证"""
    if args.wait is not None and args.wait < 0:
        raise ValueError("等待时间不能为负数")
    if args.fu and not FU_CONFIGS:
        raise RuntimeError("多服务器模式需要配置FU_CONFIGS")


def handle_wait(wait_minutes: int):
    """处理等待倒计时"""
    logger.info(f"⏳ 开始等待 {wait_minutes} 分钟...")
    try:
        with tqdm(
            total=wait_minutes * 60,
            desc="等待进度",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}s [{elapsed}<{remaining}]",
        ) as pbar:
            for _ in range(wait_minutes * 60):
                time.sleep(1)
                pbar.update(1)
    except KeyboardInterrupt:
        logger.warning("⚠️ 用户主动中断等待")
        raise
    finally:
        logger.info("✅ 等待阶段完成")


def init_game_environment():
    """游戏环境初始化"""
    logger.info("关闭所有弹窗, 最大尝试次数: 6")
    close_all_x()

    if not (find("images/fu/start_game.png") or find("images/fu/start_game_1.png")):
        logger.warning("🛑 未找到游戏开始按钮")
    else:
        logger.info("✅ 游戏环境初始化完成")


def main():
    try:
        args = parse_arguments()
        validate_arguments(args)

        # 无参数默认逻辑
        if not any(
            [
                args.huanqiu,
                args.bao_xiang,
                args.tasks is not None,
                args.zhu_xian is not None,
            ]
        ):
            logger.info("🔍 未指定任务参数，默认执行寰球救援")
            args.huanqiu = True

        print_runtime_config(args)

        # 等待逻辑
        if args.wait is not None:
            handle_wait(args.wait)

        if not args.disable_force_start:
            logger.info("⏳ 退出游戏...")
            exit_game()
            logger.info("⏳ 重新启动游戏...")
            start_game()

        if check_login_other():
            logger.info(
                f"⚠️ 检测到帐号在其他地方登录，等待{args.force_login_wait}分钟后强制登录"
            )
            force_login(args.force_login_wait)

        # 初始化游戏环境
        init_game_environment()

        # 执行任务
        if args.fu:
            run_multi_server_mode(args)
        else:
            TaskExecutor(args).execute()
    except Exception as e:
        logger.error(f"‼️ 程序异常终止: {str(e)}")
        sys.exit(1)
    finally:
        if not args.disable_exit:
            logger.info("⏳ 所有任务执行完毕，退出游戏...")
            exit_game()


if __name__ == "__main__":
    main()
