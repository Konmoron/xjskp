# 使用须知-向僵尸开炮

**如果点击不生效，请使用管理员权限运行**

**如果点击不生效，请使用管理员权限运行**

**如果点击不生效，请使用管理员权限运行**

## 安装依赖

```
pip install -r requirements.txt
```

## 运行

简单的模拟点击，时间控制

1. 需要自己截图
2. 根据自己屏幕分辨率调整`click`函数中的`x`和`y`坐标
3. 运行`python main.py`
4. 按`ctrl + c`退出

## 如何调整`click`函数中的`x`和`y`坐标

1. 先截图
2. 修改 `main.py` 里面的 `main` 方法：
```python
def main():
    # 调整`click`函数中的`x`和`y`坐标
    test_get_click_offset()
    
    # 开始
    # start()
```
3. 修改 `test_get_click_offset` 里面的图片位置
4. 运行`python main.py` 获取图片坐标
```
python .\main.py
2025-04-03 20:59:19 [409] 开始测试
2025-04-03 20:59:19 [412] 找到图片 images/huan_qiu/ji_neng_jiao_yi.png 的 location: x=2538 y=721
2025-04-03 20:59:19 [450] 找到图片images/huan_qiu/ji_neng_jiao_yi.png
```
5. 运行`python tools/get_position.py` 获取鼠标位置
```
python.exe .\tools\get_position.py
X: 2848, Y:  693
程序已终止
```
6. 计算偏移量
```
x = 2848 - 2538 = 310
y = 693 - 721 = -29
```
7. 修改 `config.py` 配置中的中的 `x` 和 `y` 坐标
8. 运行`python main.py`，验证结果
9. 修改 `main.py` 里面的 `main` 方法：
```python
def main():
    # 调整`click`函数中的`x`和`y`坐标
    # test_get_click_offset()
    
    # 开始
    start()
```
10. 运行`python main.py`

## 备注

- 本程序仅供学习和研究，不得用于非法用途
- 本程序仅供学习和研究，不得用于非法用途
- 本程序仅供学习和研究，不得用于非法用途

## 参考

- [xjskp](https://github.com/kkTea/XJSKP)
- [xjskp](https://github.com/yakehe/XJSKP)
