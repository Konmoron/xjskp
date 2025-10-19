def format_duration(seconds: float) -> str:
    """将秒数格式化为可读时间字符串（自动处理进位并优化显示）"""
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    seconds = round(remaining_seconds % 60)

    # 处理进位
    if seconds >= 60:
        seconds -= 60
        minutes += 1
    if minutes >= 60:
        minutes -= 60
        hours += 1

    # 精确转换为整数
    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)

    # 根据时间单位存在情况动态构建字符串
    parts = []
    if hours > 0:
        parts.append(f"{hours}小时")
    if minutes > 0:
        parts.append(f"{minutes}分")
    # 仅当小时和分钟都为0时显示秒数（包括0秒情况）
    if hours == 0 and minutes == 0:
        parts.append(f"{seconds}秒")
    elif seconds > 0:  # 有分钟/小时时，仅当秒>0才显示
        parts.append(f"{seconds}秒")

    # 处理全0情况（0秒）
    return "".join(parts) if parts else "0秒"
