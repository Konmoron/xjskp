# 使用须知-向僵尸开炮

**如果点击不生效，请使用管理员权限运行**

**如果点击不生效，请使用管理员权限运行**

**如果点击不生效，请使用管理员权限运行**

## 生成依赖

```
# 方法一：使用pipreqs（推荐，仅生成项目实际用到的依赖）
pip install pipreqs
pipreqs . --force --encoding=utf-8
```

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

以 关闭技能交易 为示例。

1. 先截图，图片保存到 `images/huan_qiu/ji_neng_jiao_yi.png`
2. 在命令行运行 `python tools/get_offset.py` 获取偏移量

```
python tools/get_offset.py images/huan_qiu/ji_neng_jiao_yi.png
```

之后鼠标移动到【关闭技能交易的位置】，不用点击
等待程序结束，并给出 offset 的坐标，之后粘贴到`config.py`中即可

3. 测试 offset 是否正确

执行 `python click_with_offset.py 图片路径 [偏移量名称]`，如果点击生效，说明 offset 正确

## 备注

- 本程序仅供学习和研究，不得用于非法用途
- 本程序仅供学习和研究，不得用于非法用途
- 本程序仅供学习和研究，不得用于非法用途

## 参考

- [xjskp](https://github.com/kkTea/XJSKP)
- [xjskp](https://github.com/yakehe/XJSKP)
