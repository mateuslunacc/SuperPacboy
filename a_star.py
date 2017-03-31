#essa classe da suporte a coisas como custo, passo-a-passo da construcao, etc
#mas para conseguir apenas o caminho otimizado usa-se
# como usar:

#graph = SimpleGraph()
#graph.edges = criaListaDeArestas(mapa_a_ser_usado)

#came_from, cost_so_far = a_star_search(graph, "inicio_x,inicio_y" , "fim_x,fim_y")

#print ou variavel = reconstruct_path(came_from, "inicio_x,inicio_y", "fim_x,fim_y" )

class SimpleGraph:
    def __init__(self):
        self.edges = {}

    def neighbors(self, id):
        return self.edges[id]

import collections

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self):
        return len(self.elements) == 0

    def put(self, x):
        self.elements.append(x)

    def get(self):
        return self.elements.popleft()


def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = "\u2192"
        if x2 == x1 - 1: r = "\u2190"
        if y2 == y1 + 1: r = "\u2193"
        if y2 == y1 - 1: r = "\u2191"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#" * width
    return r


import heapq

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)  # optional
    path.reverse()  # optional
    return path

#mudar euristica se possivel
def heuristic(a, b, tie_breaker):
    a = a.split(",")
    b = b.split(",")

    a = (int(a[0]), int(a[-1]))
    b = (int(b[0]), int(b[-1]))

    (x1, y1) = a
    (x2, y2) = b
    if (tie_breaker):
        return (abs(x1 - x2) + abs(y1 - y2)) * (1.0 + 1/1000)
    else:
        print abs(x1 - x2) + abs(y1 - y2)
        return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal, tie_breaker):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0
    lista = []

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current]
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                lista.append(current)
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next, tie_breaker)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, lista

