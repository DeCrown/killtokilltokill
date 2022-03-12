import pygame
import numpy
import math

def value(koefs, size, sim1, sim2):

    ret1 = koefs[0] * ((sim1.x - sim2.x) ** 2 + (sim1.y - sim2.y) ** 2) ** 0.5 / size
    ret2 = koefs[1] * (abs((sim1.move_vector_x - sim2.move_vector_x) / 2) + abs((sim1.move_vector_y - sim2.move_vector_y) / 2)) / (2 * size)
    ret3 = koefs[2] * (abs((sim1.attack_vector_x - sim2.attack_vector_x) / 2) + abs((sim1.attack_vector_y - sim2.attack_vector_y) / 2)) / (2 * size)

    print(ret1, ret2, ret3)

    return ret1 + ret2 + ret3



W, H = 100, 100

screen = pygame.display.set_mode((W, H))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen.fill(WHITE)

count = 10
sims = []
for i in range(count):
    sims.append(Sim(numpy.random.randint(10, W - 10),
                    numpy.random.randint(10, H - 10),
                    numpy.random.normal(0, 10),
                    numpy.random.normal(0, 10),
                    numpy.random.normal(0, 50),
                    numpy.random.normal(0, 50)))

groups = []
used = []
koefs = (10, 60, 7)
size = (800 ** 2 + 800 ** 2) ** 0.5
limit = 0.8

for i in range(count):
    group = []
    if not sims[i] in used:
        for j in range(count):
            if not i == j:
                val = value(koefs, size, sims[i], sims[j])
                if val <= limit:
                    if not sims[j] in used:
                        group.append(sims[j])
                        used.append(sims[j])
    if not len(group) == 0:
        group.append(sims[i])
        used.append(sims[i])
        groups.append(group)

for i in range(count):
    if not sims[i] in used:
        group = [sims[i]]
        groups.append(group)

for group in groups:
    points = []
    
    for sim in group:
        pygame.draw.circle(screen, BLACK, (sim.x, sim.y), 4)
        pygame.draw.aaline(screen, BLACK, (sim.x, sim.y), (sim.x + sim.move_vector_x, sim.y + sim.move_vector_y))
        pygame.draw.aaline(screen, RED, (sim.x, sim.y), (sim.x + sim.attack_vector_x, sim.y + sim.attack_vector_y))
        points.append((sim.x, sim.y))

    if len(group) > 2:
        pygame.draw.aalines(screen, GREEN, False, points) # numpy.random.randint(0, 255, 3)

pygame.display.update()
