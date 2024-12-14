from fluid import is_in_water
from buoyancy import apply_buoyancy
from gravity import apply_gravity
from collision import handle_wall_collision, resolve_convex_collision
from rotation import rotate_point, rotate_shape
import pygame

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Engine")
clock = pygame.time.Clock()

# 화면 상태
MODE_COLLISION = 0
MODE_BUOYANCY = 1
MODE_ROTATION = 2
current_mode = MODE_COLLISION

triangle = {
    'x': WIDTH // 2,
    'y': HEIGHT // 2,
    'vertices': [(0, -50), (43, 25), (-43, 25)],  # 초기 좌표
    'vx': 150,
    'vy': 100,
    'angle': 0,
    'angular_velocity': 90  # 90도/초
}

# 중력 및 부력
GRAVITY = 9.8
BUOYANCY_FORCE = -15
WATER_LEVEL = HEIGHT // 2

# 충돌 화면 객체
circle_yellow = {'x': 300, 'y': 100, 'radius': 30, 'vx': 150, 'vy': 100}
circle_red = {'x': 500, 'y': 100, 'radius': 30, 'vx': -150, 'vy': 100}

# 부력 화면 객체
rect = {'x': WIDTH // 2, 'y': 100, 'width': 60, 'height': 60, 'vx': 0, 'vy': 0}

# 메인 루프
running = True
while running:
    dt = clock.tick(60) / 1000
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                current_mode = (current_mode + 1) % 3

    if current_mode == MODE_COLLISION:
        # 충돌 화면
        for circle in [circle_yellow, circle_red]:
            circle['x'] += circle['vx'] * dt
            circle['y'] += circle['vy'] * dt
            apply_gravity(circle, GRAVITY, dt)
            handle_wall_collision(circle, WIDTH, HEIGHT)
        resolve_convex_collision(circle_yellow, circle_red)
        pygame.draw.circle(screen, (255, 255, 0), (int(circle_yellow['x']), int(circle_yellow['y'])), circle_yellow['radius'])
        pygame.draw.circle(screen, (255, 0, 0), (int(circle_red['x']), int(circle_red['y'])), circle_red['radius'])

    elif current_mode == MODE_BUOYANCY:
        # 부력 화면
        rect['y'] += rect['vy'] * dt
        apply_gravity(rect, GRAVITY, dt)
        if is_in_water(rect, WATER_LEVEL):
            apply_buoyancy(rect, WATER_LEVEL, BUOYANCY_FORCE, dt)

        # 물과 사각형 그리기
        pygame.draw.rect(screen, (0, 0, 255), (0, WATER_LEVEL, WIDTH, HEIGHT - WATER_LEVEL))
        pygame.draw.rect(screen, (255, 255, 0), (
        int(rect['x'] - rect['width'] // 2), int(rect['y'] - rect['height'] // 2), rect['width'], rect['height']))



    elif current_mode == MODE_ROTATION:

        # 삼각형 회전 및 이동
        triangle['x'] += triangle['vx'] * dt
        triangle['y'] += triangle['vy'] * dt
        triangle['angle'] += triangle['angular_velocity'] * dt
        # 회전 변환
        rotated_vertices = rotate_shape(
            [(triangle['x'] + v[0], triangle['y'] + v[1]) for v in triangle['vertices']],
            triangle['angle'], triangle['x'], triangle['y']
        )
        # 벽 충돌 처리
        # 삼각형 그리기
        pygame.draw.polygon(screen, (0, 255, 0), rotated_vertices)

    pygame.display.flip()

pygame.quit()
