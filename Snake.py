import pygame
import random
import pygame_menu
from pygame import mixer

lvl = 'первый'
frame_count = 0
zvuk_vk = 1
difficult = 1
name = "Гость"
pygame.mixer.pre_init(15000, -16, 1, 512)
mixer.init()
audio_game = mixer.Sound('Thunder.mp3')
audio_menu = mixer.Sound('Happy.mp3')
udar_ob_stenu = mixer.Sound('удар_об_стену.mp3')
udar_ob_sebya = mixer.Sound('удар_об_себя.mp3')
audio_apple = mixer.Sound('яблоко.mp3')
eda_zamedleniye = mixer.Sound('яблоко.mp3')
eda_uskoreniye = mixer.Sound('яблоко.mp3')
pygame.init()
bg_image = pygame.image.load('cosmos.png')
bg_image_por = pygame.image.load('cosmos_por.png')
bg_image_pob = pygame.image.load('cosmos_pob.png')
SIZE_BLOCK = 20
FRAME_COLOR = (0, 255, 100)
WHITE = (72, 209, 204)
BLUE = (64, 224, 208)
RED = (255, 0, 0)
HEADER_COLOR = (0, 205, 155)
SNAKE_COLOR = (0, 0, 250)
COUNT_BLOCKS = 20
HEADER_MARGIN = 70
MARGIN = 1
size = [SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS,
        SIZE_BLOCK * COUNT_BLOCKS + 2 * SIZE_BLOCK + MARGIN * COUNT_BLOCKS + HEADER_MARGIN]

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('Arial', 25)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < COUNT_BLOCKS and 0 <= self.y < COUNT_BLOCKS

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + column * SIZE_BLOCK + MARGIN + (column + 1),
                                     HEADER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN + (row + 1),
                                     SIZE_BLOCK, SIZE_BLOCK])


def get_random_empty_block1():
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    empty_block = SnakeBlock(x, y)
    while empty_block in snake_blocks:
        empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
        empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
    return empty_block


def busters1():
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    busters_block = SnakeBlock(x, y)
    while busters_block in snake_blocks:
        busters_block.x = random.randint(0, COUNT_BLOCKS - 1)
        busters_block.y = random.randint(0, COUNT_BLOCKS - 1)
    return busters_block


def medlenno1():
    x = random.randint(0, COUNT_BLOCKS - 1)
    y = random.randint(0, COUNT_BLOCKS - 1)
    ch_blo = SnakeBlock(x, y)
    while ch_blo in snake_blocks:
        ch_blo.x = random.randint(0, COUNT_BLOCKS - 1)
        ch_blo.y = random.randint(0, COUNT_BLOCKS - 1)
    return ch_blo


snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
d_row = buf_row = 0
d_col = buf_col = 1
apple = get_random_empty_block1()
total = 0
speed = 0
buster = busters1()
ch = medlenno1()


def start_the_game():
    if zvuk_vk:
        audio_menu.stop()
        audio_game.play(-1)

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    def busters():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        busters_block = SnakeBlock(x, y)
        while busters_block in snake_blocks:
            busters_block.x = random.randint(0, COUNT_BLOCKS - 1)
            busters_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return busters_block

    def medlenno():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        ch_blo = SnakeBlock(x, y)
        while ch_blo in snake_blocks:
            ch_blo.x = random.randint(0, COUNT_BLOCKS - 1)
            ch_blo.y = random.randint(0, COUNT_BLOCKS - 1)
        return ch_blo

    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global difficult
    global frame_count
    difficult = 4

    running = True
    while running:
        total_seconds = int(frame_count // (speed + 3)) + speed
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
        text = courier.render(output_string, True, pygame.Color('black'))
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                elif event.key == pygame.K_SPACE:
                    p_pause()
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Score:{total}', True, pygame.Color('black'))
        text_speed = courier.render(f'Speed:{speed}', True, pygame.Color('black'))
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 350, SIZE_BLOCK))
        screen.blit(text, [175, 20])

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            with open('record', 'r') as fin:
                lines = fin.readlines()
                sp = lines
                sp = sp[:15]
                lu4 = [99999]
                for i in range(len(sp)):
                    lu4.append(int(sp[i].split(", ")[0][1:]))
            if total > min(lu4) or len(lu4) < 16:
                lu4.append(total)
                lu4.sort(reverse=True)
                lu4 = lu4[:16]
                rec = total, speed, output_string, name
                sp.append(str(rec) + "\n")
                with open('record', 'w') as f:
                    for i in range(1, len(lu4)):
                        for j in range(len(sp)):
                            if int(sp[j].split(", ")[0][1:]) == lu4[i]:
                                f.write(sp[j])
                                break
            if zvuk_vk:
                audio_game.stop()
                udar_ob_stenu.play()
                audio_menu.play(loops=-1, fade_ms=0)
            porajenie_menu()
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if total % 5 == 0 and total > 0 and speed > 1:
            draw_block(pygame.Color('black'), ch.x, ch.y)

        if total % 3 == 0 and total > 0:
            draw_block(pygame.Color('purple'), buster.x, buster.y)

        if apple == head:
            if zvuk_vk:
                audio_apple.play()
            total += 1
            speed += 1
            if total % 5 == 0 and total > 0:
                speed += 0
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        if buster == head:
            if zvuk_vk:
                eda_uskoreniye.play()
            speed += 1
            total -= 1
            buster = busters()

        if ch == head:
            if zvuk_vk:
                eda_zamedleniye.play()
            speed -= 1
            total += 1
            ch = medlenno()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            with open('record', 'r') as fin:
                lines = fin.readlines()
                sp = lines
                lu4 = [99999]
                for i in range(len(sp)):
                    lu4.append(int(sp[i].split(", ")[0][1:]))
            if total > min(lu4) or len(lu4) < 11:
                lu4.append(total)
                lu4.sort(reverse=True)
                rec = total, speed, output_string, name
                sp.append(str(rec) + "\n")
                with open('record', 'w') as f:
                    for i in range(1, len(lu4)):
                        for j in range(len(sp)):
                            if int(sp[j].split(", ")[0][1:]) == lu4[i]:
                                f.write(sp[j])
                                break
            if zvuk_vk:
                audio_game.stop()
                udar_ob_sebya.play()
                audio_menu.play(loops=0, fade_ms=0)
            porajenie_menu()
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


def p_pause():
    menu1 = pygame_menu.Menu('Snake', 330, 272,
                             theme=pygame_menu.themes.THEME_DARK)

    menu1.add.button('Главное меню:', glavnoe_menu)
    menu1.add.button('Продолжить:', start_nuzniy_game)
    menu1.add.selector('Звук:', [('Выкл', 0), ('Вкл', 1)], default=zvuk_vk, onchange=set_difficulty1)
    menu1.add.button('Выйти:', pygame_menu.events.EXIT)
    audio_game.stop()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu1.is_enabled():
            menu1.update(events)
            menu1.draw(screen)

        pygame.display.update()


def level_one():
    if zvuk_vk:
        audio_menu.stop()
        audio_game.play(-1)

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    def busters():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        busters_block = SnakeBlock(x, y)
        while busters_block in snake_blocks:
            busters_block.x = random.randint(0, COUNT_BLOCKS - 1)
            busters_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return busters_block

    def medlenno():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        ch_blo = SnakeBlock(x, y)
        while ch_blo in snake_blocks:
            ch_blo.x = random.randint(0, COUNT_BLOCKS - 1)
            ch_blo.y = random.randint(0, COUNT_BLOCKS - 1)
        return ch_blo

    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global difficult
    global frame_count
    difficult = 1

    frame_count = -11

    running = True
    while running:
        total_seconds = int(frame_count // (speed + 3)) + speed * 5
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
        text = courier.render(output_string, True, pygame.Color('black'))
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                elif event.key == pygame.K_SPACE:
                    p_pause()
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Score:{total}', True, pygame.Color('black'))
        text_speed = courier.render(f'Speed:{speed}', True, pygame.Color('black'))
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 350, SIZE_BLOCK))
        screen.blit(text, [175, 20])

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                udar_ob_stenu.play()
                audio_menu.play(loops=-1, fade_ms=0)
            porajenie_menu()
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if total % 5 == 0 and total > 0 and speed > 1:
            draw_block(pygame.Color('black'), ch.x, ch.y)

        if total % 3 == 0 and total > 0:
            draw_block(pygame.Color('purple'), buster.x, buster.y)

        if apple == head:
            if zvuk_vk:
                audio_apple.play()
            total += 1
            if total % 5 == 0 and total > 0:
                speed += 0
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        if buster == head:
            if zvuk_vk:
                eda_uskoreniye.play()
            speed += 1
            total -= 1
            buster = busters()

        if ch == head:
            if zvuk_vk:
                eda_zamedleniye.play()
            speed -= 1
            total += 1
            ch = medlenno()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                udar_ob_sebya.play()
                audio_menu.play(loops=0, fade_ms=0)
            porajenie_menu()
            break
        if total > 9:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name, "победа"
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                audio_menu.play(loops=0, fade_ms=0)
            pobeda_menu()
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


def level_two():
    if zvuk_vk:
        audio_menu.stop()
        audio_game.play(-1)

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    def busters():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        busters_block = SnakeBlock(x, y)
        while busters_block in snake_blocks:
            busters_block.x = random.randint(0, COUNT_BLOCKS - 1)
            busters_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return busters_block

    def medlenno():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        ch_blo = SnakeBlock(x, y)
        while ch_blo in snake_blocks:
            ch_blo.x = random.randint(0, COUNT_BLOCKS - 1)
            ch_blo.y = random.randint(0, COUNT_BLOCKS - 1)
        return ch_blo

    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global difficult
    global frame_count
    difficult = 2
    frame_count = -11

    running = True
    while running:
        total_seconds = int(frame_count // (speed + 3)) + speed * 5
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
        text = courier.render(output_string, True, pygame.Color('black'))
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                elif event.key == pygame.K_SPACE:
                    p_pause()
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Score:{total}', True, pygame.Color('black'))
        text_speed = courier.render(f'Speed:{speed}', True, pygame.Color('black'))
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 350, SIZE_BLOCK))
        screen.blit(text, [175, 20])

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                udar_ob_stenu.play()
                audio_menu.play(loops=-1, fade_ms=0)
            porajenie_menu()
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if total % 5 == 0 and total > 0 and speed > 1:
            draw_block(pygame.Color('black'), ch.x, ch.y)

        if total % 3 == 0 and total > 0:
            draw_block(pygame.Color('purple'), buster.x, buster.y)

        if apple == head:
            if zvuk_vk:
                audio_apple.play()
            total += 1
            if total % 5 == 0 and total > 0:
                speed += 0
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        if buster == head:
            if zvuk_vk:
                eda_uskoreniye.play()
            speed += 1
            total -= 1
            buster = busters()

        if ch == head:
            if zvuk_vk:
                eda_zamedleniye.play()
            speed -= 1
            total += 1
            ch = medlenno()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                udar_ob_sebya.play()
                audio_menu.play(loops=0, fade_ms=0)
            porajenie_menu()
            break

        if total > 14:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name, "победа"
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                audio_menu.play(loops=0, fade_ms=0)
            pobeda_menu()
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


def level_three():
    if zvuk_vk:
        audio_menu.stop()
        audio_game.play(-1)

    def get_random_empty_block():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, COUNT_BLOCKS - 1)
            empty_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return empty_block

    def busters():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        busters_block = SnakeBlock(x, y)
        while busters_block in snake_blocks:
            busters_block.x = random.randint(0, COUNT_BLOCKS - 1)
            busters_block.y = random.randint(0, COUNT_BLOCKS - 1)
        return busters_block

    def medlenno():
        x = random.randint(0, COUNT_BLOCKS - 1)
        y = random.randint(0, COUNT_BLOCKS - 1)
        ch_blo = SnakeBlock(x, y)
        while ch_blo in snake_blocks:
            ch_blo.x = random.randint(0, COUNT_BLOCKS - 1)
            ch_blo.y = random.randint(0, COUNT_BLOCKS - 1)
        return ch_blo

    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global difficult
    global frame_count
    difficult = 3

    frame_count = -11

    running = True
    while running:
        total_seconds = int(frame_count // (speed + 3)) + speed * 5
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
        text = courier.render(output_string, True, pygame.Color('black'))
        frame_count += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif event.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif event.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif event.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
                elif event.key == pygame.K_SPACE:
                    p_pause()
        screen.fill(FRAME_COLOR)
        pygame.draw.rect(screen, HEADER_COLOR, [0, 0, size[0], HEADER_MARGIN])

        text_total = courier.render(f'Score:{total}', True, pygame.Color('black'))
        text_speed = courier.render(f'Speed:{speed}', True, pygame.Color('black'))
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 350, SIZE_BLOCK))
        screen.blit(text, [175, 20])

        for row in range(COUNT_BLOCKS):
            for column in range(COUNT_BLOCKS):
                if (row + column) % 2 == 0:
                    color = BLUE
                else:
                    color = WHITE

                draw_block(color, row, column)

        head = snake_blocks[-1]
        if not head.is_inside():
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                udar_ob_stenu.play()
                audio_menu.play(loops=-1, fade_ms=0)
            porajenie_menu()
            break

        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)

        if total % 5 == 0 and total > 0 and speed > 1:
            draw_block(pygame.Color('black'), ch.x, ch.y)

        if total % 3 == 0 and total > 0:
            draw_block(pygame.Color('purple'), buster.x, buster.y)

        if apple == head:
            if zvuk_vk:
                audio_apple.play()
            total += 1
            if total % 5 == 0 and total > 0:
                speed += 0
            snake_blocks.append(apple)
            apple = get_random_empty_block()

        if buster == head:
            if zvuk_vk:
                eda_uskoreniye.play()
            speed += 1
            total -= 1
            buster = busters()

        if ch == head:
            if zvuk_vk:
                eda_zamedleniye.play()
            speed -= 1
            total += 1
            ch = medlenno()

        d_row = buf_row
        d_col = buf_col
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)

        if new_head in snake_blocks:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                udar_ob_sebya.play()
                audio_menu.play(loops=0, fade_ms=0)
            porajenie_menu()
            break

        if total > 19:
            with open('history', 'r') as fin2:
                lines2 = fin2.readlines()
                sp2 = lines2
                rec2 = total, speed, output_string, lvl, name, "победа"
                sp2.append(str(rec2) + "\n")
                if len(sp2) > 15:
                    del sp2[0]
                with open('history', 'w') as f2:
                    li = ''
                    for i3 in sp2:
                        li += i3
                    f2.write(str(li))
            if zvuk_vk:
                audio_game.stop()
                audio_menu.play(loops=0, fade_ms=0)
            pobeda_menu()
            break

        snake_blocks.append(new_head)
        snake_blocks.pop(0)

        pygame.display.flip()
        timer.tick(3 + speed)


def set_difficulty(value, difficulty):
    global difficult
    difficult = difficulty


def start_nuzniy_game():
    global speed
    global frame_count
    if difficult == 3:
        if speed == 0:
            speed = 10
        if frame_count == 0:
            frame_count = 2
        level_three()
    elif difficult == 2:
        if speed == 0:
            speed = 5
        if frame_count == 0:
            frame_count = -11
        level_two()
    elif difficult == 1:
        if speed == 0:
            speed = 1
        if frame_count == 0:
            frame_count = -11
        level_one()
    elif difficult == 4:
        if speed == 0:
            speed = 1
        if frame_count == 0:
            frame_count = -11
        start_the_game()


def set_difficulty1(value1, difficulty1):
    global zvuk_vk
    zvuk_vk = difficulty1
    if zvuk_vk == 0:
        audio_game.stop()
        audio_menu.stop()
    elif zvuk_vk == 1:
        audio_menu.stop()
        audio_menu.play(-1)


def rekordi():
    screen2 = pygame.display.set_mode(size)
    pygame.display.set_caption('Records')
    timer2 = pygame.time.Clock()
    run = True
    with open('record', 'r') as fin:
        lines = fin.readlines()
        lst = ''
        sp = lines
        for j in sp:
            a = str(j)
            lst += ' ' + a
    while run:
        for event2 in pygame.event.get():
            if event2.type == pygame.QUIT:
                glavnoe_menu()
        screen2.fill(FRAME_COLOR)
        for i in range(len(sp)):
            font = pygame.font.SysFont('Arial', 25)
            follow = font.render(str(i + 1) + ") " + str(sp[i][:-1]), True, pygame.Color('black'), FRAME_COLOR)
            screen2.blit(follow, [5, i * 35 + 5])
        pygame.display.update()
        pygame.display.flip()
        timer2.tick(60)


def istoriya():
    screen3 = pygame.display.set_mode(size)
    pygame.display.set_caption('History')
    timer3 = pygame.time.Clock()
    with open('history', 'r') as fin2:
        lines2 = fin2.readlines()
        lst2 = ''
        sp2 = lines2
        for j2 in sp2:
            a2 = str(j2)
            lst2 += ' ' + a2
    run2 = True
    while run2:
        for event3 in pygame.event.get():
            if event3.type == pygame.QUIT:
                glavnoe_menu()
        screen3.fill(FRAME_COLOR)
        for i2 in range(len(sp2)):
            font2 = pygame.font.SysFont('Arial', 24)
            follow2 = font2.render(str(i2 + 1) + ") " + str(sp2[i2][:-1]), True, pygame.Color('black'), FRAME_COLOR)
            screen3.blit(follow2, [5, i2 * 35 + 5])
        pygame.display.update()
        pygame.display.flip()
        timer3.tick(60)


def pobeda_menu():
    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global frame_count
    frame_count = 0
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    d_row = buf_row = 0
    d_col = buf_col = 1
    apple = get_random_empty_block1()
    total = 0
    speed = 0
    buster = busters1()
    ch = medlenno1()
    menu = pygame_menu.Menu('Snake', 350, 272,
                            theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Заново:', start_nuzniy_game)
    menu.add.button('Главное меню:', glavnoe_menu)
    menu.add.selector('Звук:', [('Выкл', 0), ('Вкл', 1)], default=zvuk_vk, onchange=set_difficulty1)
    menu.add.button('Выйти:', pygame_menu.events.EXIT)

    while True:
        screen.blit(bg_image_pob, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()


def porajenie_menu():
    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global frame_count
    frame_count = 0
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    d_row = buf_row = 0
    d_col = buf_col = 1
    apple = get_random_empty_block1()
    total = 0
    speed = 0
    buster = busters1()
    ch = medlenno1()
    menu = pygame_menu.Menu('Snake', 350, 272,
                            theme=pygame_menu.themes.THEME_DARK)
    menu.add.button('Заново:', start_nuzniy_game)
    menu.add.button('Главное меню:', glavnoe_menu)
    menu.add.selector('Звук:', [('Выкл', 0), ('Вкл', 1)], default=zvuk_vk, onchange=set_difficulty1)
    menu.add.button('Выйти:', pygame_menu.events.EXIT)

    while True:
        screen.blit(bg_image_por, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()


def glavnoe_menu():
    global lvl
    global name
    global snake_blocks
    global apple
    global d_row
    global buf_row
    global d_col
    global buf_col
    global total
    global speed
    global buster
    global ch
    global frame_count
    frame_count = 0
    snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9), SnakeBlock(9, 10)]
    d_row = buf_row = 0
    d_col = buf_col = 1
    apple = get_random_empty_block1()
    total = 0
    speed = 0
    buster = busters1()
    ch = medlenno1()
    menu = pygame_menu.Menu('Snake', 350, 410,
                            theme=pygame_menu.themes.THEME_DARK)
    user_name = menu.add.text_input('Имя игрока: ', default=name)
    menu.add.selector('Уровень:', [('без конца', 4), ('первый', 1), ('второй', 2), ("третий", 3)],
                      default=(difficult % 4), onchange=set_difficulty)
    menu.add.selector('Звук:', [('Выкл', 0), ('Вкл', 1)], default=zvuk_vk, onchange=set_difficulty1)
    menu.add.button('Играть:', start_nuzniy_game)
    menu.add.button('Рекорды:', rekordi)
    menu.add.button('История игр:', istoriya)
    menu.add.button('Выйти:', pygame_menu.events.EXIT)

    while True:
        name = str(user_name.get_value())
        if difficult == 1:
            lvl = 'первый'
        elif difficult == 2:
            lvl = 'второй'
        elif difficult == 3:
            lvl = 'третий'
        elif difficult == 4:
            lvl = 'без конца'
        screen.blit(bg_image, (0, 0))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if menu.is_enabled():
            menu.update(events)
            menu.draw(screen)

        pygame.display.update()


glavnoe_menu()
