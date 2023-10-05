"""scènes du jeu"""

from typing import Protocol

import pygame

from background import Background
from bear import Bear
from button import Button
from countdown import Countdown
from lives import Lives
from object import Object
from score import Score
from text import Text


class Scene(Protocol):
    """Scènes du jeu"""

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

        self.fond: Background = Background(
            "images/mountain.png", (largeur // 2, hauteur // 2), largeur
        )
        self.bear: Bear = Bear((largeur // 2, hauteur - 50), 150, 10)
        self.snowflakes: pygame.sprite.Group = pygame.sprite.Group()
        self.lightnings: pygame.sprite.Group = pygame.sprite.Group()

        self.countdown: Countdown = Countdown(60, (largeur - 80, 60))
        self.score: Score = Score((largeur // 2, 60))
        self.vies: Lives = Lives(3, (80, 45))

        self.son_ok: pygame.mixer.Sound = pygame.mixer.Sound("sounds/coin.wav")
        self.son_ok.set_volume(0.15)
        self.son_ko: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/laser.wav"
        )
        self.son_ko.set_volume(0.25)

        self.new_snowflake: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_snowflake, 600)
        self.new_lightning: int = pygame.USEREVENT + 2
        pygame.time.set_timer(self.new_lightning, 1000)

    def affiche_scene(self) -> None:
        """Affiche les éléments du jeu"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.fond.image, self.fond.rect)
        if self.bear.is_visible:
            fenetre.blit(self.bear.image, self.bear.rect)
        self.snowflakes.draw(fenetre)
        self.lightnings.draw(fenetre)

        fenetre.blit(self.countdown.image, self.countdown.rect)
        fenetre.blit(self.score.image, self.score.rect)
        fenetre.blit(self.vies.image, self.vies.rect)

    def joue_tour(self) -> None:
        """Joue un tour du jeu"""
        # déplacements de l'ours
        self.bear.update()

        # générer les nouveaux objets
        for _ in pygame.event.get(self.new_snowflake):
            self.snowflakes.add(Object("images/snowflake.png", 50, 8))

        for _ in pygame.event.get(self.new_lightning):
            self.lightnings.add(Object("images/lightning.png", 25, 15))

        # faire tomber les objets
        self.snowflakes.update()
        self.lightnings.update()

        # collisions
        if pygame.sprite.spritecollide(self.bear, self.snowflakes, True):
            self.score.add_points(1)
            self.son_ok.play()
        if pygame.sprite.spritecollide(self.bear, self.lightnings, True):
            self.vies.lose(1)
            self.son_ko.play()
            self.bear.start_flashing()

        # mise à jour du timer et du score
        self.countdown.update()
        self.score.update()
        self.vies.update()

    def passe_suivant(self) -> bool:
        """Teste si la partie est terminée"""
        return self.vies.is_dead or self.countdown.time_finished


class Fin:
    """Scène de fin"""

    def __init__(self, score: int) -> None:
        largeur, hauteur = pygame.display.get_window_size()

        self.decors: Background = Background(
            "images/mountain.png", (largeur // 2, hauteur // 2), largeur
        )
        self.masque: pygame.Surface = pygame.Surface(
            (largeur, hauteur), flags=pygame.SRCALPHA
        )
        self.masque.fill(pygame.Color(230, 230, 230, 150))

        record: int = 0
        with open("record.txt", "r", encoding="utf-8") as fichier:
            record: int = int(fichier.read())

        if score > record:
            record = score
            self.message_fin: Text = Text(
                "Nouveau record",
                100,
                pygame.Color(137, 122, 194),
                (largeur // 2, 350),
            )
            with open("record.txt", "w", encoding="utf-8") as fichier:
                fichier.write(str(score))
        else:
            self.message_fin: Text = Text(
                "Perdu ...",
                100,
                pygame.Color(137, 122, 194),
                (largeur // 2, 350),
            )

        self.texte_score: Text = Text(
            f"Score : {score}",
            50,
            pygame.Color(28, 42, 73),
            (largeur // 2, 100),
        )
        self.texte_record: Text = Text(
            f"Record : {record}",
            50,
            pygame.Color(28, 42, 73),
            (largeur // 2, 170),
        )

        self.son_fin: pygame.mixer.Sound = pygame.mixer.Sound("sounds/end.wav")
        self.son_fin.set_volume(0.25)
        self.son_fin.play()

        self.bouton_rejouer: Button = Button(
            "Rejouer", (250, 80), (largeur // 2, 550)
        )
        self.son_bouton: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.son_bouton.set_volume(0.25)
        self.next: bool = False

    def affiche_scene(self) -> None:
        """Affiche la scène de fin"""
        fenetre = pygame.display.get_surface()

        fenetre.blit(self.decors.image, self.decors.rect)
        fenetre.blit(self.masque, (0, 0))
        fenetre.blit(self.texte_score.image, self.texte_score.rect)
        fenetre.blit(self.texte_record.image, self.texte_record.rect)
        fenetre.blit(self.message_fin.image, self.message_fin.rect)
        fenetre.blit(self.bouton_rejouer.image, self.bouton_rejouer.rect)

    def joue_tour(self) -> None:
        """Rien"""
        self.bouton_rejouer.update()
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.bouton_rejouer.touch_mouse():
                self.son_bouton.play()
                self.next = True

    def passe_suivant(self) -> bool:
        """Vérifie si le bouton rejouer est cliqué"""
        return self.next
