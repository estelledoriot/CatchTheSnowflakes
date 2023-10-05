"""
classe Button
"""

import pygame


class Button(pygame.sprite.Sprite):
    """Bouton
    text: texte du bouton
    size: taille du bouton
    position: texte du bouton
    """

    def __init__(
        self, text: str, size: tuple[int, int], position: tuple[int, int]
    ) -> None:
        super().__init__()
        self.font: pygame.font.Font = pygame.font.Font("font/Avdira.otf", 50)
        self.text: str = text
        self.text_color: tuple[pygame.Color, pygame.Color] = (
            pygame.Color(240, 240, 240),
            pygame.Color(225, 238, 248),
        )
        self.background_color: tuple[pygame.Color, pygame.Color] = (
            pygame.Color(28, 42, 73),
            pygame.Color(28, 64, 100),
        )
        self.position: tuple[int, int] = position
        self.image: pygame.Surface = pygame.Surface(
            size, flags=pygame.SRCALPHA
        )
        self.image.fill(pygame.Color(0, 0, 0, 0))
        self.background: pygame.Rect = self.image.get_rect()
        self.rect: pygame.Rect = self.image.get_rect(center=position)

    def touch_mouse(self) -> bool:
        """Détermine si la souris touche le bouton"""
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self) -> None:
        """Mise à jour de l'affichage du bouton"""
        message = self.font.render(
            self.text, True, self.text_color[self.touch_mouse()]
        )
        message_rect = message.get_rect(
            center=(self.background.width // 2, self.background.height // 2)
        )
        pygame.draw.rect(
            self.image,
            self.background_color[self.touch_mouse()],
            self.background,
            border_radius=20,
        )
        self.image.blit(message, message_rect)
