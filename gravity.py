def apply_gravity(obj, gravity, dt):
    """중력 적용"""
    obj['vy'] += gravity * dt
