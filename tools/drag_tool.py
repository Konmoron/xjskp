import pyautogui
import sys
from pathlib import Path
import time
import argparse
sys.path.append(str(Path(__file__).parent.parent))
from config import DRAG_CONFIGS
from utils.logger import get_logger
from utils.image_utils import drag

logger = get_logger()

def measure_drag_distance(image_path, confidence=0.8):
    """测量拖拽距离工具"""
    logger.info(f"📏 开始测量拖拽距离 | 图片: {image_path} | 置信度: {confidence}")
    logger.info("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    try:
        # 定位基准图片
        logger.debug(f"🔍 正在定位基准图片: {image_path}")
        start_time = time.time()
        image_location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=confidence
        )
        elapsed = time.time() - start_time
        
        if not image_location:
            logger.error(f"❌ 未找到基准图片: {image_path}")
            logger.warning("可能原因: 1.图片路径错误 2.图片未显示 3.置信度过高")
            return False
            
        logger.info(f"✅ 图片定位成功 | 耗时: {elapsed:.2f}s | 位置: ({image_location.x}, {image_location.y})")

        # 计算初始位置
        image_pos_x = image_location.x
        image_pos_y = image_location.y
        logger.debug(f"📐 基准坐标计算完成: X={image_pos_x}, Y={image_pos_y}")

        # 移动鼠标到目标位置
        logger.info("🖱️ 正在移动鼠标到基准位置...")
        pyautogui.moveTo(image_pos_x, image_pos_y)
        logger.info("⏳ 请在10秒内将鼠标挪到拖拽的开始位置...")
        time.sleep(10)
        
        # 记录拖拽前坐标
        start_pos = pyautogui.position()
        logger.info(f"📍 拖拽起始点坐标: X={start_pos.x}, Y={start_pos.y}")
        logger.info(f"⏳ 请在10秒内完成拖拽操作...")
        time.sleep(10)
        
        # 记录拖拽后坐标
        end_pos = pyautogui.position()
        logger.info(f"🏁 拖拽结束点坐标: X={end_pos.x}, Y={end_pos.y}")
        
        # 计算拖拽距离
        dx = end_pos.x - start_pos.x
        dy = end_pos.y - start_pos.y
        logger.info(f"📏 拖拽距离计算完成 | 水平: {dx}px | 垂直: {dy}px")
        
        # 计算相对基准图片的偏移
        offset_x = start_pos.x - image_pos_x
        offset_y = start_pos.y - image_pos_y
        logger.info("📋 本次拖拽完整信息:")
        logger.info(f"→ 基准图片偏移: X={offset_x}, Y={offset_y}")
        logger.info(f"→ 拖拽距离: X={dx}, Y={dy}")
        logger.info(f"→ 推荐配置: ({offset_x}, {offset_y}, {dx}, {dy}, 1)")
        
        return True

    except pyautogui.ImageNotFoundException:
        logger.error("‼️ 图片查找失败，请检查图片路径和显示状态")
        return False
    except pyautogui.FailSafeException:
        logger.error("🛑 触发了安全保护机制，请确保鼠标可以自由移动")
        return False
    except Exception as e:
        logger.error(f"‼️ 发生未预期错误: {str(e)}", exc_info=True)
        return False

def test_drag_config(img_path: str, config_name: str, confidence=0.8, region_name='default'):
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
            drag_config_name=config_name,
            confidence=confidence,
            image_region_name=region_name
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
    parser = argparse.ArgumentParser(description='拖拽工具集')
    
    # 必需参数
    parser.add_argument('-i', '--image', required=True, help='基准图片路径')
    parser.add_argument('-r', '--region-name', default='default', help='图片区域名称')
    
    # 互斥操作模式
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--get', action='store_true', help='测量拖拽距离')
    group.add_argument('--test', action='store_true', help='测试拖拽配置')
    
    # 可选参数
    parser.add_argument('-c', '--confidence', type=float, default=0.8,
                      help='图像匹配精度 (0-1)，默认0.8')
    parser.add_argument('-d', '--drag', help='配置名称（test模式必需）')
    
    args = parser.parse_args()
    
    # 参数验证
    if args.test and not args.drag:
        parser.error("test模式需要指定-d参数")
    
    # 执行对应操作
    if args.get:
        measure_drag_distance(args.image, args.confidence)
    elif args.test:
        test_drag_config(args.image, args.drag, args.confidence, args.region_name)