"""
classe Objet
"""

import pygame


class Objet(pygame.sprite.Sprite):
    """Objet du jeu
    filename: nom du fichier contenant l'objet
    centerx_depart, centery_depart: position initiale de l'objet (centre)
    largeur_objet: largeur de l'objet à l'écran
    """

    def __init__(
        self,
        filename: str,
        centerx_depart: int,
        centery_depart: int,
        largeur_objet: int,
    ) -> None:
        super().__init__()

        self.image: pygame.Surface = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, largeur_objet / self.image.get_width()
        )
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)
        self.rect: pygame.Rect = self.image.get_rect(
            center=(centerx_depart, centery_depart)
        )
