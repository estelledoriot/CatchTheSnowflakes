"""
classe Object
"""

from random import randint

import pygame


class Object(pygame.sprite.Sprite):
    """Objets qui tombent du ciel
    filename: nom du fichier
    width: taille de l'objet
    speed: vitesse de déplacement de l'objet
    """

    def __init__(
        self,
        filename: str,
        width: int,
        speed: int,
    ) -> None:
        super().__init__()

        screen_width, _ = pygame.display.get_window_size()

        # image
        self.image: pygame.Surface = pygame.image.load(
            filename
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, width / self.image.get_width()
        )

        # rectangle
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.x = randint(0, screen_width - self.image.get_width())

        # vitesse
        self.speed: int = speed

    def update(self) -> None:
        """Fait avancer le personnage"""
        _, screen_width = pygame.display.get_window_size()

        self.rect.y += self.speed

        if self.rect.y > screen_width:
            self.kill()
