# 简化后的主入口文件
from modules.huan_qiu import HuanQiu
from utils.logger import get_logger

logger = get_logger()

if __name__ == "__main__":
    HuanQiu().start()