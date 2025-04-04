import pyautogui
import time

try:
    while True:
        x, y = pyautogui.position()  # 获取当前坐标
        print(f"X: {x:4}, Y: {y:4}", end="\r")  # \r 实现原地刷新
        time.sleep(0.1)  # 控制刷新频率（单位：秒）
except KeyboardInterrupt:
    print("\n程序已终止")