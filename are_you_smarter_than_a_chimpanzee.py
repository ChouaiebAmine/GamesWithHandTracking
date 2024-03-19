# Import
import pygame
import cv2 as cv
import numpy as np
import mediapipe as mp

# Initialize
pygame.init()

# Create Window/Display
width, height = 640, 480
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Are You Smarter Than a Chimpanzee?")

cap = cv.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)  # height

# Initialize Clock for FPS
fps = 30
clock = pygame.time.Clock()

# Main loop
start = True

# Font
font = pygame.font.SysFont("Arial", 20)

# Score vars
score = 4

# Game vars
squares = [{i: ""} for i in range(1, score)]

# Hand detection
mp_hands = mp.solutions.hands
mp_drawing=mp.solutions.drawing_utils
hand = mp_hands.Hands()

while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
    
    # Exit keybind
    if cv.waitKey(1) == ord("e"):
        break

    # Apply Logic

    # OpenCV
    # Frame conversion to and rgb image
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    # Detecting hands
    res=hand.process(imgRGB)
    if res.multi_hand_landmarks:
        for hand_landmarks in res.multi_hand_landmarks:
            mp_drawing.draw_landmarks(imgRGB,hand_landmarks,mp_hands.HAND_CONNECTIONS)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, False, False)
    window.blit(frame, (0, 0))

    # Score
    textDisp = font.render("score : " + str(score), True, (0, 0, 0))
    window.blit(textDisp, (0, 0))

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
