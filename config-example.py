# 游戏所在区域
GLOBAL_REGION = (2100, 100, 890, 1700)

REGIONS = {
    "default": (2100, 100, 890, 1700),
    "game_start": (744, 84, 437, 826),
}

RESIZE_WINDOW_SIZE = (420, 770)

# 偏移量配置
CLICK_OFFSETS = {
    "open_chat": (349, 725),  # 打开聊天
    "close_first_charge": (146, -227),  # 首充关闭
    "close_chat": (311, 86),  # 关闭聊天
    "open_zhao_mu": (0, -57),  # 招募按钮
    "close_guan_qia_select": (-231, 0),  # 关卡返回
    "close_offline_offline": (126, 156),  # 离线
    "close_offline_offline_end": (0, 79),  # 离线结束
    "close_ji_neng_jiao_yi": (310, -28),  # 关闭技能交易
    "close_yuan_zheng_fang_an": (297, -77),  # 关闭御主界面
    "close_yuan_zheng": (-327, 126),  # 退出远征
    "close_yuan_zheng_que_ren": (133, 159),
    "close_guang_gao_1": (332, 111),  # 关闭普通广告
    "close_chou_jiang_1": (213, 94),
    "open_ti_li": (95, 113),  # 打开体力
    "jun_tuan_task_100_zuan_shi": (283, 91),  # 任务-100钻石
    "jun_tuan_task_2_bao_xiang": (218, 92),  # 任务-2宝箱
    "header_tou_xiang": (-325, 142),
}

DRAG_CONFIGS = {
    # offset_x, offset_y, 拖拽x距离, 拖拽y距离, 拖拽时间, 拖拽次数
    "shop": (0, 1176, 0, -831, 1.5, 4),
    "zhan_dou_left_down": (-346, 760, 0, -300, 2, 1),
    "zhan_dou_left_up": (-346, 434, 0, 300, 2, 1),
    "zuo_zhan_ji_hua_down": (0, -164, 0, -683, 2, 1),
    "jun_tuan_task_left_down": (0, 1048, 0, -400, 2, 1),
    "jun_tuan_task_left_up": (0, 570, 0, 400, 2, 1),
    "jun_tuan_task_up_bu_chang": (-8, 820, 1, -141, 1, 1),
    "jun_tuan_task_down_bu_chang": (-8, 820, 1, 141, 1, 1),
    "xuan_fu_down": (-6, 1026, 4, -235, 1.5, 1),
    "xuan_fu_up": (5, 644, -4, 202, 1.5, 1),
    "move_game_to_default_region": (-3, 2, 755, -52, 3, 1),
}

FU_CONFIGS = [
    {
        "name": "xxx服",
        "image_path": "images/fu/xxx_fu.png",
        "confidence": 0.95,
    },
    {
        "name": "xxxx服",
        "image_path": "images/fu/xxxx_fu.png",
        "confidence": 0.95,
    },
]
