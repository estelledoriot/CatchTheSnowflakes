"""
classe Background
"""

import pygame


class Background(pygame.sprite.Sprite):
    """Objet du jeu
    filename: nom du fichier contenant l'objet
    start_center: position initiale de l'objet (centre)
    width: largeur de l'objet à l'écran
    """

    def __init__(
        self,
        filename: str,
        start_center: tuple[int, int],
        width: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(
            filename
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, width / self.image.get_width()
        )
        self.rect: pygame.Rect = self.image.get_rect(center=start_center)
