import pygame
from random import random, randint
from math import sqrt


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, another_vector):
        new_vector = Vector(self.x + another_vector.x, self.y + another_vector.y)
        return new_vector

    def __sub__(self, another_vector):
        new_vector = Vector(self.x - another_vector.x, self.y - another_vector.y)
        return new_vector

    def len(self):
        return sqrt(self.x**2 + self.y**2)

    def __mul__(self, k):
        v = Vector(self.x*k, self.y*k)
        return v

    def int_pair(self):
        tpl = (int(self.x), int(self.y))
        return tpl


class Line:

    def __init__(self, screen_size, game_display):
        self.steps = 0
        self.points = []
        self.speeds = []
        self.color_param = 0
        self.color = pygame.Color(0)
        self.SCREEN_SIZE = screen_size
        self.gameDisplay = game_display

    def add_point(self):
        x = randint(0, self.SCREEN_SIZE[0])
        y = randint(0, self.SCREEN_SIZE[1])
        self.points.append(Vector(x, y))
        self.speeds.append(Vector(random()*2, random()*2))
        self.steps += 1

    def remove_point(self):
        self.points = self.points[:-1]
        self.speeds = self.speeds[:-1]
        self.steps -= 1

    def set_points(self):
        for point in range(len(self.points)):
            self.points[point] = self.points[point].__add__(self.speeds[point])
            if self.points[point].x > self.SCREEN_SIZE[0] or self.points[point].x < 0:
                self.speeds[point] = Vector(- self.speeds[point].x, self.speeds[point].y)
            if self.points[point].y > self.SCREEN_SIZE[1] or self.points[point].y < 0:
                self.speeds[point] = Vector(self.speeds[point].x, -self.speeds[point].y)

    def draw_points(self, points, style="points", width=4, color=(255, 255, 255)):
        if style == "line":
            for point_number in range(-1, len(points) - 1):
                pygame.draw.line(self.gameDisplay, color, points[point_number].int_pair(),
                                 points[point_number + 1].int_pair(), width)

        elif style == "points":
            for point in points:
                pygame.draw.circle(self.gameDisplay, self.color,
                                   point.int_pair(), width)

    def raise_speed(self):
        new_speeds = []
        for i in range(len(self.speeds)):
            vx, vy = self.speeds[i].x, self.speeds[i].y
            new_speeds.append(Vector(vx*2, vy*2))
        self.speeds = new_speeds

    def refuse_speed(self):
        new_speeds = []
        for i in range(len(self.speeds)):
            vx, vy = self.speeds[i].x, self.speeds[i].y
            new_speeds.append(Vector(vx/2, vy/2))
        self.speeds = new_speeds

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
        return (self.get_point(pnt, alpha, deg - 1).__mul__(1 - alpha)).__add__(pnt[deg].__mul__(alpha))

    def get_joint(self):
        if len(self.points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append((self.points[i].__add__(self.points[i + 1])).__mul__(0.5))
            pnt.append(self.points[i + 1])
            pnt.append((self.points[i + 1].__add__(self.points[i + 2])).__mul__(0.5))
            result.extend(self.get_points(pnt))
        return result


class Joint(Line):

    def add_point(self):
        x = randint(0, self.SCREEN_SIZE[0])
        y = randint(0, self.SCREEN_SIZE[1])
        self.points.append(Vector(x, y))
        self.speeds.append(Vector(random() * 2, random() * 2))
        self.steps += 1
        self.draw_points(self.get_joint(), "line", 4, self.color)

    def set_points(self):
        for point in range(len(self.points)):
            self.points[point] = self.points[point].__add__(self.speeds[point])
            if self.points[point].x > self.SCREEN_SIZE[0] or self.points[point].x < 0:
                self.speeds[point] = Vector(- self.speeds[point].x, self.speeds[point].y)
            if self.points[point].y > self.SCREEN_SIZE[1] or self.points[point].y < 0:
                self.speeds[point] = Vector(self.speeds[point].x, -self.speeds[point].y)
        self.draw_points(self.get_joint(), "line", 4, self.color)


class Game:

    def __init__(self):

        self.SCREEN_SIZE = (1280, 720)
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_SIZE)
        self.joint = Joint(self.SCREEN_SIZE, self.gameDisplay)
        self.working = True
        self.show_help = False
        self.pause = False

        pygame.init()
        self.gameDisplay = pygame.display.set_mode(self.SCREEN_SIZE)
        pygame.display.set_caption("Screen Saver")

    def len(self, vector):
        return sqrt(vector.x ** 2 + vector.y ** 2)

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
        data.append([str(self.joint.steps), "текущих точек"])

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
                        self.joint.points = []
                        self.joint.speeds = []
                        self.joint.steps = 0
                    if event.key == pygame.K_p:
                        self.pause = not self.pause
                    if event.key == pygame.K_h:
                        self.joint.raise_speed()
                    if event.key == pygame.K_l:
                        self.joint.refuse_speed()
                    if event.key == pygame.K_KP_PLUS:
                        self.joint.add_point()
                    if event.key == pygame.K_F1:
                        self.show_help = not self.show_help
                    if event.key == pygame.K_KP_MINUS:
                        if self.joint.steps > 1:
                            self.joint.remove_point()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    v = Vector(event.pos[0], event.pos[1])
                    self.joint.points.append(v)
                    s = Vector(random()*2, random()*2)
                    self.joint.speeds.append(s)
                    self.joint.steps += 1

            self.gameDisplay.fill((0, 0, 0))
            self.joint.color_param = (self.joint.color_param + 1) % 360
            self.joint.color.hsla = (self.joint.color_param, 100, 50, 100)
            self.joint.draw_points(self.joint.points)
            self.joint.draw_points(self.joint.get_joint(), "line", 4, self.joint.color)
            if not self.pause:
                self.joint.set_points()
            if self.show_help:
                self.display_help()

            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        exit(0)


game = Game()
game.running()
