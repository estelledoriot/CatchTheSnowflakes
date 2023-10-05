"""
classe FilledSurface
"""

import pygame


class FilledSurface(pygame.sprite.Sprite):
    """surface unie"""

    def __init__(self, color: pygame.Color) -> None:
        super().__init__()
        size = pygame.display.get_window_size()
        self.image: pygame.Surface = pygame.Surface(
            size, flags=pygame.SRCALPHA
        )
        self.image.fill(color)
        self.rect: pygame.rect.Rect = self.image.get_rect()
