"""scènes du jeu"""

import pygame

from typing import Protocol
from objet import Objet

from personnage import Personnage
from fond import Fond
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

        self.fond: Fond = Fond(
            "images/mountain.png", largeur // 2, hauteur // 2, largeur
        )
        self.bear: Personnage = Personnage(largeur // 2, hauteur - 50, 150, 10)
        self.snowflakes: pygame.sprite.Group = pygame.sprite.Group()
        self.lightnings: pygame.sprite.Group = pygame.sprite.Group()

        self.countdown: Countdown = Countdown(60)
        self.score: Score = Score()
        self.vies: Vies = Vies(3)

        self.son_ok: pygame.mixer.Sound = pygame.mixer.Sound("sounds/coin.wav")
        self.son_ok.set_volume(0.25)
        self.son_ko: pygame.mixer.Sound = pygame.mixer.Sound("sounds/laser.wav")
        self.son_ko.set_volume(0.25)

        self.new_snowflake: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_snowflake, 600)
        self.new_lightning: int = pygame.USEREVENT + 2
        pygame.time.set_timer(self.new_lightning, 1000)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.fond.image, self.fond.rect)
        fenetre.blit(self.bear.image, self.bear.rect)
        self.snowflakes.draw(fenetre)
        self.lightnings.draw(fenetre)

        self.countdown.draw()
        self.score.draw()
        self.vies.draw(80, 45)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements de l'ours
        self.bear.update()

        # générer les nouveaux objets
        for _ in pygame.event.get(self.new_snowflake):
            self.snowflakes.add(Objet("images/snowflake.png", 50, 8))

        for _ in pygame.event.get(self.new_lightning):
            self.lightnings.add(Objet("images/lightning.png", 25, 15))

        # faire tomber les objets
        self.snowflakes.update()
        self.lightnings.update()

        # collisions
        if pygame.sprite.spritecollide(self.bear, self.snowflakes, True):
            self.score.ajoute_points(1)
            self.son_ok.play()
        if pygame.sprite.spritecollide(self.bear, self.lightnings, True):
            self.vies.perd(1)
            self.son_ko.play()

        # mise à jour du timer et du score
        self.countdown.update()
        self.score.update()

    def passe_suivant(self) -> bool:
        """Teste si la partie est terminée"""
        return self.vies.mort or self.countdown.temps_restant <= 0
