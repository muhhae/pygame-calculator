import pygame

print("Button.py imported")


class Button:
    def __init__(self, x: int, y: int, width: int, height: int,
                 text: str, color: pygame.Color,
                 text_color: pygame.Color,
                 font: pygame.font.Font):
        self.color = color
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)

        self.text_content = text
        self.text = font.render(text, True, text_color)

        self.text_rect = self.text.get_rect(center=self.rect.center)

        self.hovered = False
        
        self.on_click = lambda x: None
        self.on_hover = lambda x: None
        self.on_update = lambda x: None
        
        self.hovered_color = self.color + pygame.Color(30, 30, 30)

    def draw(self, screen):
        self.on_update(self)
        draw_color = self.hovered_color if self.hovered else self.color
        pygame.draw.rect(screen, draw_color, self.rect, border_radius=10)
            
        screen.blit(self.text, self.text_rect)
    
    def handleEvent(self, event: pygame.event.Event):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered:
            self.on_hover(self)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.on_click(self)
