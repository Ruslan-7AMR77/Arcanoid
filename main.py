import os
import random

import pygame
import pygame_gui

from constants import *

pygame.init()


# загрузка изображения из файла
def load_image(name):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

# стенки игрового поля
class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2, sprite):
        super().__init__(player.all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(sprite)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(sprite)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# определение биты
class Paddle(pygame.sprite.Sprite):
    image = load_image("barrier_red.png")

    def __init__(self):
        super().__init__(player.all_sprites)
        self.add(player.paddle)
        self.image = pygame.transform.scale(Paddle.image, (PADDLE_WIDTH, PADDLE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = PADDLE_X
        self.rect.y = PADDLE_Y

    def update(self):
        if player.key != None:
            # если была нажата клавиша Влево и не сталкиваемся с левой стенкой
            if player.key == 'left' and not pygame.sprite.spritecollideany(self, player.left_borders):
                self.rect.left -= PADDLE_SPEED
                # если была нажата клавиша Вправо и не сталкиваемся с правой стенкой
            elif player.key == 'right' and not pygame.sprite.spritecollideany(self, player.right_borders):
                self.rect.left += PADDLE_SPEED


# определение мяча
class Ball(pygame.sprite.Sprite):
    image = load_image("ball_red_small.png")

    def __init__(self, radius):
        super().__init__(player.all_sprites)
        self.add(player.ball)
        self.radius = radius
        self.image = pygame.transform.scale(Ball.image, (2 * radius, 2 * radius))
        self.rect = pygame.Rect(BALL_X, BALL_Y, 2 * radius, 2 * radius)
        # направление мяча при движении
        self.vx = random.choice((-BALL_SPEED, BALL_SPEED))
        self.vy = -BALL_SPEED

    # движение с проверкой столкновение шара со стенками
    def update(self):
        if player.game_action:
            self.rect = self.rect.move(self.vx, self.vy)
            if pygame.sprite.spritecollideany(self, player.blocks):
                # коснулись кирпича. Меняем направление
                self.vy = -self.vy
            elif pygame.sprite.spritecollideany(self, player.paddle):
                # коснулись биты. Меняем направление
                self.vy = -self.vy
            elif pygame.sprite.spritecollideany(self, player.bottom_borders):
                # мяч коснулся нижней границы. уничтожаем мяч
                self.kill()
            elif pygame.sprite.spritecollideany(self, player.top_borders):
                # мяч коснулся верхней границы. Меняем направление
                self.vy = -self.vy
            elif pygame.sprite.spritecollideany(self, player.left_borders):
                # мяч коснулся левой границы. Меняем направление
                self.vx = -self.vx
            elif pygame.sprite.spritecollideany(self, player.right_borders):
                # мяч коснулся правой границы. Меняем направление
                self.vx = -self.vx
        elif player.key != None:
            # если мяч пока в начальном положении (на бите), то двигаем мяч вместе с битой при нажатии вправо/влево
            if player.key == 'left' and (self.rect.centerx - PADDLE_WIDTH // 2) > 0:
                self.rect.left -= PADDLE_SPEED
            elif player.key == 'right' and (self.rect.centerx + PADDLE_WIDTH // 2) < SCREEN_WIDTH:
                self.rect.left += PADDLE_SPEED


# определение кирпича
class Block(pygame.sprite.Sprite):

    def __init__(self, x, y, image_name):
        super().__init__(player.blocks)
        image = load_image(image_name)
        self.image = pygame.transform.scale(image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if pygame.sprite.spritecollideany(self, player.ball):
            # если мяч столкнулся с кирпичом, то уничтожаем кирпич
            self.kill()


# определение игрока
class Player():

    def __init__(self):
        self.player_name = ''
        self.score = 0
        self.background = None
        self.caption = ''
        self.all_sprites = pygame.sprite.Group()
        self.top_borders = pygame.sprite.Group()
        self.left_borders = pygame.sprite.Group()
        self.right_borders = pygame.sprite.Group()
        self.bottom_borders = pygame.sprite.Group()
        self.paddle = pygame.sprite.Group()
        self.ball = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        # количество кирпичей в ряду
        self.kol_blocks_in_row = SCREEN_WIDTH // BLOCK_WIDTH
        # всего кирпичей
        self.kol_blocks = self.kol_blocks_in_row * BLOCK_ROW
        # количество мячей
        self.kol_ball = 1
        # флаг, что мяч в движении (не на бите)
        self.game_action = False
        # переменная для хранения нажатой кнопки
        self.key = None
        # флаг, что игра начата
        self.start_game = False
        # флаг, что игра проиграна
        self.lose = False
        # флаг, что игра выиграна
        self.win = False
        # флаг, что необходимо проводить подсчеты
        self.need_calc = False

    # запуск игры
    def run_game(self):
        self.start_game = True
        self.need_calc = True
        Border(0, 0, SCREEN_WIDTH, 0, self.top_borders)
        Border(0, SCREEN_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, self.bottom_borders)
        Border(0, 0, 0, SCREEN_HEIGHT, self.left_borders)
        Border(SCREEN_WIDTH, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.right_borders)
        Paddle()
        Ball(BALL_RADIUS)
        for x in range(self.kol_blocks_in_row):
            for y in range(BLOCK_ROW):
                Block(x * BLOCK_WIDTH, y * BLOCK_HEIGHT, random.choice(BLOCK_LIST))
        self.key = None

    #подсчет
    def calc(self):
        if self.need_calc:
            self.kol_ball = len(player.ball.sprites())
            self.score += (self.kol_blocks - len(player.blocks.sprites()))
            self.kol_blocks = len(player.blocks.sprites())

            if player.kol_ball == 0:
                self.lose = True
            elif player.kol_blocks == 0:
                self.win = True

    def set_caption(self):
        self.caption = SCREEN_TITLE + '     Player: ' + self.player_name + '     Score: ' + str(self.score)


if __name__ == '__main__':
    size = width, height = SCREEN_WIDTH, SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(SCREEN_TITLE)
    background_image = load_image(SCREE_IMAGE)
    fps = FPS
    player_name = 'Anonymus'
    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    player = Player()
    player.player_name = player_name

    textbox = pygame_gui.elements.UITextBox(
        html_text="Enter you name:",
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 135), (200, 40)),
        manager=manager
    )

    entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 2 - 135), (200, 40)),
        manager=manager,
    )

    but_newgame = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 35), (100, 50)),
        text='New Game',
        manager=manager,
    )

    but_quitgame = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 35), (100, 50)),
        text='Exit',
        manager=manager
    )
    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                confirmation_dialog = pygame_gui.windows.UIConfirmationDialog(
                    rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100), (300, 200)),
                    manager=manager,
                    window_title='Подтверждение',
                    action_long_desc='Вы уверены, что хотите выйти?',
                    action_short_name='OK',
                    blocking=True
                )
                confirmation_event = 'quit'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.key = 'left'
                elif event.key == pygame.K_RIGHT:
                    player.key = 'right'
                elif event.key == pygame.K_SPACE:
                    # подтвердили начальный запуск мяча
                    player.game_action = True
            elif event.type == pygame.KEYUP:
                player.key = None

            # обработаем пользовательские события
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                    # была нажато подтверждение выхода. Выходим из основного цикла
                    running = False
                if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    # в окне ввода имени игрока нажали Enter.
                    # присваиваем имя игрока
                    player_name = event.text
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == but_newgame:
                        # была нажата кнопка "Новая игра". Запускаем новую игру
                        player = Player()
                        player.player_name = player_name
                        player.run_game()
                    if event.ui_element == but_quitgame:
                        # была нажата кнопка "Выйти". Выходим из основного цикла
                        running = False

                    textbox.kill()
                    if entry != None:
                        entry.kill()
                    but_newgame.kill()
                    but_quitgame.kill()

            manager.process_events(event)
        manager.update(time_delta)

        screen.blit(background_image, (0, 0))
        manager.draw_ui(screen)

        # если игра начата
        if player.start_game:
            player.all_sprites.update()
            player.blocks.update()
            player.all_sprites.draw(screen)
            player.blocks.draw(screen)

            player.calc()
            player.set_caption()
            pygame.display.set_caption(player.caption)

            # в случае проигрыша выводим сообщение и кнопки с предложением начать новую игру или выйти
            if player.lose:
                player.need_calc = False
                player.lose = False
                entry = None

                textbox = pygame_gui.elements.UITextBox(
                    html_text="             YOU LOSE",
                    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150), (300, 100)),
                    manager=manager
                )

                but_newgame = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 35), (100, 50)),
                    text='New Game',
                    manager=manager
                )

                but_quitgame = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 35), (100, 50)),
                    text='Exit',
                    manager=manager
                )
            # в случае выигрыша выводим сообщение и кнопки с предложением начать новую игру или выйти
            elif player.win:
                player.need_calc = False
                player.win = False
                entry = None

                textbox = pygame_gui.elements.UITextBox(
                    html_text="             YOU WIN",
                    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 100), (300, 200)),
                    manager=manager
                )

                but_newgame = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 35), (100, 50)),
                    text='New Game',
                    manager=manager,
                )

                but_quitgame = pygame_gui.elements.UIButton(
                    relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 35), (100, 50)),
                    text='Exit',
                    manager=manager
                )

        pygame.display.flip()
    pygame.quit()