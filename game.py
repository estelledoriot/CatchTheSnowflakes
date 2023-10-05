"""
Gestion des scènes du jeu
"""

from enum import Enum

import pygame

from background import Background
from bear import Bear
from button import Button
from countdown import Countdown
from filled_surface import FilledSurface
from lives import Lives
from object import Object
from score import Score
from text import Text

Stage = Enum("Stage", ["RUNNING", "END", "TERMINATE"])


class Game:
    """Une partie de hunt the bears"""

    def __init__(self, width: int, height: int) -> None:
        # décors
        self.background: Background = Background(
            "images/mountain.png", (width // 2, height // 2), width
        )
        self.opaque_surface: FilledSurface = FilledSurface(
            pygame.Color(230, 230, 230, 150)
        )

        # game elements
        self.bear: Bear = Bear((width // 2, height - 50), 150, 10)
        self.snowflakes: pygame.sprite.Group = pygame.sprite.Group()
        self.lightnings: pygame.sprite.Group = pygame.sprite.Group()
        self.countdown: Countdown = Countdown(60, (width - 80, 60))
        self.score: Score = Score((width // 2, 60))
        self.lives: Lives = Lives(3, (80, 45))
        self.game_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.game_elements.add(
            self.background,
            self.countdown,
            self.lives,
            self.score,
            self.bear,
            self.snowflakes,
            self.lightnings,
        )
        self.game_elements_to_draw: pygame.sprite.Group = pygame.sprite.Group()
        self.game_elements_to_draw.add(
            self.background,
            self.countdown,
            self.lives,
            self.score,
            self.snowflakes,
            self.lightnings,
        )

        # end elements
        self.record: int = 0
        with open("record.txt", "r", encoding="utf-8") as fichier:
            self.record = int(fichier.read())
        self.score_surface: Text = Text(
            f"Score : {self.score.score}",
            50,
            pygame.Color(28, 42, 73),
            (width // 2, 100),
        )
        self.record_surface: Text = Text(
            f"Record : {self.record}",
            50,
            pygame.Color(28, 42, 73),
            (width // 2, 170),
        )
        self.end_message: Text = Text(
            "", 100, pygame.Color(255, 255, 255), (width // 2, 350)
        )
        self.restart_button: Button = Button(
            "Rejouer", (250, 80), (width // 2, 550)
        )
        self.end_elements: pygame.sprite.Group = pygame.sprite.Group()
        self.end_elements.add(
            self.background,
            self.opaque_surface,
            self.score_surface,
            self.record_surface,
            self.end_message,
            self.restart_button,
        )

        # events
        self.new_snowflake_event: int = pygame.USEREVENT + 1
        pygame.time.set_timer(self.new_snowflake_event, 600)
        self.new_lightning_event: int = pygame.USEREVENT + 2
        pygame.time.set_timer(self.new_lightning_event, 1000)

        # sons
        self.ok_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/coin.wav"
        )
        self.ok_sound.set_volume(0.15)
        self.ko_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/laser.wav"
        )
        self.ko_sound.set_volume(0.25)
        self.end_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/end.wav"
        )
        self.end_sound.set_volume(0.25)
        self.button_sound: pygame.mixer.Sound = pygame.mixer.Sound(
            "sounds/pop.wav"
        )
        self.button_sound.set_volume(0.25)

        # stage
        self.stage: Stage = Stage.RUNNING

    @property
    def won(self) -> bool:
        """Vérifie si la partie est gagnée"""
        return (
            self.countdown.time_finished or self.lives.is_dead
        ) and self.score.score > self.record

    @property
    def lost(self) -> bool:
        """Vérifie si la partie est perdue"""
        return (
            self.countdown.time_finished or self.lives.is_dead
        ) and self.score.score <= self.record

    def run_game(self) -> None:
        """Fait tourner le jeu"""
        # générer les nouveaux objets
        for _ in pygame.event.get(self.new_snowflake_event):
            self.snowflakes.add(Object("images/snowflake.png", 50, 8))

        for _ in pygame.event.get(self.new_lightning_event):
            self.lightnings.add(Object("images/lightning.png", 25, 15))

        # collisions
        if pygame.sprite.spritecollide(self.bear, self.snowflakes, True):
            self.score.add_points(1)
            self.ok_sound.play()
        if pygame.sprite.spritecollide(self.bear, self.lightnings, True):
            self.lives.lose(1)
            self.ko_sound.play()
            self.bear.start_flashing()

        # mise à jour des éléments
        self.game_elements.remove(self.snowflakes, self.lightnings)
        self.game_elements.add(self.snowflakes, self.lightnings)
        self.game_elements.update()
        self.game_elements_to_draw.remove(self.snowflakes, self.lightnings)
        self.game_elements_to_draw.add(self.snowflakes, self.lightnings)

        # fin du jeu
        if self.won:
            self.record = self.score.score
            with open("record.txt", "w", encoding="utf-8") as fichier:
                fichier.write(str(self.record))
        if self.won or self.lost:
            self.stage = Stage.END
            self.end_sound.play()
            self.end_message.update_text(
                "Nouveau record" if self.won else "Perdu ..."
            )
            self.score_surface.update_text(f"score: {self.score.score}")
            self.record_surface.update_text(f"record: {self.record}")

    def draw_game(self, screen: pygame.Surface) -> None:
        """Affiche les éléments du jeu"""
        self.game_elements_to_draw.draw(screen)
        if self.bear.is_visible:
            screen.blit(self.bear.image, self.bear.rect)

    def run_end(self) -> None:
        """Fait tourner l'écran de fin"""
        # mise à jour des éléments de l'écran de fin
        self.end_elements.update()

        # clic sur le bouton pour commencer une nouvelle partie
        for _ in pygame.event.get(pygame.MOUSEBUTTONDOWN):
            if self.restart_button.touch_mouse():
                self.button_sound.play()
                self.stage = Stage.TERMINATE

    def draw_end(self, screen: pygame.Surface) -> None:
        """Affiche les éléments de l'écran de fin"""
        self.end_elements.draw(screen)
