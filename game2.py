import cv2 as cv
import numpy as np
import mediapipe as mp

def play_game2():


    width, height = 640, 480
    cap = cv.VideoCapture(1)
    cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    start = True
    score = 4
    squares = [
        {i: (np.random.randint(0, width), np.random.randint(0, height))}
        for i in range(1, score + 1)
    ]
    last_number = 0
    game_over = False
    round_started = False
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hand = mp_hands.Hands(min_detection_confidence=0.3, min_tracking_confidence=0.3)
    xcl1, ycl1, xcl2, ycl2 = 0, 0, 0, 0
    lml = []
    xl = []
    yl = []
    status = "closed"

    while start:
        if cv.waitKey(1) & 0xFF == ord("e"):
            start = False

        success, img = cap.read()
        img = cv.flip(img, 1)
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)

        if not game_over:
            res = hand.process(imgRGB)
            if res.multi_hand_landmarks:
                for hand_landmarks in res.multi_hand_landmarks:
                    if status == "open":
                        mp_drawing.draw_landmarks(
                            img, hand_landmarks, mp_hands.HAND_CONNECTIONS
                        )

            if res.multi_hand_landmarks != None:
                for lm in res.multi_hand_landmarks:
                    xcl1, ycl1 = hand_landmarks.landmark[7].x, hand_landmarks.landmark[7].y
                    xcl2, ycl2 = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                if ycl2 > ycl1:
                    status = "closed"
                else:
                    status = "open"

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

            if cv.waitKey(1) & 0xFF == ord("s") and not round_started:
                round_started = True

            for x in squares:
                for k, v in x.items():
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
                    else:
                        img = cv.rectangle(
                            img,
                            pt1=(v[0], v[1]),
                            pt2=(v[0] + 20, v[1] - 25),
                            color=(0, 0, 255),
                            thickness=-1,
                        )

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
                            and status == "open"
                        ):
                            if k != last_number + 1:
                                game_over = True
                                print(k, last_number)
                            else:
                                print("removed", x, "index was at", xcl2, ycl2)
                                squares.remove(x)
                                last_number += 1

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
        else:
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
                    text="but don't worry you're still smarter than them press Q to quit",
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
                if cv.waitKey(1) & 0xFF == ord('q'):
                    break
        cv.imshow("Game 2: Number Recognition", img)

    cap.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    play_game2()
