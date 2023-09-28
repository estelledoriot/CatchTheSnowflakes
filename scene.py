"""scènes du jeu"""

import pygame

from typing import Protocol

from personnage import Personnage
from objet import Objet
from countdown import Countdown
from score import Score
from vies import Vies


class Scene(Protocol):
    def affiche_scene(self) -> None:
        ...

    def joue_tour(self) -> None:
        ...

    def passe_suivant(self) -> bool:
        ...


class Partie:
    """Partie de labyrinthe"""

    def __init__(self) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.fond: Objet = Objet(
            "images/mountain.png", largeur // 2, hauteur // 2, largeur
        )
        self.bear: Personnage = Personnage(largeur // 2, hauteur - 50, 100, 10)
        self.countdown: Countdown = Countdown(60)
        self.score: Score = Score()
        self.vies: Vies = Vies(3)
        self.son_ok: pygame.mixer.Sound = pygame.mixer.Sound("sounds/coin.wav")
        self.son_ok.set_volume(0.25)
        self.son_ko: pygame.mixer.Sound = pygame.mixer.Sound("sounds/laser.wav")
        self.son_ko.set_volume(0.25)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()
        fenetre.blit(self.fond.image, self.fond.rect)
        fenetre.blit(self.bear.image, self.bear.rect)
        self.countdown.draw()
        self.score.draw()
        self.vies.draw(500, 30)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements de l'ours
        self.bear.update()

        # mise à jour du timer
        self.countdown.update()
        self.score.update()

    def passe_suivant(self) -> bool:
        """Teste si la partie est terminée"""
        return self.vies.mort
