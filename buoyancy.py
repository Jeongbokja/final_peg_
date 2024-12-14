def apply_buoyancy(obj, water_level, buoyancy_force, dt):
    """부력 적용"""
    if 'radius' in obj:  # 원일 경우
        if obj['y'] + obj['radius'] > water_level:  # 물에 닿은 경우
            obj['vy'] += buoyancy_force * dt
    elif 'height' in obj:  # 사각형일 경우
        if obj['y'] + obj['height'] / 2 > water_level:  # 물에 닿은 경우
            obj['vy'] += buoyancy_force * dt
