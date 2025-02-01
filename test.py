import mediapipe as mp
import cv2
import numpy as np
import time
import pyautogui
import threading
import pygame
import random

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Global variables
x1, y1 = 0, 0
real_x1, real_y1 = 0, 0
stop_threads = False
toMove = False
score = 0
game_over = False

# Initialize video capture
video = cv2.VideoCapture(0)

# Pygame initialization
# pygame.init()
# screen = pygame.display.set_mode((800, 600))
# pygame.display.set_caption("Fruit Ninja")
# clock = pygame.time.Clock()

# Colors
RED = (255, 0, 0)  # Fruit color
BLACK = (0, 0, 0)  # Bomb color
WHITE = (255, 255, 255)  # Background color

# Fruit and Bomb class
class GameObject:
    def __init__(self, color, radius, speed):
        self.color = color
        self.radius = radius
        self.x = random.randint(radius, 800 - radius)
        self.y = 600 + radius  # Start below the screen
        self.speed = speed

    def update(self):
        self.y -= self.speed
        if self.y < -self.radius:  # Reset if off the screen
            self.y = 600 + self.radius
            self.x = random.randint(self.radius, 800 - self.radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Game function
def fruit_ninja_game():
    global score, game_over, stop_threads

    fruits = [GameObject(RED, 20, random.randint(3, 7)) for _ in range(5)]
    bomb = GameObject(BLACK, 20, 2)

    while not stop_threads:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_threads = True
                return

        screen.fill(WHITE)

        # Update and draw fruits
        for fruit in fruits:
            fruit.update()
            fruit.draw()

            # Check for collision with cursor
            if (fruit.x - x1 * 4) ** 2 + (fruit.y - y1 * 5) ** 2 <= fruit.radius ** 2:
                score += 1
                fruit.y = 600 + fruit.radius
                fruit.x = random.randint(fruit.radius, 800 - fruit.radius)

        # Update and draw bomb
        bomb.update()
        bomb.draw()

        # Check for collision with bomb
        if (bomb.x - x1 * 4) ** 2 + (bomb.y - y1 * 5) ** 2 <= bomb.radius ** 2:
            game_over = True
            stop_threads = True

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        # pygame.display.flip()
        clock.tick(30)

    pygame.quit()

# Hand tracking function
def hand_tracking():
    global x1, y1, real_x1, real_y1, stop_threads, toMove
    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while video.isOpened() and not stop_threads:
            ret, frame = video.read()
            if not ret:
                continue
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = cv2.flip(image, 1)
            image_height, image_width, _ = image.shape
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(258, 44, 250), thickness=2, circle_radius=2))
                    
                    for point in mp_hands.HandLandmark:
                        normalizedLandmark = hand_landmarks.landmark[point]
                        pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                            normalizedLandmark.x, normalizedLandmark.y, image_width, image_height)
                        
                        if pixelCoordinatesLandmark is None:
                            continue

                        if point == 8:  # Index finger tip
                            cv2.circle(image, (pixelCoordinatesLandmark[0], pixelCoordinatesLandmark[1]), 25, (0, 200, 0), 5)
                            real_x1, real_y1 = pixelCoordinatesLandmark[0], pixelCoordinatesLandmark[1]
                            x1 += (real_x1 - x1) * 0.5
                            y1 += (real_y1 - y1) * 0.5
                toMove = True
                print("Yes")
            else:
                toMove = False
                print("No")
            
            cv2.imshow('Hand Tracking', image)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                stop_threads = True
                break

    video.release()
    cv2.destroyAllWindows()

# Cursor movement function
def move_cursor():
    global x1, y1, stop_threads, toMove
    while not stop_threads:
        try:
            if(toMove):
                print("yhyhy")
                pyautogui.moveTo((int(x1 * 4), int(y1 * 5)))
        except Exception as e:
            print(e)

# Create threads
hand_tracking_thread = threading.Thread(target=hand_tracking)
cursor_movement_thread = threading.Thread(target=move_cursor)
# game_thread = threading.Thread(target=fruit_ninja_game)

# Start threads
hand_tracking_thread.start()
cursor_movement_thread.start()
# game_thread.start()

# Wait for threads to finish
hand_tracking_thread.join()
cursor_movement_thread.join()
# game_thread.join()

# Game over message
if game_over:
    print(f"Game Over! Your score is {score}")