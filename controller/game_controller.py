import pygame
from model.game_logic import GameLogic
from view.ui import Ui


class GameController:
    def __init__(self):
        self.game_logic = GameLogic()

        # יצירת אובייקטים של screen ו-font
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont("Arial", 36)
        self.score_font = pygame.font.SysFont("Arial", 24)

        # יצירת אובייקט של Ui ומעבר את המשתנים הנדרשים
        self.game_ui = Ui(self.screen, self.font, self.score_font)

    def start_game(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            keys = pygame.key.get_pressed()  # מחזיר את כל המפתחות הלחוצים
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # תנועה מבוססת על מקשי WASD
            if keys[pygame.K_w]:  # למעלה
                self.game_logic.move_plane("up")
            if keys[pygame.K_s]:  # למטה
                self.game_logic.move_plane("down")
            if keys[pygame.K_a]:  # שמאלה
                self.game_logic.move_plane("left")
            if keys[pygame.K_d]:  # ימינה
                self.game_logic.move_plane("right")

            self.game_logic.move_flag()
            self.game_logic.update_score()

            self.screen.fill((255, 255, 255))  # מנקה את המסך
            self.game_ui.draw_plane(self.game_logic.plane_x, self.game_logic.plane_y,
                                    self.game_logic.plane_width, self.game_logic.plane_height)
            self.game_ui.draw_flag(self.game_logic.flag_x, self.game_logic.flag_y,
                                   self.game_logic.flag_width, self.game_logic.flag_height)
            self.game_ui.draw_score(self.game_logic.score)

            if self.game_logic.check_collision():
                print("Game Over! Score:", self.game_logic.score)
                running = False

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
