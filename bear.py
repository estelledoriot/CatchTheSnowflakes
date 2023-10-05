"""
classe Bear
"""

from enum import Enum

import pygame

Direction = Enum("Direction", ["DROITE", "GAUCHE"])


class Bear(pygame.sprite.Sprite):
    """Personnage du jeu
    Peut se déplacer dans 2 directions
    start_center: position initiale du personnage (centre)
    size: taille du personnage à l'écran
    vitesse: vitesse de déplacement du personnage
    """

    def __init__(
        self,
        start_center: tuple[int, int],
        size: int,
        speed: int,
    ) -> None:
        super().__init__()

        # images
        self.images: list[pygame.Surface] = [
            pygame.image.load(f"images/polar_bear_{i}.png").convert_alpha()
            for i in range(1, 4)
        ]
        for i, image in enumerate(self.images):
            self.images[i] = pygame.transform.scale_by(
                image, size / image.get_width()
            )
        self.image: pygame.Surface = self.images[0]

        # rectangle
        self.rect: pygame.Rect = self.image.get_rect(center=start_center)

        # costumes
        self.image_number: float = 0
        self.direction: Direction = Direction.DROITE
        self.is_visible: bool = True
        self.is_hit: bool = False
        self.flash_start_time: int = 0

        # vitesse
        self.speed: int = speed

    def change_costume(self) -> None:
        """Change le costume du personnage"""

        self.image = self.images[int(self.image_number) % 3]
        if self.direction == Direction.GAUCHE:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center=self.rect.center)

    def start_flashing(self) -> None:
        """Lance le timer pour le clignotement"""
        self.flash_start_time = pygame.time.get_ticks()
        self.is_hit = True

    def update(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        largeur, _ = pygame.display.get_window_size()
        pygame.sprite.Sprite.update(self)

        if not self.is_hit:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT] and self.rect.right < largeur:
                self.rect.x += self.speed
                self.direction = Direction.DROITE
                self.image_number += 0.2
            elif pressed[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.speed
                self.direction = Direction.GAUCHE
                self.image_number += 0.2
        elif pygame.time.get_ticks() - self.flash_start_time < 100:
            self.is_visible = False
        elif pygame.time.get_ticks() - self.flash_start_time < 200:
            self.is_visible = True
        elif pygame.time.get_ticks() - self.flash_start_time < 300:
            self.is_visible = False
        else:
            self.is_visible = True
            self.is_hit = False

        self.change_costume()
