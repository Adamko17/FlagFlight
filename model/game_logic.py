# model/game_logic.py
import random
import time

class GameLogic:
    def __init__(self):
        self.plane_x = 100
        self.plane_y = 300  # מיקום התחלתי של המטוס
        self.plane_width = 50
        self.plane_height = 50
        self.plane_speed = 5
        self.flag_width = 50
        self.flag_height = 50
        self.flag_speed = 5
        self.flag_x = 800  # מיקום התחלתי של הדגל
        self.flag_y = random.randint(0, 550)
        self.score = 0
        self.start_time = time.time()
        self.game_over = False


    def move_flag(self):
        self.flag_x -= self.flag_speed
        if self.flag_x < 0:
            self.flag_x = 800
            self.flag_y = random.randint(0, 550)

    def check_collision(self):
        if (self.plane_x + self.plane_width > self.flag_x and self.plane_x < self.flag_x + self.flag_width) and \
           (self.plane_y + self.plane_height > self.flag_y and self.plane_y < self.flag_y + self.flag_height):
            return True
        return False

    def move_plane(self, direction):
        if direction == "up" and self.plane_y > 0:
            self.plane_y -= self.plane_speed
        elif direction == "down" and self.plane_y < 600 - self.plane_height:
            self.plane_y += self.plane_speed


    def update_score(self):
        """עדכון הניקוד לפי הזמן שחלף"""
        elapsed_time = time.time() - self.start_time
        self.score = int(elapsed_time // 60)  # כל דקה משחק מוסיפה ניקוד שלם

    def get_game_state(self):
        return self.game_over, self.score
