"""
classe Vies
"""

import pygame


class Vies:
    """Gestion des vies"""

    def __init__(self, vies_max: int) -> None:
        self.vies: int = vies_max
        self.image = pygame.image.load("images/heart.png").convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, 30 / self.image.get_width()
        )

    def perd(self, nombre: int) -> None:
        """Perd des vies"""
        self.vies -= nombre

    def draw(self, x: int, y: int) -> None:
        """Affiche les vies"""
        fenetre = pygame.display.get_surface()
        for i in range(self.vies):
            fenetre.blit(self.image, (x + i * (self.image.get_width() + 5), y))

    @property
    def mort(self) -> bool:
        """Détermine si le personnage est mort"""
        return self.vies == 0
