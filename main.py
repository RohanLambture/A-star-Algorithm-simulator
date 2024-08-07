
import pygame
from queue import PriorityQueue

WIDTH = 1000
HEIGHT = 800
OPTIONS_WIDTH = 200
GRID_SIZE = 600
PADDING = 20

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = OPTIONS_WIDTH + PADDING + (col * width)
        self.y = PADDING + (row * width)
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (OPTIONS_WIDTH + PADDING, PADDING + i * gap), (OPTIONS_WIDTH + PADDING + width, PADDING + i * gap))
        pygame.draw.line(win, GREY, (OPTIONS_WIDTH + PADDING + i * gap, PADDING), (OPTIONS_WIDTH + PADDING + i * gap, PADDING + width))

def draw_options_panel(win, selected_tool):
    try:
        font = pygame.font.SysFont('comicsans', 30)
    except pygame.error:
        font = pygame.font.Font(None, 30)  
        
    text = font.render('Options', 1, WHITE)
    win.blit(text, (10, 10))

    button_width = 160
    button_height = 40
    button_margin = 10
    button_color = (100, 100, 100)
    button_hover_color = (150, 150, 150)
    text_color = BLACK

    buttons = [
        {"rect": pygame.Rect(10, 60, button_width, button_height), "color": GREEN, "hover_color": (0, 255, 0), "text": "Start"},
        {"rect": pygame.Rect(10, 110, button_width, button_height), "color": RED, "hover_color": (255, 0, 0), "text": "End"},
        {"rect": pygame.Rect(10, 160, button_width, button_height), "color": BLUE, "hover_color": (0, 0, 255), "text": "Wall"},
        {"rect": pygame.Rect(10, 210, button_width, button_height), "color": WHITE, "hover_color": (200, 200, 200), "text": "Ground"}
    ]

    for button in buttons:
        color = button["hover_color"] if button["text"].lower() == selected_tool else button["color"]
        pygame.draw.rect(win, color, button["rect"])
        if button["rect"].collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(win, button["hover_color"], button["rect"])
        try:
            button_font = pygame.font.SysFont('comicsans', 20)
        except pygame.error:
            button_font = pygame.font.Font(None, 20)  
        button_text = button_font.render(button["text"], 1, text_color)
        win.blit(button_text, (button["rect"].x + button_width // 2 - button_text.get_width() // 2,
                               button["rect"].y + button_height // 2 - button_text.get_height() // 2))

    start_button_rect = pygame.Rect(10, HEIGHT - 100, button_width, button_height)
    reset_button_rect = pygame.Rect(10, HEIGHT - 50, button_width, button_height)
    pygame.draw.rect(win, GREEN, start_button_rect)
    pygame.draw.rect(win, RED, reset_button_rect)
    if start_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(win, (0, 255, 0), start_button_rect)
    if reset_button_rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(win, (255, 0, 0), reset_button_rect)
    start_text = font.render('Start', 1, text_color)
    reset_text = font.render('Reset', 1, text_color)
    win.blit(start_text, (start_button_rect.x + button_width // 2 - start_text.get_width() // 2,
                          start_button_rect.y + button_height // 2 - start_text.get_height() // 2))
    win.blit(reset_text, (reset_button_rect.x + button_width // 2 - reset_text.get_width() // 2,
                          reset_button_rect.y + button_height // 2 - reset_text.get_height() // 2))

def draw(win, grid, rows, width):
    win.fill(BLACK)
    draw_options_panel(win, selected_tool)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x, y = pos

    row = (y - PADDING) // gap
    col = (x - OPTIONS_WIDTH - PADDING) // gap

    return row, col

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def main(win, width, height):
    ROWS = 30
    grid = make_grid(ROWS, GRID_SIZE)

    start = None
    end = None
    run = True
    started = False

    global selected_tool
    selected_tool = None

    while run:
        draw(win, grid, ROWS, GRID_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:  
                pos = pygame.mouse.get_pos()
                if pos[0] < OPTIONS_WIDTH:
                    if 60 <= pos[1] < 100:
                        selected_tool = "start"
                    elif 110 <= pos[1] < 150:
                        selected_tool = "end"
                    elif 160 <= pos[1] < 200:
                        selected_tool = "wall"
                    elif 210 <= pos[1] < 250:
                        selected_tool = "ground"
                    elif HEIGHT - 100 <= pos[1] < HEIGHT - 60:  
                        if start and end:
                            for row in grid:
                                for spot in row:
                                    spot.update_neighbors(grid)
                            started = True
                            algorithm(lambda: draw(win, grid, ROWS, GRID_SIZE), grid, start, end)
                            started = False
                    elif HEIGHT - 50 <= pos[1] < HEIGHT - 10:  
                        start = None
                        end = None
                        grid = make_grid(ROWS, GRID_SIZE)
                        selected_tool = None
                        started = False
                else:
                    row, col = get_clicked_pos(pos, ROWS, GRID_SIZE)
                    if 0 <= row < ROWS and 0 <= col < ROWS:
                        spot = grid[row][col]
                        if selected_tool == "start":
                            if start:
                                start.reset()
                            start = spot
                            start.make_start()
                        elif selected_tool == "end":
                            if end:
                                end.reset()
                            end = spot
                            end.make_end()
                        elif selected_tool == "wall":
                            spot.make_barrier()
                        elif selected_tool == "ground":
                            spot.reset()
                            if spot == start:
                                start = None
                            elif spot == end:
                                end = None

            elif pygame.mouse.get_pressed()[2]:  
                pos = pygame.mouse.get_pos()
                if pos[0] > OPTIONS_WIDTH:
                    row, col = get_clicked_pos(pos, ROWS, GRID_SIZE)
                    if 0 <= row < ROWS and 0 <= col < ROWS:
                        spot = grid[row][col]
                        spot.reset()
                        if spot == start:
                            start = None
                        elif spot == end:
                            end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    started = True
                    algorithm(lambda: draw(win, grid, ROWS, GRID_SIZE), grid, start, end)
                    started = False

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, GRID_SIZE)
                    selected_tool = None

    pygame.quit()

pygame.font.init()
main(WIN, WIDTH, HEIGHT)
