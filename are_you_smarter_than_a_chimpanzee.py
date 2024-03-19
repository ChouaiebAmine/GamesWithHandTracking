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
squares = [
    {i: (np.random.randint(0, width), np.random.randint(0, height))}
    for i in range(1, score + 1)
]
print(squares)
# Hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Hand coordinates list
lml = []
xl = []
yl = []

while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Exit keybind
    if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
        start = False

    # Apply Logic

    # Frame conversion to and rgb image
    success, img = cap.read()
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    imgRGB = np.ascontiguousarray(imgRGB)

    # Detecting hands and drawing landmarks
    res = hand.process(imgRGB)
    if res.multi_hand_landmarks:
        for hand_landmarks in res.multi_hand_landmarks:
            mp_drawing.draw_landmarks(imgRGB, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Drawing the processed frame on screen
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    frame = pygame.transform.flip(frame, False, False)
    window.blit(frame, (0, 0))

    # Hand coordination stuff
    if res.multi_hand_landmarks != None:
        # Seeing if the hand is closed or open by checking if the top point of the middle finger
        # is below the lowest point of the middle finger
        for lm in res.multi_hand_landmarks:
            xcl1, ycl1 = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
            xcl2, ycl2 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y
        if ycl2 > ycl1:
            status = "closed"
        else:
            status = "open"
        # Printing the hand's coodrinates
        for id, lm in enumerate(res.multi_hand_landmarks[0].landmark):
            h, w, _ = img.shape
            xc, yc = int(lm.y * h), int(lm.x * w)
            lml.append([id, xc, yc])
            # xl.append(xc)
            # yl.append(yc)
        print(lml[::-1][0][1], lml[::-1][0][2],status, " ", squares)

    # Display number squares
    for x in squares:
        for k, v in x.items():
            pygame.draw.rect(
                surface=window,
                color="white",
                rect=pygame.Rect(v[0], v[1], 20, 20),
                border_radius=2,
            )
            squareText = font.render(str(k), True, (0, 0, 255))
            window.blit(squareText, v)

    # Score
    scoreText = font.render("score : " + str(score), True, (0, 0, 255))
    window.blit(scoreText, (0, 0))

    # Update Display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)
