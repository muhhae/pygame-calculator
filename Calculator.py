# import sys, os

# sys.stdout = open(os.devnull, "w")
# sys.stderr = open(os.devnull, "w")

import pygame
import copy

from Button import Button
from InfixToPostfix import infixToPostfix, calculatePostfix, listToStr, bracketFunc

pygame.init()

pygame.display.set_icon(pygame.image.load("icon.png"))
pygame.display.set_caption("Calculator")

screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

running = True

inputting = True
true_value = "0"
postfix_value = "0"
bracket_value = "0"
mode = "Calculate"

input_font = pygame.font.SysFont("firacode", 28)
input_text = ""
input_field = input_font.render(input_text, True, pygame.Color("black"))
input_field_rect = input_field.get_rect(center=(45, 50))

inp_rect = pygame.Rect(0, 0, 340, 180)
inp_rect.center = (200, 120)


def drawMultilineText(screen, font, text: str, color: pygame.Color,
                      text_rect: pygame.Rect, max_char: int):
    n = 0
    temp_rect = copy.copy(text_rect)
    while n < len(text):
        screen.blit(font.render(text[n:n + max_char], True, color),
                    temp_rect)
        n += max_char
        temp_rect.y += font.get_height()


def calc():
    global true_value, postfix_value, bracket_value, inputting
    try:
        postfix_res = infixToPostfix(true_value)
        bracket_res = bracketFunc(postfix_res)
        result = calculatePostfix(postfix_res)

        result = int(result) if result % 1 == 0 else result
        match mode:
            case "Calculate":
                true_value = str(result)
            case "Postfix":
                postfix_value = listToStr(postfix_res)
            case "BracketFunct":
                bracket_value = bracket_res
        inputting = False
        return 1
    except:
        true_value = "Syntax Error"
        return 0


def inputButton(button: Button):
    global true_value, postfix_value, bracket_value, inputting

    if true_value in ["Syntax Error"]:
        true_value = "0"

    if button.text_content == "=":
        if calc():
            return

    elif button.text_content == "⌫":
        true_value = true_value[:-1]

    else:
        if true_value == "0":
            true_value = ""
        true_value += button.text_content

    if true_value == "":
        true_value = "0"

    inputting = True


button_size = 60

gap = [0, 0]
gap_size = 10
button_list = []

inp = [1, 2, 3, "+", "-",
       4, 5, 6, "*", "/",
       7, 8, 9, "(", ")",
       ".", 0, "⌫", "^", "="]

for i, e in enumerate(inp):

    x = (i % 5 + 1) * button_size - gap_size + gap[0] + 10
    y = (int(i / 5) + 1) * button_size - gap_size + gap[1] + 290

    gap[0] += gap_size

    if (i + 1) % 5 == 0:
        gap[1] += gap_size
        gap[0] = 0

    font = pygame.font.SysFont("firacode", 25)
    button_color = pygame.Color("grey25")

    if e in ["+", "-", "*", "/", "^", "(", ")", "=", "."]:
        button_color = pygame.Color("goldenrod")
    if e == "⌫":
        button_color = pygame.Color("orangered1")
        font = pygame.font.SysFont("firacode", 30)

    button_temp = Button(x, y, button_size, button_size,
                         str(e), button_color, pygame.Color("white"),
                         font)
    button_temp.on_click = inputButton

    button_list.append(button_temp)

input_text = "0"
line_start = 0


def changeMode(button: Button):
    global mode
    mode_list = ["Calculate", "Postfix", "BracketFunct"]
    mode = button.text_content

    i = mode_list.index(mode) + 1
    if i >= len(mode_list):
        i = 0
    button.text_content = mode_list[i]
    mode = mode_list[i]


def ac(button: Button):
    global true_value, postfix_value, bracket_value
    true_value = "0"
    postfix_value = "0"
    bracket_value = "0"


def line_up(button: Button):
    global line_start
    line_start -= 1


def line_down(button: Button):
    global line_start
    line_start += 1


button_mode = Button(2 * button_size + 10, - button_size - gap_size + gap[1] + 290,
                     button_size * 3 + gap_size *
                     2, button_size, mode, pygame.Color("lightseagreen"),
                     pygame.Color("white"), pygame.font.SysFont("firacode", 22))
button_mode.on_click = changeMode
button_list.append(button_mode)

button_ac = Button(5 * button_size - gap_size * 3, - button_size - gap_size + gap[1] + 290,
                   button_size, button_size, "AC", pygame.Color("orangered1"),
                   pygame.Color("white"), pygame.font.SysFont("firacode", 26))
button_ac.on_click = ac
button_list.append(button_ac)

button_up = Button(6 * button_size - gap_size * 2, (- button_size - gap_size - 1 + gap[1])/2*3 + 290,
                   button_size, button_size / 2 -
                   5, "/\\", pygame.Color("lightskyblue3"),
                   pygame.Color("white"), pygame.font.SysFont("firacode", 20))
button_up.on_click = line_up
button_list.append(button_up)

button_down = Button(6 * button_size - gap_size * 2, (- button_size - gap_size + 1 + gap[1])/2 + 290,
                     button_size, button_size / 2 -
                     5, "\\/", pygame.Color("lightskyblue3"),
                     pygame.Color("white"), pygame.font.SysFont("firacode", 20))
button_down.on_click = line_down
button_list.append(button_down)

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        for button in button_list:
            button.handleEvent(event)
        if event.type == pygame.KEYDOWN:
            if true_value == "Syntax Error":
                true_value = "0"
            match event.key:
                case pygame.K_BACKSPACE:
                    true_value = true_value[:-1]
                    if true_value == "":
                        true_value = "0"
                case pygame.K_ESCAPE:
                    true_value = "0"
                case pygame.K_DOWN:
                    line_start += 1
                case pygame.K_UP:
                    line_start -= 1
            if 48 <= event.key <= 57:
                if true_value == "0":
                    true_value = ""
                true_value += str(event.key - 48)
                inputting = True
        if event.type == pygame.QUIT:
            running = False

    text_to_show = ""
    match button_mode.text_content:
        case "Calculate":
            text_to_show = true_value
        case "Postfix":
            text_to_show = postfix_value
        case "BracketFunct":
            text_to_show = bracket_value

    if text_to_show == "0":
        text_to_show = true_value

    if inputting:
        text_to_show = true_value

    if line_start < 0 or len(text_to_show) / 18 <= 5:
        line_start = 0

    max_line_start = len(text_to_show) / 18 - 4

    if max_line_start < 0:
        max_line_start = 0

    if line_start > max_line_start:
        line_start = int(max_line_start)

    index_start = line_start * 18
    index_end = index_start + 18 * 5

    if index_end > len(text_to_show):
        index_end = len(text_to_show)

    input_text = text_to_show[index_start: index_end]

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
