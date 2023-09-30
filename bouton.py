"""
classe Bouton
"""

import pygame

from texte import Texte


class Bouton:
    """Bouton
    message: texte du bouton
    """

    def __init__(self, message: Texte) -> None:
        self.message: Texte = message
        self.bouton: pygame.Rect = pygame.Rect(0, 0, 0, 0)

    def draw(
        self,
        couleur: pygame.Color,
        couleur_fond: pygame.Color,
        centerx: int,
        centery: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        fenetre = pygame.display.get_surface()
        self.message.genere_surface(couleur, centerx, centery)
        self.bouton = self.message.rect.inflate(15, 15)
        self.bouton.center = (centerx, centery)
        pygame.draw.rect(fenetre, couleur_fond, self.bouton, border_radius=20)
        self.message.draw(couleur, centerx, centery)

    def touche_souris(self) -> bool:
        """Détermine si la souris touche le bouton"""
        return self.bouton.collidepoint(pygame.mouse.get_pos())
