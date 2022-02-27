SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Арканоид'
SCREE_IMAGE = 'fon_grey.jpg'

FPS = 60

# размер биты
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 28
PADDLE_SPEED = 15
# начальное положение биты
PADDLE_X = SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2
PADDLE_Y = SCREEN_HEIGHT - 50

# параметры мяча
BALL_RADIUS = 20
BALL_SPEED = 5
# начальное положение мяча
BALL_X = SCREEN_WIDTH // 2 - BALL_RADIUS
BALL_Y = PADDLE_Y - 2 * BALL_RADIUS

# размер кирпича
BLOCK_WIDTH = 60
BLOCK_HEIGHT = 30
# количество рядов кирпичей
BLOCK_ROW = 4
# имена файлов кирпичей
BLOCK_LIST = ["block_brown.png", "block_blue.png", "block_green.png", "block_red.png"]