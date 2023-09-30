"""
classe Personnage
"""

import pygame


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

        self.images: list[pygame.Surface] = [
            pygame.image.load(f"images/polar_bear_{i}.png").convert_alpha()
            for i in range(1, 4)
        ]
        for i, image in enumerate(self.images):
            self.images[i] = pygame.transform.scale_by(
                image, taille / image.get_width()
            )

        self.numero_costume: float = 0
        self.direction: str = "droite"
        self.image: pygame.Surface = self.images[0]
        self.rect: pygame.Rect = self.image.get_rect(
            center=(centerx_depart, centery_depart)
        )

        self.clignote_timer: int = 0
        self.touche: bool = False
        self.visible: bool = True

    def update(self) -> None:
        """Déplacement du personnage suivant les touches pressées"""
        largeur, _ = pygame.display.get_window_size()
        pygame.sprite.Sprite.update(self)

        if not self.touche:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RIGHT] and self.rect.right < largeur:
                self.rect.x += self.vitesse
                self.direction = "droite"
                self.numero_costume += 0.2
            elif pressed[pygame.K_LEFT] and self.rect.left > 0:
                self.rect.x -= self.vitesse
                self.direction = "gauche"
                self.numero_costume += 0.2
        elif pygame.time.get_ticks() - self.clignote_timer < 100:
            self.visible = False
        elif pygame.time.get_ticks() - self.clignote_timer < 200:
            self.visible = True
        elif pygame.time.get_ticks() - self.clignote_timer < 300:
            self.visible = False
        else:
            self.visible = True
            self.touche = False

        self.change_costume()

    def change_costume(self) -> None:
        """Change le costume du personnage"""

        self.image = self.images[int(self.numero_costume) % 3]
        if self.direction == "gauche":
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect = self.image.get_rect(center=self.rect.center)

    def clignote(self) -> None:
        """Lance le timer pour le clignotement"""
        self.clignote_timer = pygame.time.get_ticks()
        self.touche = True
