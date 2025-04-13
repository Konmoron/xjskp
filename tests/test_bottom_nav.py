from modules.operators.bottom_nav_view import open_zhan_dou
from utils.logger import get_logger

logger = get_logger()

def test_open_zhan_dou():
    logger.info("开始测试战斗按钮点击...")
    result = open_zhan_dou()
    
    if result:
        logger.info("✅ 测试通过 - 成功找到并点击战斗按钮")
    else:
        logger.warning("❌ 测试失败 - 未找到战斗按钮图片")

if __name__ == "__main__":
    test_open_zhan_dou()