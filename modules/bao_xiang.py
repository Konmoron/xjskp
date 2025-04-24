import argparse
from utils.image_utils import find, find_and_click
from utils.logger import get_logger
import time
from .operators.bottom import (
    open_zhan_dou,
    open_shop,
)
from .operators.common_operations import (
   back,
)
    

logger = get_logger()

class BaoXiang:
    """
    BaoXiang 类用于执行 抽宝箱 任务。
    执行逻辑：
    1. 先抽66次普通宝箱；
    2. 再抽3次璀璨宝箱；
    3. 再10次10连抽璀璨宝箱；
    """
    def __init__(self, max_num=10):
        """
        初始化 BaoXiang 类，加载配置文件。
        :param max_num: 最大执行次数，默认为 1。
        """
        self.max_num = max_num

    def run(self):
        """
        执行 宝箱 任务的主要逻辑。
        """
        logger.info("🎁 开始执行 宝箱 任务")

        open_shop()

        # 执行 66 次普通宝箱
        logger.info("🔄 执行 20 次普通宝箱")
        find_and_click("./images/bao_xiang/pu_tong_1.png")
        for _ in range(20):
            find_and_click("./images/bao_xiang/lian_xu_pu_tong_1.png")

        back()

        # 执行 3 次璀璨宝箱
        logger.info("🔄 执行 3 次璀璨宝箱")
        find_and_click("./images/bao_xiang/cui_can_1.png")
        for _ in range(3):
            find_and_click("./images/bao_xiang/lian_xu_cui_can_1.png")

        # 执行 10 次 10 连璀璨宝箱
        logger.info(f"🔄 执行 {self.max_num} 次 10 连璀璨宝箱")
        for _ in range(self.max_num):
            find_and_click("./images/bao_xiang/lian_xu_cui_can_10.png")
            
        back()

        open_zhan_dou()

def main():
    """
    主函数，解析命令行参数并执行任务。
    命令行参数：
    -n, --number: 执行次数，默认为 1。
    使用示例：
    python -m modules.bao_xiang
    """
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="宝箱任务执行器")
    parser.add_argument("-n", "--number", type=int, default=1, help="执行次数")
    args = parser.parse_args()
    # 创建 BaoXiang 实例并执行任务
    bao_xiang = BaoXiang(max_num=args.number)
    bao_xiang.run()
    
# end def

if __name__ == "__main__":
    main()
