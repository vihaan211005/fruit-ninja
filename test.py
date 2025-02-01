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
            else:
                toMove = False
            
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
                pyautogui.moveTo((int(x1 * 4), int(y1 * 5)))
        except Exception as e:
            print(e)

# Create threads
hand_tracking_thread = threading.Thread(target=hand_tracking)
cursor_movement_thread = threading.Thread(target=move_cursor)

# Start threads
hand_tracking_thread.start()
cursor_movement_thread.start()

# Wait for threads to finish
hand_tracking_thread.join()
cursor_movement_thread.join()