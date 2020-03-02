import pygame
import pygame.display
import pygame.draw
import pymunk
import pymunk.pygame_util

from constants import DEFAULT_POS, BOARD_WIDTH, BORDER_WIDTH, GOAL_POS
from utils.engine import to_pygame

FPS = 120


class Sim:
    lines = []

    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_WIDTH, BOARD_WIDTH))
        pygame.display.set_caption("Move a body in square")
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()
        self.space.gravity = (0, 0)

        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self._create_goal()
        self._create_body()
        self._create_room()

    def _create_room(self):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = (0, 0)
        width = BOARD_WIDTH - BORDER_WIDTH
        l1 = pymunk.Segment(body, (BORDER_WIDTH, BORDER_WIDTH), (width, BORDER_WIDTH), 1)
        l2 = pymunk.Segment(body, (BORDER_WIDTH, width), (width, width), 1)
        l3 = pymunk.Segment(body, (BORDER_WIDTH, BORDER_WIDTH), (BORDER_WIDTH, width), 1)
        l4 = pymunk.Segment(body, (width, BORDER_WIDTH), (width, width), 1)
        self.lines.append(l1)
        self.lines.append(l2)
        self.lines.append(l3)
        self.lines.append(l4)
        self.space.add(l1)
        self.space.add(l2)
        self.space.add(l3)
        self.space.add(l4)
        self._draw_lines(
            [
                l1,
                l2,
                l3,
                l4,
            ]
        )

    def _draw_lines(self, lines):
        for line in lines:
            body = line.body
            pv1 = body.position + line.a.rotated(body.angle)
            pv2 = body.position + line.b.rotated(body.angle)
            p1 = to_pygame(pv1)
            p2 = to_pygame(pv2)
            pygame.draw.lines(self.screen, 1, False, [p1, p2])

    def _create_goal(self):
        mass = 1
        radius = 3
        moment = pymunk.moment_for_circle(mass, 1, radius)
        self.body_goal = pymunk.Body(mass, moment)
        self.body_goal.position = GOAL_POS
        self.shape_goal = pymunk.Circle(self.body_goal, radius)
        self.space.add(self.body_goal, self.shape_goal)

    def _create_body(self):
        mass = 1
        radius = 10
        moment = pymunk.moment_for_circle(mass, 1, radius)
        self.body_character = pymunk.Body(mass, moment)
        self.body_character.position = DEFAULT_POS
        self.shape_character = pymunk.Circle(self.body_character, radius)
        self.space.add(self.body_character, self.shape_character)

    def move(self, x, y, do=True):
        if do:
            self.body_character.position = (self.body_character.position.x + x, self.body_character.position.x + y)
            return True

    def render(self):
        self.space.step(1 / 50.0)
        self.screen.fill((255, 255, 255))
        self.space.debug_draw(self.draw_options)
        pygame.display.flip()
        self.clock.tick(FPS)


sim = Sim()
