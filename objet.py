"""
classe Objet
"""

from random import randint

import pygame


class Objet(pygame.sprite.Sprite):
    """Objets qui tombent du ciel
    filename: nom du fichier
    taille: taille de l'objet
    vitesse: vitesse de déplacement de l'objet
    """

    def __init__(
        self,
        filename: str,
        taille: int,
        vitesse: int,
    ) -> None:
        super().__init__()

        largeur, _ = pygame.display.get_window_size()

        self.vitesse: int = vitesse

        self.image: pygame.Surface = pygame.image.load(
            filename
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, taille / self.image.get_width()
        )
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.bottom = 0
        self.rect.x = randint(0, largeur - self.image.get_width())

    def update(self) -> None:
        """Fait avancer le personnage"""
        _, hauteur = pygame.display.get_window_size()

        self.rect.y += self.vitesse

        if self.rect.y > hauteur:
            self.kill()
