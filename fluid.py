def is_in_water(obj, water_level):
    """객체가 물 속에 있는지 확인"""
    if 'radius' in obj:  # 원일 경우
        return obj['y'] + obj['radius'] > water_level
    elif 'height' in obj:  # 사각형일 경우
        return obj['y'] + obj['height'] / 2 > water_level
    return False
