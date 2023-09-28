"""
classe Personnage
"""

import pygame

# TODO animation du personnage


class Personnage(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut se déplacer dans 2 directions
    centerx_depart, centery_depart: position initiale du personnage (centre)
    taille: taille du personnage à l'écran
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(
        self,
        centerx_depart: int,
        centery_depart: int,
        taille: int,
        vitesse: int,
    ) -> None:
        super().__init__()

        self.vitesse: int = vitesse

        self.image: pygame.Surface = pygame.image.load(
            "images/polar-bear.png"
        ).convert_alpha()
        self.image = pygame.transform.scale_by(
            self.image, taille / self.image.get_width()
        )
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.center = centerx_depart, centery_depart

    def update(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        pygame.sprite.Sprite.update(self)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.rect.x += self.vitesse
        elif pressed[pygame.K_LEFT]:
            self.rect.x -= self.vitesse
