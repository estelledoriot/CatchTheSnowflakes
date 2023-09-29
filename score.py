"""
classe Score
"""

import pygame

from texte import Texte


class Score:
    """score du joueur"""

    def __init__(self) -> None:
        self.score = 0
        self.etiquette: Texte = Texte(str(self.score), "font/Avdira.otf", 40)

    def ajoute_points(self, amount: int) -> None:
        """Ajoute des points"""
        self.score += amount

    def update(self) -> None:
        """Mise à jour du nombre à afficher"""
        self.etiquette.texte = str(self.score)

    def draw(self) -> None:
        """Affiche le score"""
        largeur, _ = pygame.display.get_window_size()
        couleur_score = pygame.Color(240, 240, 240)
        self.etiquette.draw(couleur_score, largeur // 2, 60)
