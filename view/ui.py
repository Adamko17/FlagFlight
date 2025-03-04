# view/ui.py
import pygame

class Ui:
    def __init__(self, screen, font, score_font):
        self.screen = screen
        self.font = font
        self.score_font = score_font

    def draw_plane(self, plane_x, plane_y, plane_width, plane_height):
        pygame.draw.rect(self.screen, (0, 0, 255), (plane_x, plane_y, plane_width, plane_height))  # כחול

    def draw_flag(self, flag_x, flag_y, flag_width, flag_height):
        pygame.draw.rect(self.screen, (255, 0, 0), (flag_x, flag_y, flag_width, flag_height))  # אדום

    def draw_score(self, score):
        score_text = self.score_font.render(f"Score: {score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))

    def draw_game_over(self):
        game_over_text = self.font.render("Game Over", True, (255, 255, 255))
        self.screen.blit(game_over_text, (300, 250))

    def update_display(self):
        pygame.display.update()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))  # רקע שחור
