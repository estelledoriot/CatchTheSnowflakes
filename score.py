"""
classe Score
"""

import pygame


class Score(pygame.sprite.Sprite):
    """score du joueur
    posiion: position du score"""

    def __init__(self, position: tuple[int, int]) -> None:
        super().__init__()
        self.score: int = 0
        self.font: pygame.font.Font = pygame.font.Font("font/Avdira.otf", 40)
        self.score_color: pygame.Color = pygame.Color(240, 240, 240)
        self.image: pygame.Surface = self.font.render(
            str(self.score), True, self.score_color
        )
        self.position: tuple[int, int] = position
        self.rect: pygame.Rect = self.image.get_rect(center=self.position)

    def add_points(self, amount: int) -> None:
        """Ajoute des points"""
        self.score += amount

    def update(self) -> None:
        """Mise à jour du nombre à afficher"""
        self.image = self.font.render(str(self.score), True, self.score_color)
        self.rect = self.image.get_rect(center=self.position)
