import pygame
from random import random
from math import sqrt

SCREEN_SIZE = (1280, 720)


def sub(x, y):  # СЂР°Р·РЅРѕСЃС‚СЊ РІРµРєС‚РѕСЂРѕРІ
    return x[0] - y[0], x[1] - y[1]


def add(x, y):  # СЃСѓРјРјР° РІРµРєС‚РѕСЂРѕРІ
    return x[0] + y[0], x[1] + y[1]


def length(x):  # РґР»РёРЅРЅР° РІРµРєС‚РѕСЂР°
    return sqrt(x[0] * x[0] + x[1] * x[1])


def multiply(vec, k):  # СѓРјРЅРѕР¶РµРЅРёРµ РІРµРєС‚РѕСЂР° РЅР° С‡РёСЃР»Рѕ
    return vec[0] * k, vec[1] * k


def scalar_multiply(vec, k):  # СЃРєР°Р»СЏСЂРЅРѕРµ СѓРјРЅРѕР¶РµРЅРёРµ РІРµРєС‚РѕСЂРѕРІ
    return vec[0] * k, vec[1] * k


def vector(x, y):  # СЃРѕР·РґР°РЅРёРµ РІРµРєС‚РѕСЂР° РїРѕ РЅР°С‡Р°Р»Сѓ (x) Рё РєРѕРЅС†Сѓ (y) РЅР°РїСЂР°РІР»РµРЅРЅРѕРіРѕ РѕС‚СЂРµР·РєР°
    return sub(y, x)


def draw_points(points, style="points", width=4, color=(255, 255, 255)):
    if style == "line":
        for point_number in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, (int(points[point_number][0]), int(points[point_number][1])),
                             (int(points[point_number + 1][0]), int(points[point_number + 1][1])), width)

    elif style == "points":
        for point in points:
            pygame.draw.circle(gameDisplay, color,
                               (int(point[0]), int(point[1])), width)


def get_point(points, alpha, deg=None):
    if deg is None:
        deg = len(points) - 1
    if deg == 0:
        return points[0]
    return add(multiply(points[deg], alpha), multiply(get_point(points, alpha, deg - 1), 1 - alpha))


def get_points(base_points, count):
    alpha = 1 / count
    result = []
    for i in range(count):
        result.append(get_point(base_points, i * alpha))
    return result


def get_joint(points, count):
    if len(points) < 3:
        return []
    result = []
    for i in range(-2, len(points) - 2):
        pnt = []
        pnt.append(multiply(add(points[i], points[i + 1]), 0.5))
        pnt.append(points[i + 1])
        pnt.append(multiply(add(points[i + 1], points[i + 2]), 0.5))

        result.extend(get_points(pnt, count))
    return result


def display_help():
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "РџРѕРјРѕС‰СЊ"])
    data.append(["R", "РџРµСЂРµР·Р°РїСѓСЃРє"])
    data.append(["P", "Р’РѕСЃРїСЂРѕРёР·РІРµСЃС‚Рё / РџР°СѓР·Р°"])
    data.append(["Num+", "Р”РѕР±Р°РІРёС‚СЊ С‚РѕС‡РєСѓ"])
    data.append(["Num-", "РЈРґР°Р»РёС‚СЊ С‚РѕС‡РєСѓ"])
    data.append(["", ""])
    data.append([str(steps), "С‚РµРєСѓС‰РёС… С‚РѕС‡РµРє"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


def set_points(points, speeds):
    for point in range(len(points)):
        points[point] = add(points[point], speeds[point])
        if points[point][0] > SCREEN_SIZE[0] or points[point][0] < 0:
            speeds[point] = (- speeds[point][0], speeds[point][1])
        if points[point][1] > SCREEN_SIZE[1] or points[point][1] < 0:
            speeds[point] = (speeds[point][0], -speeds[point][1])


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    points = []
    speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    points = []
                    speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(event.pos)
                speeds.append((random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        draw_points(points)
        draw_points(get_joint(points, steps), "line", 4, color)
        if not pause:
            set_points(points, speeds)
        if show_help:
            display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
