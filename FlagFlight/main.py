import pygame
import random
import os

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Model - Game data representation
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.width = 50
        self.height = 50
        self.speed = 5
        self.lives = 3
        self.score = 0
        self.last_score_update = pygame.time.get_ticks()

    def move(self, keys):
        # Fixed movement with arrow keys
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < HEIGHT - self.height:
            self.y += self.speed

    def update_score(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_score_update >= 1000:
            self.score += 1
            self.last_score_update = current_time


class FlagData:
    def __init__(self):
        # Database of questions and answers about flags in English
        self.flag_database = [
            {
                "country": "Israel",
                "question": "What are the colors of the Israeli flag?",
                "options": ["Blue and White", "Red and White", "Green and Yellow", "Black and Red"],
                "answer": 0
            },
            {
                "country": "France",
                "question": "What is the capital of France?",
                "options": ["Berlin", "Madrid", "Paris", "Rome"],
                "answer": 2
            },
            {
                "country": "USA",
                "question": "How many states are there in the USA?",
                "options": ["48", "50", "52", "45"],
                "answer": 1
            },
            {
                "country": "Japan",
                "question": "What does the red circle on Japan's flag represent?",
                "options": ["Mount Fuji", "The Sun", "The Moon", "Cherry Blossom"],
                "answer": 1
            },
            {
                "country": "Brazil",
                "question": "What color is the central circle on Brazil's flag?",
                "options": ["Red", "Green", "Blue", "Yellow"],
                "answer": 2
            },
            {
                "country": "UK",
                "question": "What is the name of the UK flag?",
                "options": ["Union Jack", "Royal Flag", "British Banner", "Kingdom Cross"],
                "answer": 0
            },
            {
                "country": "Canada",
                "question": "Which leaf appears on Canada's flag?",
                "options": ["Oak Leaf", "Maple Leaf", "Eucalyptus Leaf", "Palm Leaf"],
                "answer": 1
            },
            {
                "country": "Germany",
                "question": "What are the colors of the German flag?",
                "options": ["Black, Red, Yellow", "Black, Red, Blue", "White, Red, Black", "Green, Yellow, Red"],
                "answer": 0
            }
        ]

    def get_random_flag_data(self):
        return random.choice(self.flag_database)


class Flag:
    def __init__(self, flag_data):
        self.x = WIDTH + random.randint(50, 200)  # Starts slightly off-screen
        self.y = random.randint(50, HEIGHT - 100)
        self.width = 60
        self.height = 40
        self.speed = random.randint(2, 5)
        self.flag_data = flag_data
        self.country = flag_data["country"]
        self.question = flag_data["question"]
        self.options = flag_data["options"]
        self.answer = flag_data["answer"]

    def move(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x < -self.width

    def collides_with(self, player):
        return (player.x < self.x + self.width and
                player.x + player.width > self.x and
                player.y < self.y + self.height and
                player.y + player.height > self.y)


# View - Game display
class GameView:
    def __init__(self, screen):
        self.screen = screen
        self.large_font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 28)
        self.colors = {
            "Israel": (0, 0, 128),
            "France": (0, 0, 255),
            "USA": (255, 0, 0),
            "Japan": (255, 0, 0),
            "Brazil": (0, 156, 59),
            "UK": (0, 36, 125),
            "Canada": (255, 0, 0),
            "Germany": (0, 0, 0)
        }
        try:
            # Replace "background.jpg" with the path to your image
            self.background_image = pygame.image.load("BG.png").convert()
            # Scale the image to fit the screen
            self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        except pygame.error as e:
            print(f"Could not load background image: {e}")
            self.background_image = None

    def draw_heart(self, x, y, width, height):
        # Draw a heart shape
        heart_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Heart shape drawn with a polygon
        heart_points = [
            (width//2, height//5),
            (width//4, 0),
            (0, height//5),
            (0, height//2),
            (width//2, height),
            (width, height//2),
            (width, height//5),
            (3*width//4, 0),
            (width//2, height//5)
        ]
        pygame.draw.polygon(heart_surface, RED, heart_points)

        self.screen.blit(heart_surface, (x, y))

    def draw_game(self, player, flags, game_state):
        # Draw background image instead of filling with white
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(WHITE)

        # Draw player
        pygame.draw.rect(self.screen, BLUE, (player.x, player.y, player.width, player.height))

        # Draw flags
        for flag in flags:
            color = self.colors.get(flag.country, RED)
            pygame.draw.rect(self.screen, color, (flag.x, flag.y, flag.width, flag.height))
            text = self.small_font.render(flag.country, True, WHITE)
            text_rect = text.get_rect(center=(flag.x + flag.width/2, flag.y + flag.height/2))
            self.screen.blit(text, text_rect)

        # Draw score
        score_text = self.medium_font.render(f"Score: {player.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        # Draw hearts for lives
        heart_width, heart_height = 25, 25
        hearts_start_x = 160
        for i in range(player.lives):
            self.draw_heart(hearts_start_x + i * (heart_width + 5), 10, heart_width, heart_height)

        pygame.display.flip()

    def draw_question(self, flag):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(WHITE)

        # Question title
        title = self.large_font.render(f"Flag: {flag.country}", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH/2, 80))
        self.screen.blit(title, title_rect)

        # Question itself
        question = self.medium_font.render(flag.question, True, BLACK)
        question_rect = question.get_rect(center=(WIDTH/2, 150))
        self.screen.blit(question, question_rect)

        # Answer options with enhanced styling
        option_rects = []
        for i, option in enumerate(flag.options):
            # Button colors
            base_color = (70, 130, 180)  # Steel blue
            hover_color = (100, 149, 237)  # Cornflower blue
            border_color = (40, 70, 120)  # Darker blue for border
            text_color = WHITE

            # Get mouse position to check for hover effect
            mouse_pos = pygame.mouse.get_pos()

            # Create button rectangle
            button_rect = pygame.Rect(WIDTH/2 - 180, 220 + i*85, 360, 65)

            # Draw shadow first (offset rectangle)
            shadow_rect = button_rect.copy()
            shadow_rect.x += 4
            shadow_rect.y += 4
            pygame.draw.rect(self.screen, (50, 50, 50), shadow_rect, border_radius=15)

            # Draw main button
            if button_rect.collidepoint(mouse_pos):
                # Apply hover color
                pygame.draw.rect(self.screen, hover_color, button_rect, border_radius=15)
            else:
                # Apply normal color
                pygame.draw.rect(self.screen, base_color, button_rect, border_radius=15)

            # Draw button border
            pygame.draw.rect(self.screen, border_color, button_rect, 2, border_radius=15)

            # Draw a highlight at the top of the button
            highlight_rect = pygame.Rect(button_rect.x + 5, button_rect.y + 5, button_rect.width - 10, 10)
            pygame.draw.rect(self.screen, (120, 180, 230), highlight_rect, border_radius=10)

            # Option text with number
            option_text = self.medium_font.render(f"{i+1}. {option}", True, text_color)
            option_rect = option_text.get_rect(center=button_rect.center)
            self.screen.blit(option_text, option_rect)

            option_rects.append(button_rect)

        pygame.display.flip()

        return option_rects

    def draw_feedback(self, is_correct):
        feedback_text = "Correct Answer!" if is_correct else "Wrong Answer!"
        color = GREEN if is_correct else RED

        feedback = self.large_font.render(feedback_text, True, color)
        feedback_rect = feedback.get_rect(center=(WIDTH/2, HEIGHT/2))

        # Semi-transparent background
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 200))
        self.screen.blit(overlay, (0, 0))

        self.screen.blit(feedback, feedback_rect)
        pygame.display.flip()

        # Short delay to show feedback
        pygame.time.delay(1500)

    def draw_game_over(self, score):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(WHITE)

        game_over = self.large_font.render("Game Over", True, RED)
        game_over_rect = game_over.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))
        self.screen.blit(game_over, game_over_rect)

        score_text = self.medium_font.render(f"Your final score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 20))
        self.screen.blit(score_text, score_rect)

        restart_text = self.medium_font.render("Press SPACE to restart", True, BLUE)
        restart_rect = restart_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 80))
        self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def draw_start_screen(self):
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(WHITE)

        title = self.large_font.render("Flag Flight - אדם & Gaya", True, BLUE)
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/2 - 80))
        self.screen.blit(title, title_rect)

        instructions = self.medium_font.render("Move around the flags!", True, BLACK)
        instructions_rect = instructions.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.screen.blit(instructions, instructions_rect)

        start_text = self.medium_font.render("Press SPACE to start the game", True, GREEN)
        start_rect = start_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 80))
        self.screen.blit(start_text, start_rect)

        controls = self.small_font.render("Controls: Arrow keys to move", True, BLACK)
        controls_rect = controls.get_rect(center=(WIDTH/2, HEIGHT/2 + 140))
        self.screen.blit(controls, controls_rect)

        pygame.display.flip()


# Controller - Game management
class GameController:
    def __init__(self, screen):
        self.screen = screen
        self.view = GameView(screen)
        self.flag_data = FlagData()
        self.reset_game()
        self.state = "START"  # Possible states: START, PLAYING, QUESTION, GAME_OVER
        self.clock = pygame.time.Clock()

    def reset_game(self):
        self.player = Player()
        self.flags = []
        self.current_flag = None
        self.running = True

    def spawn_flag(self):
        if random.randint(1, 100) > 97:  # 3% chance to spawn a flag each frame
            flag_data = self.flag_data.get_random_flag_data()
            self.flags.append(Flag(flag_data))

    def update_playing(self, keys):
        self.player.move(keys)
        self.player.update_score()

        # Update flag positions and remove flags that are off-screen
        for flag in self.flags:
            flag.move()
        self.flags = [flag for flag in self.flags if not flag.is_off_screen()]

        # Check for collisions
        collided_flag = None
        for flag in self.flags[:]:  # Copy list so we can remove while iterating
            if flag.collides_with(self.player):
                collided_flag = flag
                self.flags.remove(flag)
                break

        if collided_flag:
            self.current_flag = collided_flag
            self.state = "QUESTION"

    def handle_question(self, event):
        option_rects = self.view.draw_question(self.current_flag)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(option_rects):
                if rect.collidepoint(event.pos):
                    is_correct = (i == self.current_flag.answer)
                    self.view.draw_feedback(is_correct)

                    if not is_correct:
                        self.player.lives -= 1

                    if self.player.lives <= 0:
                        self.state = "GAME_OVER"
                    else:
                        self.state = "PLAYING"

                    return True  # Indicate we handled the event

        return False  # Event not handled

    def handle_game_over(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.reset_game()
            self.state = "PLAYING"
            return True
        return False

    def handle_start_screen(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.state = "PLAYING"
            return True
        return False

    def run(self):
        while self.running:
            # Get key presses
            keys = pygame.key.get_pressed()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return

                # Handle events based on game state
                if self.state == "QUESTION":
                    if self.handle_question(event):
                        continue
                elif self.state == "GAME_OVER":
                    if self.handle_game_over(event):
                        continue
                elif self.state == "START":
                    if self.handle_start_screen(event):
                        continue

            # Update game based on state
            if self.state == "PLAYING":
                self.spawn_flag()
                self.update_playing(keys)
                self.view.draw_game(self.player, self.flags, self.state)
            elif self.state == "QUESTION":
                self.view.draw_question(self.current_flag)
            elif self.state == "GAME_OVER":
                self.view.draw_game_over(self.player.score)
            elif self.state == "START":
                self.view.draw_start_screen()

            # Control game speed
            self.clock.tick(60)


# Main - Game execution
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flag Meteor Game")

    controller = GameController(screen)
    controller.run()

    pygame.quit()

if __name__ == "__main__":
    main()