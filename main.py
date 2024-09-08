import sys, random
import pygame

from pygame.locals import *

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

FPS = 30
fpsClock = pygame.time.Clock()

MINES = 10 # 爆弾の数
TILE_SIZE  = 64 # タイルの一辺の長さ
START_TILE_WIDTH = (SCREEN_WIDTH - (TILE_SIZE * MINES)) / 2
START_TILE_HEIGHT = (SCREEN_HEIGHT - (TILE_SIZE * MINES)) / 2

# フォント設定
font = None

# 爆弾がある場所は "-1" とする
# 設定するステージ
backStages = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

# ユーザーから見えるステージ
# 0: 触っていない
# 1: オープン済み
# 2: オープン済み(数字)
# 3: フラグ
userStages = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

colors = {
    "white" : (255, 255, 255),
    "black" : (0, 0, 0),
    "red"   : (255, 0, 0),
    "green" : (0, 255, 0),
    "blue"  : (0, 0, 255),
}

# チャタリング回避用
oldMouseL, oldMouseM, oldMouseR = False, False, False

game_over = False
win = False

# *******************************************************************
# 爆弾を設置する    
# *******************************************************************
def place_mines():
    mine_coords = set()
    # 爆弾の数になるまでセットする
    while len(mine_coords) < MINES:
        row = random.randint(0, len(backStages[0]) - 1)
        col = random.randint(0, len(backStages) - 1)
        mine_coords.add((row, col))
    for mine in mine_coords:
        backStages[mine[0]][mine[1]] = -1


# *******************************************************************
# 爆弾を数え、ステージに記録する    
# *******************************************************************
def count_mines():
    cnt = 0
    for col_i in range(len(backStages)):
        for row_i in range(len(backStages[0])):
            # 爆弾の場合スキップ
            if backStages[col_i][row_i] == -1 :
                continue
            for y in range(-1, 2) :
                for x in range(-1, 2) :
                    # 自分自身の時
                    if y == 0 and x == 0:
                        continue
                    # 枠より小さい時
                    if col_i + y < 0 or row_i + x < 0:
                        continue
                    # 枠より大きい時
                    if col_i + y >= len(backStages) or row_i + x >= len(backStages[0]):
                        continue
                    # 爆弾の時、カウントを増やす
                    if backStages[col_i+y][row_i+x] == -1:
                        cnt += 1
            backStages[col_i][row_i] = cnt
            cnt = 0

# *******************************************************************
# 現在マウスのあるタイルの場所を返します。
# *******************************************************************
def get_tile_pos():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    x =  (mouse_x - START_TILE_WIDTH) / TILE_SIZE
    y = (mouse_y - START_TILE_HEIGHT) / TILE_SIZE
    return (int(x), int(y))

# *******************************************************************
# ステージをコンソールに表示します。
# デバッグ時に活用してください。
# *******************************************************************
def stage_preview():
    print("stage***************")
    for stage in backStages:
        print(stage)
    print("********************")

# *******************************************************************
# タイルをオープンする
# *******************************************************************
def open_tile(x, y):
    global game_over, win
    if x < 0 or x >= len(backStages[0]) or y < 0 or y >= len(backStages):
        return
    if userStages[y][x] != 0:
        return
    if backStages[y][x] == -1:
        game_over = True
        return
    userStages[y][x] = 1
    if backStages[y][x] == 0:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx != 0 or dy != 0:
                    open_tile(x + dx, y + dy)
    check_win()

# *******************************************************************
# 勝利条件をチェックする
# *******************************************************************
def check_win():
    global win
    for y in range(len(backStages)):
        for x in range(len(backStages[0])):
            if backStages[y][x] != -1 and userStages[y][x] == 0:
                return
    win = True

def setup():
    global font
    pygame.init()
    pygame.display.set_caption("Pygame Minesweeper")
    place_mines()
    count_mines()
    font = pygame.font.Font(None, 50)
    stage_preview()

def update():
    global font, oldMouseL, oldMouseM, oldMouseR, game_over, win
    while True:
        # *******************************************************************
        # 処理
        # *******************************************************************
        isMouseL, isMouseM, isMouseR = pygame.mouse.get_pressed()
        # 左クリックしたとき
        if isMouseL and not oldMouseL:
            mouseX, mouseY = get_tile_pos()
            if not game_over and not win:
                open_tile(mouseX, mouseY)

        # 右クリックしたとき
        elif isMouseR and not oldMouseR:
            mouseX, mouseY = get_tile_pos()
            if not game_over and not win:
                if userStages[mouseY][mouseX] == 3:
                    userStages[mouseY][mouseX] = 0
                elif userStages[mouseY][mouseX] == 0:
                    userStages[mouseY][mouseX] = 3

                # 前回のキーを記録しておく
        oldMouseL, oldMouseM, oldMouseR = isMouseL, isMouseM, isMouseR
        # *******************************************************************
        # 描画
        # *******************************************************************
        screen.fill(colors["black"])

        # 縁枠
        pygame.draw.rect(screen, colors["white"], (START_TILE_WIDTH, START_TILE_HEIGHT, 640, 640), 5)

        # タイルを表示する
        tileWidth = START_TILE_WIDTH
        tileHeight = START_TILE_HEIGHT
        for tileY in range(10):
            for tileX in range(10):
                # 開いてないとき
                if userStages[tileY][tileX] == 0:
                    pygame.draw.rect(screen, colors["white"], (tileWidth, tileHeight, TILE_SIZE, TILE_SIZE))
                # フラグを立てている時
                elif userStages[tileY][tileX] == 3:
                    pygame.draw.rect(screen, colors["red"], (tileWidth, tileHeight, TILE_SIZE, TILE_SIZE))
                # 開いているとき
                elif userStages[tileY][tileX] == 1:
                    if backStages[tileY][tileX] == 0:
                        pygame.draw.rect(screen, colors["green"], (tileWidth, tileHeight, TILE_SIZE, TILE_SIZE))
                    else:
                        pygame.draw.rect(screen, colors["blue"], (tileWidth, tileHeight, TILE_SIZE, TILE_SIZE))
                        text = font.render(str(backStages[tileY][tileX]), True, colors["white"])
                        screen.blit(text, (tileWidth + 20, tileHeight + 10))
                pygame.draw.rect(screen, colors["black"], (tileWidth, tileHeight, TILE_SIZE, TILE_SIZE), 2)
                tileWidth += TILE_SIZE
            tileWidth = START_TILE_WIDTH
            tileHeight += TILE_SIZE

        if game_over:
            text = font.render("Game Over", True, colors["red"])
            screen.blit(text, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50])
        elif win:
            text = font.render("You Win!", True, colors["green"])
            screen.blit(text, [SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50])

        pygame.display.update()
        fpsClock.tick(FPS)

        # *******************************************************************
        # 終了時
        # *******************************************************************
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

def main():
    setup()
    update()

if __name__ == "__main__":
    main()