import math
import buoyancy
import fluid
import gravity

#처음의 원의 경우 convex hull로 다각형화근사화 여기서는 8각형으로 구현하였음
def get_circle_vertices(circle, num_vertices=8):
    vertices = []
    for i in range(num_vertices):
        angle = 2 * math.pi * i / num_vertices
        x = circle['x'] + circle['radius'] * math.cos(angle)
        y = circle['y'] + circle['radius'] * math.sin(angle)
        vertices.append((x, y))
    return vertices

def project_polygon(vertices, axis): #다각형 투영
    min_proj = float('inf')
    max_proj = float('-inf')
    for vertex in vertices:
        projection = vertex[0] * axis[0] + vertex[1] * axis[1]
        min_proj = min(min_proj, projection)
        max_proj = max(max_proj, projection)
    return min_proj, max_proj

def separating_axis_test(vertices1, vertices2): #sat충돌감지
    edges = []
    for i in range(len(vertices1)):
        x1, y1 = vertices1[i]
        x2, y2 = vertices1[(i + 1) % len(vertices1)]
        edges.append((-(y2 - y1), x2 - x1))

    for i in range(len(vertices2)):
        x1, y1 = vertices2[i]
        x2, y2 = vertices2[(i + 1) % len(vertices2)]
        edges.append((-(y2 - y1), x2 - x1))

    for edge in edges:
        axis = normalize(edge)
        min1, max1 = project_polygon(vertices1, axis)
        min2, max2 = project_polygon(vertices2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

def normalize(vector):
    """벡터 정규화"""
    length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    return vector[0] / length, vector[1] / length

def resolve_convex_collision(obj1, obj2):
    """충돌 처리"""
    vertices1 = get_circle_vertices(obj1)
    vertices2 = get_circle_vertices(obj2)
    if separating_axis_test(vertices1, vertices2):
        obj1['vx'], obj2['vx'] = -obj1['vx'], -obj2['vx']
        obj1['vy'], obj2['vy'] = -obj1['vy'], -obj2['vy']

def handle_wall_collision(obj, screen_width, screen_height):
    """벽 충돌 처리"""
    if 'radius' in obj:  # 원일 경우
        if obj['x'] - obj['radius'] < 0 or obj['x'] + obj['radius'] > screen_width:
            obj['vx'] = -obj['vx']
            obj['x'] = max(obj['radius'], min(obj['x'], screen_width - obj['radius']))
        if obj['y'] - obj['radius'] < 0 or obj['y'] + obj['radius'] > screen_height:
            obj['vy'] = -obj['vy']
            obj['y'] = max(obj['radius'], min(obj['y'], screen_height - obj['radius']))
    elif 'width' in obj and 'height' in obj:  # 사각형일 경우
        half_width, half_height = obj['width'] / 2, obj['height'] / 2
        if obj['x'] - half_width < 0 or obj['x'] + half_width > screen_width:
            obj['vx'] = -obj['vx']
            obj['x'] = max(half_width, min(obj['x'], screen_width - half_width))
        if obj['y'] - half_height < 0 or obj['y'] + half_height > screen_height:
            obj['vy'] = -obj['vy']
            obj['y'] = max(half_height, min(obj['y'], screen_height - half_height))



