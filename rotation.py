import math

def rotate_shape(vertices, angle, cx, cy):
    """삼각형을 회전시키는 함수"""
    return [rotate_point(v[0], v[1], cx, cy, angle) for v in vertices]

def rotate_point(x, y, cx, cy, angle):
    """점 (x, y)를 중심 (cx, cy) 기준으로 angle만큼 회전"""
    radians = math.radians(angle)
    cos_a = math.cos(radians)
    sin_a = math.sin(radians)

    # 회전 변환
    nx = cos_a * (x - cx) - sin_a * (y - cy) + cx
    ny = sin_a * (x - cx) + cos_a * (y - cy) + cy
    return nx, ny