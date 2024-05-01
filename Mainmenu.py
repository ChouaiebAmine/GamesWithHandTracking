import cv2
import numpy as np
import game1
import game2

def display_menu(img):
    cv2.putText(img, "Main Menu", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "1. Play Game 1", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "2. Play Game 2", (50, 220), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(img, "3. Quit", (50, 290), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    return img

def main():
    window_name = "Main Menu"
    img = np.zeros((400, 800, 3), dtype=np.uint8)
    img = display_menu(img)

    while True:
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1)

        if key == ord('1'):
            cv2.destroyWindow(window_name)
            game1.play_game1()
            img = display_menu(np.zeros((400, 800, 3), dtype=np.uint8))
        elif key == ord('2'):
            cv2.destroyWindow(window_name)
            game2.play_game2()
            img = display_menu(np.zeros((400, 800, 3), dtype=np.uint8))
        elif key == ord('3'):
            print("Exiting...")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
