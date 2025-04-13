import time
import pyautogui
from PIL import ImageGrab, ImageDraw
import argparse
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from config import GLOBAL_REGION

def get_region():
    """获取屏幕区域坐标的辅助函数"""
    print("\n=== 屏幕区域坐标获取工具 ===")
    
    # 获取左上角坐标
    print("\n将鼠标移动到目标区域的左上角，等待5秒...")
    time.sleep(5)
    x1, y1 = pyautogui.position()
    print(f"左上角坐标: ({x1}, {y1})")
    
    # 获取右下角坐标
    print("\n将鼠标移动到目标区域的右下角，等待5秒...")
    time.sleep(5)
    x2, y2 = pyautogui.position()
    print(f"右下角坐标: ({x2}, {y2})")
    
    # 计算并打印结果
    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    
    print("\n=== 最终region参数 ===")
    print(f"({left}, {top}, {width}, {height})")
    
    return (left, top, width, height)

def show_region():
    """显示当前屏幕区域的辅助函数"""
    print("\n=== 当前屏幕区域可视化 ===")
    print(f"GLOBAL_REGION: {GLOBAL_REGION}")
    
    try:
        # 截取区域截图
        left, top, width, height = GLOBAL_REGION
        img = ImageGrab.grab(bbox=(left, top, left+width, top+height))
        
        # 绘制红色边框
        draw = ImageDraw.Draw(img)
        draw.rectangle([0, 0, width-1, height-1], outline="red", width=3)
        
        # 保存并显示
        img.save("region_visualization.png")
        img.show()
        print("已生成可视化截图: region_visualization.png")
    except Exception as e:
        print(f"区域可视化失败: {str(e)}")
        print("请检查：1.区域值是否有效 2.是否安装Pillow库(pip install pillow)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='屏幕区域工具')
    parser.add_argument('--show', action='store_true', help='显示当前GLOBAL_REGION范围')
    args = parser.parse_args()

    if args.show:
        show_region()
    else:
        get_region()