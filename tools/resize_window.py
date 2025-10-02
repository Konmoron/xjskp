"""
resize_window.py - 游戏窗口调整工具

本脚本用于调整"向僵尸开炮"游戏窗口的大小至预设尺寸。
通过调用 common_operations 模块中的 resize_window 函数实现窗口调整功能。

使用说明:
1. 确保游戏已启动且窗口标题为"向僵尸开炮"
2. 在项目根目录下执行: python tools/resize_window.py
3. 脚本将自动调整游戏窗口至 config.RESIZE_WINDOW_SIZE 指定的尺寸

注意:
- 仅支持Windows平台
- 需要 pygetwindow 库支持
- 游戏必须处于前台运行状态
"""

import sys
import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)
# 获取项目根目录路径（xjskp目录）
# 通过两次dirname操作：tools -> xjskp
project_root = os.path.dirname(os.path.dirname(current_file_path))

# 将项目根目录添加到Python系统路径，以便正确导入模块
if project_root not in sys.path:
    sys.path.append(project_root)
    # 调试信息（可选）: print(f"已添加项目根目录到Python路径: {project_root}")

# 从项目模块中导入游戏操作工具
# modules.operators.common_operations 包含窗口调整等游戏自动化操作
from modules.operators import common_operations

if __name__ == "__main__":
    """
    主程序入口
    当直接运行此脚本时执行以下操作:
    1. 调用 common_operations.resize_window() 函数
    2. 该函数会查找并调整"向僵尸开炮"游戏窗口大小

    使用示例:
    $ python tools/resize_window.py

    注意事项:
    - 游戏必须已经启动且窗口可见
    - 如果找不到游戏窗口，程序会报错并退出
    - 确保 config.py 中已正确配置 RESIZE_WINDOW_SIZE
    """
    # 调用窗口调整函数
    # 此函数会尝试找到标题为"向僵尸开炮"的窗口并调整其大小
    common_operations.resize_window()
