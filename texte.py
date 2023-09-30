"""
classe Texte
"""

import pygame


class Texte:
    """Message
    texte: texte à afficher
    nom_police: nom du fichier de police pour afficher le message
    taille: taille du texte
    """

    def __init__(self, texte: str, nom_police: str, taille: int) -> None:
        self.police: pygame.font.Font = pygame.font.Font(nom_police, taille)
        self.texte: str = texte
        self.surface: pygame.Surface = pygame.Surface((0, 0))
        self.rect: pygame.Rect = self.surface.get_rect()

    def genere_surface(
        self, couleur: pygame.Color, centerx: int, centery: int
    ):
        """Génère le message"""
        self.surface = self.police.render(self.texte, True, couleur)
        self.rect = self.surface.get_rect(center=(centerx, centery))

    def draw(
        self,
        couleur: pygame.Color,
        centerx: int,
        centery: int,
    ) -> None:
        """Affiche le message sur la fenêtre"""
        fenetre = pygame.display.get_surface()
        self.genere_surface(couleur, centerx, centery)
        fenetre.blit(self.surface, self.rect)
