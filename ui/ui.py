import pygame

class UIElement:
    def __init__(self,label, x, y, width, height, color=(255, 255, 255)):
        self.label = label
        
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

        self.active = True
        self.visible = True

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def set_size(self, width, height):
        self.rect.width = width
        self.rect.height = height

    def is_clicked(self, pos):
        return self.active and self.rect.collidepoint(pos)

class Text:
    """Parameters: font name, size, text content, color (RGB), x position, y position"""
    def __init__(self, font_name, font_size, text, color, pos_x, pos_y):
        self.font = pygame.font.Font(font_name, font_size)
        self.text = text
        self.color = color

        self.pos_x = pos_x
        self.pos_y = pos_y

    def draw(self, game):
        self.text = game.trainer.pokedex[0].moove1 #Change button label to move name
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=(self.pos_x, self.pos_y))
        game.screen.blit(self.surface, self.rect)

        #def update_text(self, new_text): // TODO need fix on this
        #self.text = new_text
        #self.surface = self.font.render(self.text, True, self.color)
        #self.rect = self.surface.get_rect(center=(self.pos_x, self.pos_y))