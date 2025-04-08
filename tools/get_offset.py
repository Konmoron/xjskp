import pyautogui
import time
import logging

def get_offset(image_path):
    """
    获取图片位置并计算偏移量
    :param image_path: 图片路径
    :return: 偏移量元组 (x_offset, y_offset) 或 None
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(lineno)d] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 获取图片位置
    location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
    if not location:
        logging.info(f"未找到图片 {image_path}")
        return None
        
    logging.info(f"找到图片 {image_path} 的 location: x={location.x} y={location.y}")
    x0, y0 = location.x, location.y

    # 获取目标点击位置
    logging.info("将鼠标移动到要点击的位置，等待10秒...")
    time.sleep(10)
    x1, y1 = pyautogui.position()
    logging.info(f"移动后的位置: x={x1} y={y1}")

    # 计算偏移量
    offset = (x1 - x0, y1 - y0)
    print(f"偏移量: x={offset[0]}, y={offset[1]}")
    
    return offset

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("使用方法: python tools/get_offset.py 图片路径")
        sys.exit(1)
        
    result = get_offset(sys.argv[1])
    if result:
        logging.info(f"偏移量: ({result[0]}, {result[1]})")
        # print(f"最终偏移量: x={result[0]}, y={result[1]}")