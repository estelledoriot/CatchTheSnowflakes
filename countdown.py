"""
classe Countdown
"""

import pygame

from texte import Texte


class Countdown:
    """Countdown: en charge du compte à rebours"""

    def __init__(self, temps_total: int) -> None:
        self.start: int = pygame.time.get_ticks()
        self.temps_total: int = temps_total
        self.etiquette: Texte = Texte(
            str(self.temps_restant), "font/Avdira.otf", 40
        )

    @property
    def temps_restant(self) -> int:
        """Calcule le temps restant"""
        return (
            self.temps_total - (pygame.time.get_ticks() - self.start) // 1000
        )

    def update(self) -> None:
        """Mise à jour du nombre à afficher"""
        self.etiquette.texte = str(self.temps_restant)

    def draw(self) -> None:
        """Affiche le timer à l'écran"""
        largeur, _ = pygame.display.get_window_size()
        couleur_timer = pygame.Color(235, 80, 63)
        self.etiquette.draw(couleur_timer, largeur - 80, 60)
