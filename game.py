import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Ninja")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game variables
score = 0
game_over = False
cursor_radius = 20
fruit_radius = 30
bomb_radius = 30

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont("Arial", 36)

# Function to draw text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function to create a new fruit or bomb
def create_object():
    x = random.randint(fruit_radius, WIDTH - fruit_radius)
    y = HEIGHT
    obj_type = random.choice(["fruit", "bomb"])
    return {"x": x, "y": y, "type": obj_type}

# List to hold fruits and bombs
objects = []

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Draw cursor
        pygame.draw.circle(screen, BLACK, (mouse_x, mouse_y), cursor_radius)

        # Spawn new objects
        if random.random() < 0.02:
            objects.append(create_object())

        # Move and draw objects
        for obj in objects:
            obj["y"] -= 5  # Move object upwards
            if obj["type"] == "fruit":
                pygame.draw.circle(screen, GREEN, (int(obj["x"]), int(obj["y"])), fruit_radius)
            else:
                pygame.draw.circle(screen, RED, (int(obj["x"]), int(obj["y"])), bomb_radius)

            # Check for collision with cursor
            distance = ((mouse_x - obj["x"]) ** 2 + (mouse_y - obj["y"]) ** 2) ** 0.5
            if distance < cursor_radius + (fruit_radius if obj["type"] == "fruit" else bomb_radius):
                if obj["type"] == "fruit":
                    score += 1
                else:
                    game_over = True
                objects.remove(obj)

        # Remove objects that go off-screen
        objects = [obj for obj in objects if obj["y"] > -fruit_radius]

        # Draw score
        draw_text(f"Score: {score}", font, BLACK, 10, 10)

    else:
        # Game over screen
        draw_text("Game Over!", font, RED, WIDTH // 2 - 100, HEIGHT // 2 - 50)
        draw_text(f"Final Score: {score}", font, BLACK, WIDTH // 2 - 120, HEIGHT // 2)

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Quit pygame
pygame.quit()
sys.exit()