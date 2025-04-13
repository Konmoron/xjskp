import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import DRAG_CONFIGS
from utils.image_utils import drag
from utils.logger import get_logger
import argparse

logger = get_logger()

def test_drag_config(img_path: str, config_name: str):
    """测试单个拖拽配置"""
    logger.info(f"🔍 开始测试配置项：{config_name} | 图片路径: {img_path}")
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    config = DRAG_CONFIGS.get(config_name)
    if not config:
        logger.error(f"❌ 配置 '{config_name}' 不存在于DRAG_CONFIGS中")
        return False

    try:
        x_offset, y_offset, drag_x, drag_y, duration, times = config
        logger.debug("📋 当前测试配置参数:")
        logger.debug(f"→ 偏移量 X: {x_offset} Y: {y_offset}")
        logger.debug(f"→ 拖拽距离 X: {drag_x} Y: {drag_y}")
        logger.debug(f"→ 持续时间: {duration}s 次数: {times}次")
        
        logger.info("🔄 正在执行拖拽操作...")
        result = drag(
            image_path=img_path, 
            x_offset=x_offset,
            y_offset=y_offset,
            drag_x=drag_x,
            drag_y=drag_y,
            times=times,
            duration=duration
        )
        
        if result:
            logger.info(f"✅ 测试通过 [{config_name}]")
        else:
            logger.error(f"❌ 测试失败 [{config_name}]")
        return result
        
    except ValueError as e:
        logger.error(f"‼️ 配置格式错误: {str(e)}")
        logger.error(f"当前配置值: {config}")
        return False
    except Exception as e:
        logger.error(f"‼️ 发生意外错误: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='拖拽配置测试工具')
    # 新增图片路径参数
    parser.add_argument('-i', '--image', required=True, 
                      help='基准图片路径')
    parser.add_argument('-c', '--config-name', required=True,
                      help='配置名称（支持all测试全部）')
    
    args = parser.parse_args()
    
    # 新增参数日志输出
    logger.info("📌 命令行参数:")
    logger.info(f"→ 基准图片: {args.image}")
    logger.info(f"→ 配置名称: {args.config_name}")
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    test_drag_config(args.image, args.config_name)