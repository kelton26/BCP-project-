import pygame
import sys
import random

pygame.init()

screen = pygame.display.set_mode((1280, 720))

MENU = 0
GAME = 1
END = 2
state = MENU


font = pygame.font.SysFont(None, 90)
font = pygame.font.SysFont(None, 60)
big_font = pygame.font.SysFont(None, 90)
tries_font = pygame.font.SysFont(None, 120)


text = font.render("Hangman 26", True, (255, 255, 255)) 
shadow = font.render("Hangman 26", True, (0, 0, 0))
text_rect = text.get_rect(midtop=(640, 100)) 
shadow_rect = shadow.get_rect(midtop=(640, 105))


background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (1280, 720))
sub_imag = pygame.image.load("hang.png")
sub_image = pygame.transform.scale(sub_imag, (500, 700))
man_images = [
    pygame.image.load("man1.png"),
    pygame.image.load("man2.png"),
    pygame.image.load("man3.png"),
    pygame.image.load("man4.png"),
    pygame.image.load("man5.png"),
    pygame.image.load("man6.png"),
]
for i in range(len(man_images)):
    man_images[i] = pygame.transform.scale(man_images[i], (400, 400))
win_image = pygame.image.load("win.png")
win_image = pygame.transform.scale(win_image, (400, 400))
lose_image = pygame.image.load("lose.png")
lose_image = pygame.transform.scale(lose_image, (800, 400))


button = pygame.Rect(415, 260, 450, 200)


words = ["PYTHON", "HANGMAN", "SIMULATOR", "CODE"]
word = random.choice(words)
correct = []
wrong = []
max_tries = 6
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
box_rects = []
start_x = 350
start_y = 600
spacing = 45
for i, l in enumerate(letters):
    rect = pygame.Rect(start_x + (i % 13) * spacing, start_y + (i // 13) * 60, 40, 40)
    box_rects.append((l, rect))


def draw_tries():
    tries_left = max_tries - len(wrong)
    color = (200, 50, 50) if tries_left <= 3 else (0, 0, 0)
    text = tries_font.render(f"Tries: {tries_left}", True, color)
    screen.blit(text, (20, 20))



def draw_word():
    display = ""
    for l in word:
        display += l + " " if l in correct else "_ "
    text = big_font.render(display, True, (0, 0, 0))
    screen.blit(text, text.get_rect(center=(640, 450)))



def draw_letters():
    for letter, rect in box_rects:
        if letter in correct:
            color = (0, 200, 0)
        elif letter in wrong:
            color = (200, 0, 0)
        else:
            color = (0, 0, 0)

        pygame.draw.rect(screen, color, rect, 2)
        txt = font.render(letter, True, color)
        screen.blit(txt, (rect.x + 5, rect.y + 2))



def draw_man():
    index = min(len(wrong), len(man_images) - 1)
    img = man_images[index]
    rect = img.get_rect(midright=(1200, 350))
    screen.blit(img, rect)



def draw_end(win):
    screen.fill((255, 255, 255))
    if win:
        text = big_font.render("your comrade is saved", True, (0, 200, 0))
        img = win_image
    else:
        text = big_font.render("comrade has been killed", True, (200, 0, 0))
        img = lose_image
    screen.blit(text, text.get_rect(center=(640, 120)))
    screen.blit(img, img.get_rect(center=(640, 400)))
    word_text = big_font.render(f"The word was: {word}", True, (0, 0, 0))
    screen.blit(word_text, word_text.get_rect(center=(640, 650)))

while True:
    screen.fill((255, 255, 255))
    mouse = pygame.mouse.get_pos()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == MENU and button.collidepoint(mouse):
                state = GAME


        if event.type == pygame.KEYDOWN and state == GAME:
            key = event.unicode.upper()
            if key in letters:
                if key in word and key not in correct:
                    correct.append(key)
                elif key not in word and key not in wrong:
                    wrong.append(key)


    if state == MENU:
        screen.blit(background, (0, 0))
        screen.blit(shadow, shadow_rect) 
        screen.blit(text, text_rect)
        button_surface = pygame.Surface((button.width, button.height), pygame.SRCALPHA)
        button_color = (0, 0, 0, 140)
        pygame.draw.rect(
            button_surface,
            button_color,
            button_surface.get_rect(),
            border_radius=40
        )
        txt = font.render("START", True, (255, 255, 255))
        txt_rect = txt.get_rect(center=(button.width // 2, button.height // 2))
        button_surface.blit(txt, txt_rect)
        screen.blit(button_surface, button.topleft)


    elif state == GAME:
        screen.blit(sub_image, (-10, 150))
        draw_word()
        draw_letters()
        draw_tries()
        draw_man()

        if all(l in correct for l in word):
            state = END
            win = True

        if len(wrong) >= max_tries:
            state = END
            win = False

    elif state == END:
        draw_end(win)

    pygame.display.update()
