import pygame
import os
import random

# num - число, которое нужно отгадать
num = []
while len(set(num)) != 4:
    num.append(str(random.randrange(10)))
num = "".join(set(num))

pygame.init()
size = width, height = 910, 680
screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())
clock = pygame.time.Clock()


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[" "] * width for _ in range(height)]
        self.left = 20
        self.top = 85
        self.cell_size = 80

    def render(self):
        color = pygame.Color("#FF7F24")
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen, color, (
                    x * self.cell_size + self.left, y * self.cell_size + self.top, self.cell_size, self.cell_size), 1)

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Attempts(Board):
    def __init__(self, width, height):
        super().__init__(width, height)
        # вначале все клетки закрыты
        self.board = [[" "] * width for _ in range(height)]
        self._x = 0
        self._y = 0

    def open_cell(self, cell):
        self._x, self._y = cell

    def update_cell(self, number, count):
        if count < 4:
            if self.board[self._y][self._x] == " ":
                self.board[self._y][self._x] = number

    def on_click(self, cell):
        self.open_cell(cell)

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != " ":
                    color = pygame.Color("#FFD700")
                    font = pygame.font.Font(None, self.cell_size + 25)
                    text = font.render(str(self.board[y][x]), 1, color)
                    screen.blit(text, (x * self.cell_size + self.left + 22, y * self.cell_size + self.top + 10))


def load_image(name):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        image = pygame.transform.scale(image, (75, 75))
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


class Bulls(pygame.sprite.Sprite):
    image_bull = load_image("Bull.png")

    def __init__(self, group, number, n_str):
        #
        super().__init__(group)
        self.image = Bulls.image_bull
        self.rect = self.image.get_rect()
        self.x = 350 + 3 * 80 + (number - 1) * 80
        self.rect.y = 85 + (n_str - 1) * 80
        self.rect.x = width

    def update(self):
        if self.rect.x > self.x:
            self.rect.x -= 1


class Cows(pygame.sprite.Sprite):
    image_cow = load_image("Cow.png")

    def __init__(self, group, number, n_str):
        #
        super().__init__(group)
        self.image = Cows.image_cow
        self.rect = self.image.get_rect()
        self.x = 350 + (number - 1) * 80
        self.rect.y = 85 + (n_str - 1) * 80
        self.rect.x = width

    def update(self):
        if self.rect.x > self.x:
            self.rect.x -= 1


def check(num, num_att):
    ans_cows = 0
    ans_bulls = 0
    for i, n in enumerate(num):
        if n in num_att:
            if num[i] == num_att[i]:
                ans_bulls += 1
            else:
                ans_cows += 1
    return ans_cows, ans_bulls


def draw_Title():
    screen.fill((0, 0, 0))
    color = pygame.Color("#8A3324")
    font = pygame.font.Font(None, 55)
    text = font.render("Bulls and Cows", 1, color)
    text_x = width // 2 - text.get_width() // 2
    text_y = 15
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, color,
                     (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)
    font = pygame.font.Font(None, 20)
    text = font.render("You have seven attempts to guess a four-digit number, consisting of different numbers.", 1,
                       color)
    text_x = width // 2 - text.get_width() // 2
    text_y = 65
    screen.blit(text, (text_x, text_y))

    font = pygame.font.Font(None, 25)
    text = font.render("Click on the cell and enter the number.", 1, color)
    text_x = 25
    text_y = height - 30
    screen.blit(text, (text_x, text_y))


def draw_result(n_str, num_bulls):
    color = pygame.Color("#FF0000")
    font = pygame.font.Font(None, 25)
    if num_bulls == 4:
        text = font.render("You are well done", 1, color)
    else:
        text = font.render("That was the number " + num, 1, color)
    text_x = 370
    text_y = height - 30
    screen.blit(text, (text_x, text_y))


count = 0
n_str = 0
num_attempts = []
rez = False
all_sprites = pygame.sprite.Group()
draw_Title()
board = Board(4, 7)
board.render()
attempts = Attempts(4, 7)
ticks = 0
num_cows, num_bulls = 0, 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            attempts.get_click(event.pos)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                number = "0"
            if event.key == pygame.K_1:
                number = "1"
            if event.key == pygame.K_2:
                number = "2"
            if event.key == pygame.K_3:
                number = "3"
            if event.key == pygame.K_4:
                number = "4"
            if event.key == pygame.K_5:
                number = "5"
            if event.key == pygame.K_6:
                number = "6"
            if event.key == pygame.K_7:
                number = "7"
            if event.key == pygame.K_8:
                number = "8"
            if event.key == pygame.K_9:
                number = "9"
            num_attempts.append(number)
            attempts.update_cell(number, count)
            count += 1
            if count == 4:
                num_att = "".join(num_attempts)
                num_attempts = []
                (num_cows, num_bulls) = check(num, num_att)
                rez = True
                count = 0
                n_str += 1
                if n_str == 7 or num_bulls == 4:
                    draw_result(n_str, num_bulls)

    attempts.render()
    for i in range(1, num_cows + 1):
        Cows(all_sprites, i, n_str)
    for i in range(1, num_bulls + 1):
        Bulls(all_sprites, i, n_str)
    num_cows, num_bulls = 0, 0
    if rez:
        all_sprites.draw(screen)
        all_sprites.update()
    pygame.display.flip()
    clock.tick(1500)
pygame.quit()
