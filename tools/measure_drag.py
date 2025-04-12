import pyautogui
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.logger import get_logger
import time

logger = get_logger()

def measure_drag_distance(image_path):
    try:
        # 定位基准图片
        image_location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=0.8
        )
        
        if not image_location:
            logger.warning(f"未找到基准图片: {image_path}")
            return False

        # 计算初始位置
        image_pos_x = image_location.x
        image_pos_y = image_location.y

        logger.info(f"{image_path}基准图片位置: x={image_pos_x}, y={image_pos_y}")

        # 移动鼠标到目标位置
        pyautogui.moveTo(image_pos_x, image_pos_y)
        logger.info("请在10秒内将鼠标挪到拖拽的开始位置...")
        time.sleep(10)
        
        # 记录拖拽前坐标
        start_pos = pyautogui.position()
        logger.info(f"拖拽开始，初始坐标: x={start_pos.x}, y={start_pos.y}")
        logger.info(f"请在10秒内完成拖拽...")
        time.sleep(10)  # 等待用户拖拽
        
        # 记录拖拽后坐标
        end_pos = pyautogui.position()
        logger.info(f"拖拽结束，结束坐标: x={end_pos.x}, y={end_pos.y}")
        
        # 计算拖拽距离
        dx = end_pos.x - start_pos.x
        dy = end_pos.y - start_pos.y
        logger.info(f"拖拽结束，水平距离: {dx}，垂直距离: {dy}")    
        
        logger.info(f"本次拖拽的信息: ({start_pos.x-image_pos_x}, {start_pos.y-image_pos_y}, {dx}, {dy}, 1)")
        return True

    except Exception as e:
        logger.error(f"操作异常: {str(e)}")
        return False

if __name__ == "__main__":
    # 从命令行获取图像路径和offset_name，offset_name是可选参数
    if len(sys.argv) < 2:
        print("Usage: python drag.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]

    # 调用drag_to函数
    measure_drag_distance(image_path)
