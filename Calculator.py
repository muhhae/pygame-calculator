# import sys, os

# sys.stdout = open(os.devnull, "w")
# sys.stderr = open(os.devnull, "w")

import pygame
import copy

from Button import Button
from InfixToPostfix import infixToPostfix, calculatePostfix

pygame.init()

pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("Calculator")

screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

running = True

input_font = pygame.font.SysFont("digital7mono", 40)
input_text = ""
input_field = input_font.render(input_text, True, pygame.Color("black"))
input_field_rect = input_field.get_rect(center=(38, 33))

inp_rect = pygame.Rect(0, 0, 340, 280)
inp_rect.center = (200, 150)


def drawMultilineText(screen, font, text: str, color: pygame.Color,
                      text_rect: pygame.Rect, max_char: int):
    n = 0
    temp_rect = copy.copy(text_rect)
    while n < len(text):
        screen.blit(font.render(text[n:n + max_char], True, color),
                    temp_rect)
        n += max_char
        temp_rect.y += font.get_height() + 10


def inputButton(button: Button):

    # print("button:", button.text_content)

    global input_text

    if input_text in ["Syntax Error"]:
        input_text = "0"

    if button.text_content == "=":
        try:
            result = calculatePostfix(infixToPostfix(input_text))
            result = int(result) if result % 1 == 0 else result
            input_text = str(result)
        except:
            input_text = "Syntax Error"

    elif button.text_content == "<-":
        input_text = input_text[:-1]

    else:
        if input_text == "0":
            input_text = ""
        input_text += button.text_content

    if input_text == "":
        input_text = "0"


button_size = 60

gap = [0, 0]
gap_size = 10
button_list = []

inp = [1, 2, 3, "+", "-",
       4, 5, 6, "*", "/",
       7, 8, 9, "(", ")",
       ".", 0, "<-", "^", "="]

for i, e in enumerate(inp):

    x = (i % 5 + 1) * button_size - gap_size + gap[0] + 10
    y = (int(i / 5) + 1) * button_size - gap_size + gap[1] + 290

    gap[0] += gap_size

    if (i + 1) % 5 == 0:
        gap[1] += gap_size
        gap[0] = 0

    button_color = pygame.Color("grey25")
    if e in ["+", "-", "*", "/", "^", "(", ")", "=", "."]:
        button_color = pygame.Color("goldenrod")
    if e == "<-":
        button_color = pygame.Color("orangered1")

    button_temp = Button(x, y, button_size, button_size,
                         str(e), button_color, pygame.Color("white"),
                         pygame.font.SysFont("firacode", 25))
    button_temp.on_click = inputButton

    button_list.append(button_temp)

input_text = "0"

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        for button in button_list:
            button.handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if input_text in ["Syntax Error"]:
                input_text = "0"
            match event.key:
                case pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    if input_text == "":
                        input_text = "0"
                case pygame.K_ESCAPE:
                    input_text = "0"
            if 48 <= event.key <= 57:
                if input_text == "0":
                    input_text = ""
                input_text += str(event.key - 48)
        if event.type == pygame.QUIT:
            running = False

    if len(input_text) > 18 * 8:
        input_text = input_text[:18 * 8]

    screen.fill("honeydew4")

    pygame.draw.rect(screen, pygame.Color("gray"), inp_rect,
                     border_radius=10)

    for button in button_list:
        button.draw(screen)

    drawMultilineText(screen, input_font, input_text,
                      pygame.Color("black"), input_field_rect, 18)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
