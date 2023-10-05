"""
classe Lives
"""

import pygame


class Lives(pygame.sprite.Sprite):
    """Gestion des vies"""

    def __init__(self, vies_max: int, position: tuple[int, int]) -> None:
        super().__init__()
        self.lives: int = vies_max
        self.heart: pygame.Surface = pygame.image.load(
            "images/heart.png"
        ).convert_alpha()
        self.heart = pygame.transform.scale_by(
            self.heart, 30 / self.heart.get_width()
        )
        self.image: pygame.Surface = pygame.Surface(
            (35 * vies_max, 35), flags=pygame.SRCALPHA
        )
        self.rect: pygame.rect.Rect = self.image.get_rect(topleft=position)

    @property
    def is_dead(self) -> bool:
        """Détermine si le personnage est mort"""
        return self.lives <= 0

    def lose(self, amount: int) -> None:
        """Perd des vies"""
        self.lives -= amount

    def update(self) -> None:
        """Affiche les vies"""
        self.image.fill(pygame.Color(0, 0, 0, 0))
        for i in range(self.lives):
            self.image.blit(self.heart, (i * (self.heart.get_width() + 5), 0))
