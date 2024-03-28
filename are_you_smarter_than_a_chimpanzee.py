# Import
import cv2 as cv
import numpy as np
import mediapipe as mp

# Create Window/Display
width, height = 640, 480

cap = cv.VideoCapture(0)
cap.set(4, 640)  # width
cap.set(3, 480)  # height

# Main loop
start = True

# Score vars
score = 4

# Game vars
squares = [
    {i: (np.random.randint(0, width), np.random.randint(0, height))}
    for i in range(1, score + 1)
]
last_number = 0
game_over = False
round_started = False
# Hand detection
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hand = mp_hands.Hands(min_detection_confidence=0.3, min_tracking_confidence=0.3)
xcl1, ycl1, xcl2, ycl2 = 0, 0, 0, 0

# Hand coordinates list
lml = []
xl = []
yl = []
status = "closed"
while start:

    # Exit keybind
    if cv.waitKey(1) & 0xFF == ord("e"):
        start = False

    # Frame conversion to and rgb image
    success, img = cap.read()
    img = cv.flip(img, 1)
    imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    if not game_over:
        # Detecting hands and drawing landmarks
        res = hand.process(imgRGB)
        if res.multi_hand_landmarks:
            for hand_landmarks in res.multi_hand_landmarks:
                if status == "open":
                    mp_drawing.draw_landmarks(
                        img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

        # Hand coordination stuff
        if res.multi_hand_landmarks != None:
            # Seeing if the hand is closed or open by checking if the tip (point 8) of the index finger
            # is below the dip (point 7) of the index finger
            for lm in res.multi_hand_landmarks:
                xcl1, ycl1 = hand_landmarks.landmark[7].x, hand_landmarks.landmark[7].y
                xcl2, ycl2 = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
            if ycl2 > ycl1:
                status = "closed"
            else:
                status = "open"

            # Scaling index finger coordinates to pixels
            xcl2, ycl2 = xcl2 * width, ycl2 * height
        if not round_started:
            img = cv.putText(
                img,
                org=(200, 20),
                text="Press 's' to hide the numbers and start",
                color=(255, 0, 0),
                thickness=2,
                fontScale=0.7,
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
            )
        # Start round with 's'
        if cv.waitKey(1) & 0xFF == ord("s") and not round_started:
            round_started = True
        # Display numbers
        # Looping through numbers
        for x in squares:
            for k, v in x.items():
                # Displaying the number on screen
                if not round_started:
                    img = cv.putText(
                        img,
                        text=str(k),
                        org=(v[0], v[1]),
                        color=(0, 0, 255),
                        thickness=2,
                        fontScale=0.7,
                        fontFace=cv.FONT_HERSHEY_SIMPLEX,
                    )
                if round_started:
                    img = cv.rectangle(
                        img,
                        pt1=(v[0], v[1]),
                        pt2=(v[0] + 20, v[1] - 25),
                        color=(0, 0, 255),
                        thickness=-1,
                    )
                    # Checking if the finger is inside the numbers' hitboxes
                    if (
                        cv.pointPolygonTest(
                            np.array(
                                [
                                    [v[0], v[1]],
                                    [v[0], v[1] - 25],
                                    [v[0] + 25, v[1] - 25],
                                    [v[0] + 25, v[1]],
                                ],
                                dtype=np.int32,
                            ),
                            (xcl2, ycl2),
                            False,
                        )
                        == 1
                    ) and status == "open":

                        # If the finger is inside and the number is equal to last_number + 1 we remove the number from the list
                        if k != last_number + 1:
                            game_over = True
                            print(k, last_number)
                        else:
                            print("removed", x, "index was at", xcl2, ycl2)
                            squares.remove(x)
                            last_number += 1

        # If you won ( the list becomes empty) we add 1 to score and repeat
        if not squares:
            img = cv.putText(
                img,
                org=(0, 240),
                text="Press 'n' to start the next round",
                color=(255, 0, 0),
                thickness=2,
                fontScale=0.7,
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
            )
            if cv.waitKey(1) & 0xFF == ord("n"):
                score += 1
                last_number = 0
                squares = [
                    {i: (np.random.randint(0, width), np.random.randint(0, height))}
                    for i in range(1, score + 1)
                ]
                round_started = False
        # Showing score and index finger coordinates
        img = cv.putText(
            img,
            org=(0, 20),
            text="score : " + str(score) + " " + status,
            color=(255, 0, 0),
            thickness=2,
            fontScale=0.7,
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
        )
        img = cv.putText(
            img,
            org=(0, 40),
            text="x : " + format(xcl2, ".0f") + " y : " + format(ycl2, ".0f"),
            color=(255, 0, 0),
            thickness=2,
            fontScale=0.7,
            fontFace=cv.FONT_HERSHEY_SIMPLEX,
        )
    # ---------game-over-stuff---------------------------------
    if game_over:
        if score > 9:
            img = cv.putText(
                img,
                org=(0, 240),
                text="You are smarter than a chimpanzee ,your score is "
                + str(score)
                + " :)",
                color=(0, 255, 0),
                thickness=2,
                fontScale=0.7,
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
            )
        else:
            img = cv.putText(
                img,
                org=(0, 240),
                text="Chimpanzees score up to 9",
                color=(255, 0, 0),
                thickness=2,
                fontScale=0.7,
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
            )
            img = cv.putText(
                img,
                org=(0, 260),
                text="but don't worry you're still smarter than them",
                color=(255, 0, 0),
                thickness=2,
                fontScale=0.7,
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
            )
            img = cv.putText(
                img,
                org=(0, 280),
                text="your score is " + str(score) + " :)",
                color=(255, 0, 0),
                thickness=2,
                fontScale=0.7,
                fontFace=cv.FONT_HERSHEY_SIMPLEX,
            )
    # Drawing the processed frame on screen
    cv.imshow("Are you smarter than a chimpanzee ?", img)
cap.release()
cv.destroyAllWindows()
