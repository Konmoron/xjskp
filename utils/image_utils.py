import pyautogui
import time
from config import CLICK_OFFSETS, GLOBAL_REGION, DRAG_CONFIGS
from .logger import get_logger

logger = get_logger()

def find(image_path, confidence=0.8, timeout=3):
    """
    寻找并点击指定图片
    :param image_path: 图片路径
    :param confidence: 匹配精度（0.0到1.0）
    :param timeout: 超时时间（秒）
    :return: 是否找到并点击成功
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=GLOBAL_REGION)
            if location:
                return True
        except pyautogui.ImageNotFoundException as e:
            break
    return False

def find_and_click(image_path, offset_name=None, before_sleep=1, after_sleep=1, timeout=1, confidence=0.8):
    """
    寻找并点击指定图片
    :param image_path: 图片路径
    :param timeout: 超时时间（秒）
    :param offset_name: 预设偏移量名称
    :param x_offset: x轴偏移量（正数向右，负数向左）
    :param y_offset: y轴偏移量（正数向下，负数向上）
    :return: 是否找到并点击成功
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            time.sleep(before_sleep)
            location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence, region=GLOBAL_REGION)
            if location:
                if offset_name and offset_name in CLICK_OFFSETS:
                    x_offset, y_offset = CLICK_OFFSETS[offset_name]
                else:
                    x_offset, y_offset = 0, 0
                
                pyautogui.click(location.x + x_offset, location.y + y_offset)
                time.sleep(after_sleep)
                return True
        except pyautogui.ImageNotFoundException as e:
            break
    return False

def drag(
    image_path: str,
    drag_config_name: str,
    confidence: float = 0.8,
    image_region: tuple = GLOBAL_REGION
):
    """
    根据图像定位执行多次拖拽操作
    :param image_path: 基准图片路径
    :param drag_config_name: 拖拽配置名称
    :param confidence: 匹配精度
    :param image_region: 图片区域
    """
    try:
        logger.info(f"🔄 初始化拖拽操作 | 配置: {drag_config_name} | 置信度: {confidence}")
        drag_cfg = DRAG_CONFIGS.get(drag_config_name)
        if not drag_cfg:
            logger.error(f"❌ 配置 '{drag_config_name}' 不存在于DRAG_CONFIGS中")
            logger.debug(f"可用配置列表: {list(DRAG_CONFIGS.keys())}")
            return False

        # 解包并记录配置参数
        x_offset, y_offset, drag_x, drag_y, duration, times = drag_cfg
        logger.info("📋 加载拖拽配置参数:")
        logger.info(f"→ 基准偏移: X={x_offset} Y={y_offset}")
        logger.info(f"→ 拖拽向量: ΔX={drag_x} ΔY={drag_y}")
        logger.info(f"→ 持续时间: {duration}s | 重复次数: {times}次")

        # 定位基准图片
        logger.debug(f"🔍 正在定位基准图片: {image_path}")
        location = pyautogui.locateCenterOnScreen(
            image_path,
            confidence=confidence,
            region=image_region
        )
        
        if not location:
            logger.error(f"❌ 基准图片定位失败: {image_path}")
            logger.warning("可能原因: 图片未显示/路径错误/分辨率不匹配")
            return False

        logger.info(f"✅ 基准图片定位成功 | 原始坐标: X={location.x} Y={location.y}")
        
        # 计算起始坐标
        start_x = location.x + x_offset
        start_y = location.y + y_offset
        logger.debug(f"📐 计算起始坐标 | X:{location.x}+{x_offset}={start_x} Y:{location.y}+{y_offset}={start_y}")

        # 执行拖拽操作
        logger.info(f"🚀 开始执行拖拽操作，共{times}次循环")
        for i in range(times):
            current = i + 1
            logger.info(f"⏳ 第{current}/{times}次拖拽 | 方向: {drag_x},{drag_y} | 持续: {duration}s")
            
            try:
                logger.debug(f"🖱️ 移动鼠标到起始坐标: ({start_x}, {start_y})")
                pyautogui.moveTo(start_x, start_y)
                
                logger.debug(f"⏲️ 开始拖拽操作...")
                pyautogui.dragRel(drag_x, drag_y, duration=duration, button='left')
                time.sleep(2)
                
                logger.info(f"✅ 第{current}次拖拽完成")
                if current < times:
                    logger.debug(f"⏳ 下一次拖拽前等待1秒...")
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"❌ 第{current}次拖拽失败: {str(e)}")
                return False

        logger.info(f"🎉 所有拖拽操作成功完成 | 总次数: {times}次")
        return True

    except pyautogui.ImageNotFoundException:
        logger.error("‼️ 基准图片查找超时，请检查图片路径和显示状态")
        return False
    except Exception as e:
        logger.error(f"‼️ 未处理的异常: {str(e)}", exc_info=True)
        return False

def drag_search(base_image_path, serach_image_path, drag_config_name, 
                max_attempts=1,
                base_image_confidence=0.8,
                search_image_confidence=0.8,
                search_before_drag=True):
    """
    拖拽搜索指定图片
    :param base_image_path: 基准图片路径
    :param serach_image_path: 搜索图片路径
    :param drag_config_name: 拖拽配置名称
    :param base_image_confidence: 基准图片匹配精度
    :param search_image_confidence: 搜索图片匹配精度
    :param max_attempts: 最大尝试次数
    :param search_before_drag: 是否在拖拽前搜索图片
    :return: 是否找到并点击成功
    """

    # 打印参数
    logger.info(f"🔍 开始拖拽搜索操作:")
    logger.info(f"→ 基准图片: {base_image_path}, 精度: {base_image_confidence}")
    logger.info(f"→ 搜索图片: {serach_image_path}, 精度: {search_image_confidence}")
    logger.info(f"→ 拖拽配置: {drag_config_name}")
    logger.info(f"→ 拖拽前搜索: {'是' if search_before_drag else '否'}")
    logger.info(f"🔄 开始执行拖拽搜索，最大尝试次数: {max_attempts}")

    logger.info(f"🔍 开始查找搜索图片: {serach_image_path}")
    if find(serach_image_path, confidence=search_image_confidence):
        logger.info(f"✅ 搜索图片找到: {serach_image_path}")
        return True

    for i in range(max_attempts):
        # 执行拖拽操作
        logger.info(f"🔄 第{i+1}/{max_attempts}次拖拽搜索")
        drag(base_image_path, drag_config_name, base_image_confidence)
        time.sleep(2)  # 等待拖拽完成

        # 查找搜索图片
        logger.info(f"🔍 开始查找搜索图片: {serach_image_path}")
        if find(serach_image_path, confidence=search_image_confidence):
            logger.info(f"✅ 搜索图片找到: {serach_image_path}")
            return True

    time.sleep(1)
    return False