import pygame
from random import random
from math import sqrt


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        return sqrt(self.x**2 + self.y**2)

    def multiply(self, k):
        v = Vector(self.x*k, self.y*k)
        return v


class Game:

    def __init__(self):

        self.steps = 20
        self.working = True
        self.points = []
        self.speeds = []
        self.show_help = False
        self.pause = False
        self.color_param = 0
        self.color = pygame.Color(0)
        self.SCREEN_SIZE = (1280, 720)

        pygame.init()
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Screen Saver")

    def sub(self, v1, v2):
        return Vector(v1.x - v2.x, v1.y - v2.y)

    def vector(self, v1, v2):
        return self.sub(v2, v1)

    def add(self, v1, v2):
        v = Vector(v1.x+v2.x, v1.y+v2.y)
        return v

    def draw_points(self, points, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(self.gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                                 (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)

        elif style == "points":
            for point in points:
                pygame.draw.circle(self.gameDisplay, color,
                                   (int(point.x), int(point.y)), width)

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append((self.add(self.points[i], self.points[i + 1])).multiply(0.5))
            pnt.append(self.points[i + 1])
            pnt.append((self.add(self.points[i + 1], self.points[i + 2])).multiply(0.5))

            result.extend(self.get_points(pnt))
        return result

    def set_points(self):
        for point in range(len(self.points)):
            self.points[point] = self.add(self.points[point], self.speeds[point])
            if self.points[point].x > self.SCREEN_SIZE[0] or self.points[point].x < 0:
                self.speeds[point] = Vector(- self.speeds[point].x, self.speeds[point].y)
            if self.points[point].y > self.SCREEN_SIZE[1] or self.points[point].y < 0:
                self.speeds[point] = Vector(self.speeds[point].x, -self.speeds[point].y)

    def get_points(self, pnt):
        alpha = 1 / self.steps
        result = []
        for i in range(self.steps):
            result.append(self.get_point(pnt, i * alpha))
        return result

    def get_point(self, pnt, alpha, deg=None):
        if deg is None:
            deg = len(pnt) - 1
        if deg == 0:
            return pnt[0]
        return self.add(pnt[deg].multiply(alpha), self.get_point(pnt, alpha, deg - 1).multiply(1 - alpha))

    def display_help(self):

        self.gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("arial", 30)
        font2 = pygame.font.SysFont("serif", 30)
        data = []
        data.append(["F1", "Помощь"])
        data.append(["R", "Перезапуск"])
        data.append(["P", "Перезапустить/пауза"])
        data.append(["Num+", "Добавить точку"])
        data.append(["Num-", "Удалить точку"])
        data.append(["", ""])
        data.append([str(self.steps), "текущих точек"])

        pygame.draw.lines(self.gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for item, text in enumerate(data):
            self.gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
            self.gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * item))

    def running(self):

        while self.working:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.working = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.working = False
                    if event.key == pygame.K_r:
                        self.points = []
                        self.speeds = []
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_KP_PLUS:
                        self.steps += 1
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        self.steps -= 1 if self.steps > 1 else 0

                if event.type == pygame.MOUSEBUTTONDOWN:
                    v = Vector(event.pos[0], event.pos[1])
                    self.points.append(v)
                    s = Vector(random()*2, random()*2)
                    self.speeds.append(s)

            self.gameDisplay.fill((0, 0, 0))
            self.color_param = (self.color_param + 1) % 360
            self.color.hsla = (self.color_param, 100, 50, 100)
            self.draw_points(self.points)
            self.draw_points(self.get_joint(), "line", 4, self.color)
            if not self.pause:
                self.set_points()
            if self.show_help:
                self.display_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


game = Game()
game.running()
