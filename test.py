import pygame
import numpy
import math

def value(koefs, size, sim1, sim2):

    ret1 = koefs[0] * ((sim1.x - sim2.x) ** 2 + (sim1.y - sim2.y) ** 2) ** 0.5 / size
    ret2 = koefs[1] * (abs((sim1.move_vector_x - sim2.move_vector_x) / 2) + abs((sim1.move_vector_y - sim2.move_vector_y) / 2)) / (2 * size)
    ret3 = koefs[2] * (abs((sim1.attack_vector_x - sim2.attack_vector_x) / 2) + abs((sim1.attack_vector_y - sim2.attack_vector_y) / 2)) / (2 * size)

    #print(ret1, ret2, ret3)

    return ret1 + ret2 + ret3

class Sim:

    def __init__(self, x, y, move_vector_x, move_vector_y, attack_vector_x, attack_vector_y, force_attack, max_force_attack):

        self.x, self.y = x, y
        self.move_vector_x, self.move_vector_y = move_vector_x, move_vector_y
        self.attack_vector_x, self.attack_vector_y = attack_vector_x, attack_vector_y
        self.force_attack = force_attack
        self.max_force_attack = max_force_attack

W, H = 600, 600

screen = pygame.display.set_mode((W, H))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen.fill(WHITE)

count = 10
sims = []
for i in range(count):
    max_force_ = numpy.random.normal(50, 5)
    sims.append(Sim(numpy.random.randint(10, W - 10),
                    numpy.random.randint(10, H - 10),
                    numpy.random.normal(0, 10),
                    numpy.random.normal(0, 10),
                    numpy.random.normal(0, 50),
                    numpy.random.normal(0, 50),
                    numpy.random.randint(0, 100) / 100 * max_force_,
                    max_force_))

size = 20

limits_x = [-1, 0] # мин, макс
limits_y = [-1, 0] # мин, макс

avg_force_attack = 0
avg_max_force_attack = 0

for sim in sims:
    if limits_x[0] == -1 or limits_x[0] > sim.x:
        limits_x[0] = sim.x
    if limits_x[1] < sim.x:
        limits_x[1] = sim.x
    if limits_y[0] == -1 or limits_y[0] > sim.y:
        limits_y[0] = sim.y
    if limits_y[1] < sim.y:
        limits_y[1] = sim.y

    avg_force_attack += sim.force_attack
    avg_max_force_attack += sim.max_force_attack

avg_force_attack /= len(sims)
avg_max_force_attack /= len(sims)

limit_min_x = limits_x[0] // size * size
limit_max_x = (limits_x[1] // size + 1) * size
limit_min_y = limits_y[0] // size * size
limit_max_y = (limits_y[1] // size + 1) * size

shape_x, shape_y = (limit_max_x - limit_min_x) // size, (limit_max_y - limit_min_y) // size

situation = numpy.zeros((4, shape_x, shape_y))
# позиции противника
# изменение позиций противника
# позиция выдения огня (откуда) 
# атакуемые позиции (куда)

for sim in sims:
    x, y = (sim.x - limit_min_x) // size, (sim.y - limit_min_y) // size
    situation[0][x][y] += sim.max_force_attack / avg_max_force_attack

    situation[1][x][y] -= sim.max_force_attack / avg_max_force_attack
    x_moving, y_moving = int((sim.x + sim.move_vector_x - limit_min_x) // size), int((sim.y + sim.move_vector_y - limit_min_y) // size)
    if 0 <= x_moving < shape_x and 0 <= y_moving < shape_y:
        situation[1][x_moving][y_moving] += sim.max_force_attack / avg_max_force_attack
    
    situation[2][x][y] += sim.force_attack / avg_force_attack

    x_attacking, y_attacking = int((sim.x + sim.attack_vector_x - limit_min_x) // size), int((sim.y + sim.attack_vector_y - limit_min_y) // size)
    if 0 <= x_attacking < shape_x and 0 <= y_attacking < shape_y:
        situation[3][x_attacking][y_attacking] += sim.force_attack / avg_force_attack

for i in range(shape_x):
    for j in range(shape_y):
        situation[0] /= abs(situation[0].max())
        rect = pygame.Surface([size, size], pygame.SRCALPHA, 32).convert_alpha()
        rect.fill((0, 0, 0, 125 * situation[0][i][j]))
        screen.blit(rect, (limit_min_x + i * size, limit_min_y + j * size))

        situation[1] /= abs(situation[1].max())
        rect = pygame.Surface([size, size], pygame.SRCALPHA, 32).convert_alpha()
        if situation[1][i][j] > 0:
            rect.fill((0, 0, 255, 125 * situation[1][i][j]))
        else:
            rect.fill((255, 0, 0, 0 - 125 * situation[1][i][j]))
        #screen.blit(rect, (limit_min_x + i * size, limit_min_y + j * size))

        situation[2] /= abs(situation[2].max())
        rect = pygame.Surface([size, size], pygame.SRCALPHA, 32).convert_alpha()
        rect.fill((255, 255, 0, 125 * situation[2][i][j]))
        screen.blit(rect, (limit_min_x + i * size, limit_min_y + j * size))

        situation[3] /= abs(situation[3].max())
        rect = pygame.Surface([size, size], pygame.SRCALPHA, 32).convert_alpha()
        rect.fill((255, 0, 0, 125 * situation[3][i][j]))
        screen.blit(rect, (limit_min_x + i * size, limit_min_y + j * size))
    


pygame.display.update()
