import cv2
import numpy as np
import game1
import game2
import cvzone

def display_menu(img):
    # Display the main menu options
    cvzone.putTextRect(img, f"Measure Your Abilities With Brain Games", (200, 70), colorR=(139, 61, 72), scale=2)
    cvzone.putTextRect(img, f'Games: ', (40, 200), colorR=(139, 61, 72), scale=3)
    cvzone.putTextRect(img, f'1-Reaction Time', (40, 270), colorR=(32, 165, 218), scale=2)
    cvzone.putTextRect(img, f'2-Chimp Test', (40, 340), colorR=(32, 165, 218), scale=2)
    cvzone.putTextRect(img, f'\'3\' to Quit ', (40, 410), colorR=(0, 0, 128), scale=2)
    return img

def main():
    window_name = "Main Menu"
    img = np.zeros((720,1280 , 3), dtype=np.uint8)
    img = display_menu(img)

    while True:
        cv2.imshow(window_name, img)
        key = cv2.waitKey(1)

        if key == ord('1'):
            cv2.destroyWindow(window_name)
            game1.play_game1()  # Call the play_game1() function from game1.py
            img = display_menu(np.zeros((720,1280 , 3), dtype=np.uint8))
        elif key == ord('2'):
            cv2.destroyWindow(window_name)
            game2.play_game2()  # Call the play_game2() function from game2.py
            img = display_menu(np.zeros((720,1280 , 3), dtype=np.uint8))
        elif key == ord('3'):
            print("Exiting...")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
