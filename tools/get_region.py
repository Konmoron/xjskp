import time
import pyautogui

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

if __name__ == "__main__":
    get_region()