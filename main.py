import pygame
from random import random
from math import sqrt


SCREEN_SIZE = (1280, 720)


class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def add(self, other):
        result = self.x + other.x, self.y + other.y
        return Vector(result)

    def sub(self, other):
        result = self.x - other.x, self.y - other.y
        return Vector(result)

    def mul(self, other):
        if isinstance(other, Vector):
            result = self.x * other, self.y * other
            return Vector(result)

    def scalar_mul(self, other):
        result = self.x * other.x + self.y * other.y
        return result

    def __len__(self):
        result = sqrt(self.x **2+ self.y **2)
        return Vector(result)


class Line:

    def __init__(self):
        self.points = []
        self.speeds = []

    def add_point(self, position, speed):
        self.points.append(position)
        self.speeds.append(speed)

    def change_speed(self, new_speed):
        for speed_number in range(len(self.speeds)):
            self.speeds[speed_number] = Vector.mul(self.speeds[speed_number], new_speed)

    def delete_point(self):
        self.points = self.points[:-1]
        self.speeds = self.speeds[:-1]

    def set_points(self, points, speeds):
        for point in range(len(points)):
            points[point] = points[point].add(speeds[point])
            if points[point].x > SCREEN_SIZE[0] or points[point].x < 0:
                speeds[point] = (- speeds[point].x, speeds[point].y)
            if points[point].y > SCREEN_SIZE[1] or points[point].y < 0:
                speeds[point] = (speeds[point].x, -speeds[point].y)


class Joint(Line):

    def __init__(self):
        super().__init__()

    def draw_points(self, color):
        """Drawing of lines"""
        super().draw_points(style='line', color=color)

    def get_joint(self, points, count):
        if len(points) < 3:
            return []
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append(Vector.mul(Vector.add(self.points[i], self.points[i + 1]), 0.5))
            pnt.append(self.points[i + 1])
            pnt.append(Vector.mul(Vector.add(self.points[i + 1], self.points[i + 2]), 0.5))

            result.extend(self.get_points(pnt))

        return result

    def get_points(self, base_points):
        alpha = 1 / self.steps
        result = []
        for i in range(self.steps):
            result.append(self.get_point(base_points, i * alpha))
        return result

    def get_point(self, base_points, alpha, deg=None):
        if deg is None:
            deg = len(base_points) - 1

        if deg == 0:
            return base_points[0]

        return Vector.add(Vector.mul(base_points[deg], alpha),
                          Vector.mul(self.get_point(base_points, alpha, deg - 1), 1 - alpha))


def display_help(joint):
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("arial", 30)
    font2 = pygame.font.SysFont("serif", 30)
    data = []
    data.append(["F1", "Помощь"])
    data.append(["R", "Перезапуск"])
    data.append(["P", "Воспроизвести / Пауза"])
    data.append(["Num+", "Добавить точку"])
    data.append(["Num-", "Удалить точку"])
    data.append(["H", "Увеличить скорость"])
    data.append(["L", "Уменьшить скорость"])
    data.append(["DELETE", "Удалить точку из кривой"])
    data.append(["", ""])
    data.append([str(joint.steps), "текущих точек"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
                      (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for item, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * item))

def draw_points(points, style="points", width=4, color=(255, 255, 255)):
    if style == "line":
        for point_number in range(-1, len(points) - 1):
            pygame.draw.line(gameDisplay, color, (int(points[point_number].x), int(points[point_number].y)),
                                 (int(points[point_number + 1].x), int(points[point_number + 1].y)), width)

    elif style == "points":
        for point in points:
            pygame.draw.circle(gameDisplay, color,
                                (int(point.x), int(point.y)), width)


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    points = []
    speeds = []
    steps = 20
    working = True
    show_help = False
    pause = False
    line = Line()
    joint = Joint()
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
                    line.points = []
                    line.speeds = []
                    joint.points = []
                    joint.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    joint.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    joint.steps -= 1 if joint.steps > 1 else 0
                if event.key == pygame.K_h:
                    line.change_speed(2)
                    joint.change_speed(2)
                if event.key == pygame.K_l:
                    line.change_speed(0.5)
                    joint.change_speed(0.5)
                if event.key == pygame.K_DELETE:
                    line.delete_point()
                    joint.delete_point()

            if event.type == pygame.MOUSEBUTTONDOWN:
                points.append(Vector(event.pos[0], event.pos[1]))
                speeds.append(Vector(random() * 2, random() * 2))

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        line.draw_points()
        joint.draw_points(color=color)

        if not pause:
            line.set_points()
            joint.set_points()
        if show_help:
            display_help(joint)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
