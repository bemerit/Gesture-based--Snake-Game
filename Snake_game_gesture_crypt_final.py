#Author: EMERIT BEEMUL 
# Gesture based cryptography in video games

import pygame as pg
from random import randrange
import pickle
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
# Compare gestures
def compareGestures(gesture1, gesture2):
    # Compare the finger states for each finger
    for finger1, finger2 in zip(gesture1, gesture2):
        if finger1 != finger2:
            return False
    return True

# Start gesture check

#function to input gesture
detector = HandDetector(detectionCon=0.8)

def input_gesture():

    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Record the first gesture
    #input("Press Enter to start recording the Gesture to load your save file")

    gesture_data1 = []
    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        success, img = cap.read()

        if success:
            hands, img = detector.findHands(img)

            if hands:
                lmList = hands[0]['lmList']
                fingers = detector.fingersUp(hands[0])
                gesture_data1.append(fingers)

            cv2.imshow("Image", img)

            if elapsed_time >= 5:
                break

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Close the video
    cap.release()
    cv2.destroyAllWindows()
    return gesture_data1


def gestureCheck():

    # Prompt user to start recording the second gesture
    #input("Press Enter to verify your identity with the Gesture used.")

    # Reinitialize the video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    # Record the second gesture
    gesture_data2 = []
    start_time_gc = pg.time.get_ticks() / 1000.0 #using this as time is being considered as int

    while True:
        current_time_gc = pg.time.get_ticks() / 1000.0
        elapsed_time = current_time_gc - start_time_gc

        success, img = cap.read()

        if success:
            hands, img = detector.findHands(img)

            if hands:
                lmList = hands[0]['lmList']
                fingers = detector.fingersUp(hands[0])
                gesture_data2.append(fingers)

            cv2.imshow("Image", img)

            if elapsed_time >= 5:
                break

        if cv2.waitKey(1) & 0xFF == 27:
            break
    # Close the video again
    cap.release()
    cv2.destroyAllWindows()

    return gesture_data2


def compare_Input(gesture_data1, gesture_data2):
    # Compare the two recorded gestures
    gesture_match = compareGestures(gesture_data1, gesture_data2)

    # Print the result
    if gesture_match:
        print("Gestures match!")
        return True
    else:
        print("Gestures do not match.")
        return False

WINDOW = 700
TILE_SIZE = 50
RANGE = (TILE_SIZE // 2, WINDOW - TILE_SIZE // 2, TILE_SIZE)
get_random_position = lambda: [randrange(*RANGE), randrange(*RANGE)]

# Initialize Pygame
pg.init()

# Create the screen
screen = pg.display.set_mode([WINDOW] * 2)
pg.display.set_caption("Hans Snake Game")
clock = pg.time.Clock()

# Function to display the main menu
def main_menu():
    font = pg.font.Font(None, 36)
    text_player1 = font.render("1. Player 1", True, "white")
    text_player2 = font.render("2. Player 2", True, "white")

    screen.fill("black")
    screen.blit(text_player1, (WINDOW // 2 - text_player1.get_width() // 2, WINDOW // 2 - 50))
    screen.blit(text_player2, (WINDOW // 2 - text_player2.get_width() // 2, WINDOW // 2 + 50))

    pg.display.flip()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_1:

                    screen.fill("black")
                    small_font = pg.font.Font(None, 24)
                    text_message = small_font.render("Please hold your Identification Gesture for 4 seconds. Thank you", True, "white")
                    screen.blit(text_message, (WINDOW // 2 - text_message.get_width() // 2, WINDOW // 2))
                    pg.display.flip()
                    pg.time.wait(2000)  # Wait for 2 seconds

                    secu_gest = input_gesture()
                    return secu_gest
                elif event.key == pg.K_2:

                    screen.fill("black")
                    small_font = pg.font.Font(None, 24)
                    text_message = small_font.render("Please hold your Identification Gesture for 4 seconds. Thank you", True, "white")
                    screen.blit(text_message, (WINDOW // 2 - text_message.get_width() // 2, WINDOW // 2))
                    pg.display.flip()
                    pg.time.wait(2000)  # Wait for 2 seconds
                    secu_gest = input_gesture()
  #return gesture made by player
                    return secu_gest

# Get the selected profile from the main menu
secu_gest = main_menu()

# Define parameters of snake
snake = pg.rect.Rect([0, 0, TILE_SIZE - 2, TILE_SIZE - 2])
snake.center = get_random_position()
length = 1
segments = [snake.copy()]

# Define variable for snake to move
snake_dir = (0, 0)
time, time_step = 0, 110

# Create food and copy as snake's head
food = snake.copy()
food.center = get_random_position()

# Create dictionary to prevent from moving in opposite direction
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

# Initialize score
score = 0

# Game over flag and font setup
game_over = False
font = pg.font.Font(None, 74)


# Save and load state functions
def save_state():
    state = {
        "snake": snake,
        "length": length,
        "segments": segments,
        "snake_dir": snake_dir,
        "food": food,
        "dirs": dirs,
        "score": score,
    }
    with open("game_state.pkl", "wb") as file:
        pickle.dump(state, file)

def load_state():
    with open("game_state.pkl", "rb") as file:
        state = pickle.load(file)
    return (
        state["snake"],
        state["length"],
        state["segments"],
        state["snake_dir"],
        state["food"],
        state["dirs"],
        state["score"],
    )

# Flag to check if the player wants to save the game
save_prompt = False

# Flag to check if the player wants to start a new game or load saved data
new_game_prompt = False

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()

        if not game_over:
            # Make snake move using w a s d
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w and dirs[pg.K_w]:
                    snake_dir = (0, -TILE_SIZE)
                    dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}

                if event.key == pg.K_s and dirs[pg.K_s]:
                    snake_dir = (0, TILE_SIZE)
                    dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

                if event.key == pg.K_a and dirs[pg.K_a]:
                    snake_dir = (-TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}

                if event.key == pg.K_d and dirs[pg.K_d]:
                    snake_dir = (TILE_SIZE, 0)
                    dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}

    if not game_over:
        screen.fill("black")

        # Create a collision check
        colliding = pg.Rect.collidelist(snake, segments[:-1]) != -1

        # Create boundaries within window
        if (
            snake.left < 0
            or snake.right > WINDOW
            or snake.top < 0
            or snake.bottom > WINDOW
            or colliding
        ):
            # Game over
            game_over = True
            snake.center, food.center = get_random_position(), get_random_position()
            length, snake_dir = 1, (0, 0)
            segments = [snake.copy()]

            # Display game over message
            text_game_over = font.render("Game Over", True, "white")
            screen.blit(text_game_over, (WINDOW // 2 - text_game_over.get_width() // 2, WINDOW // 2 - 50))

            # Display prompt to start a new game or load saved data
            font_new_game_prompt = pg.font.Font(None, 36)
            text_new_game_prompt = font_new_game_prompt.render("Do you want to start a new game (N) or load saved data (L)?", True, "white")
            screen.blit(text_new_game_prompt, (WINDOW // 2 - text_new_game_prompt.get_width() // 2, WINDOW // 2 + 50))
            pg.display.flip()

            # Wait for player input
            new_game_response = None
            while new_game_response not in ['n', 'l']:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_n:
                            new_game_response = 'n'
                        elif event.key == pg.K_l:
                            new_game_response = 'l'

            if new_game_response == 'n':
                # Start a new game
                game_over = False
                score = 0
                segments = [snake.copy()]
            elif new_game_response == 'l':
                y = gestureCheck()
                check = compare_Input(secu_gest, y)
                if check != True:
                    break
                # Load saved data
                try:
                    snake, length, segments, snake_dir, food, dirs, score = load_state()
                except FileNotFoundError:
                    # If saved data not found, start a new game
                    game_over = False
                    score = 0
                    segments = [snake.copy()]

            # Reset flags
            save_prompt = False
            new_game_prompt = False

        # Check if food and snake match (position)
        if snake.center == food.center:
            food.center = get_random_position()
            length += 1
            # Increase the score
            score += 1

            # Check if the score is a multiple of 10
            if score % 10 == 0:
                save_prompt = True

            # Save state if the player wants to save
            if save_prompt:
                # Display prompt to save
                font_save_prompt = pg.font.Font(None, 36)
                text_save_prompt = font_save_prompt.render("Do you want to save the game? (Y/N)", True, "white")
                screen.blit(text_save_prompt, (WINDOW // 2 - text_save_prompt.get_width() // 2, WINDOW // 2 - 50))
                pg.display.flip()

                # Wait for player input
                save_response = None
                while save_response not in ['y', 'n']:
                    for event in pg.event.get():
                        if event.type == pg.KEYDOWN:
                            if event.key == pg.K_y:
                                save_response = 'y'
                            elif event.key == pg.K_n:
                                save_response = 'n'

                save_prompt = False  # Reset save prompt

                if save_response == 'y':
                    save_state()

        # Draw the score at the top of the screen
        font_score = pg.font.Font(None, 36)
        text_score = font_score.render(f"Score: {score}", True, "white")
        screen.blit(text_score, (10, 10))

        # Draw the snake and food on the canvas
        [pg.draw.rect(screen, "blue", segment) for segment in segments]
        [pg.draw.rect(screen, "red", food)]

        # Move snake and track time
        time_now = pg.time.get_ticks()
        if time_now - time > time_step:
            time = time_now

            snake.move_ip(snake_dir)
            segments.append(snake.copy())
            segments = segments[-length:]
    else:
        pg.display.flip()
        pg.time.wait(3000)  # Wait for 3 seconds before restarting the game
        game_over = False
        score = 0  # Reset the score
        segments = [snake.copy()]

        # Load state if available
        if score % 10 == 0:
            try:
                snake, length, segments, snake_dir, food, dirs, score = load_state()
            except FileNotFoundError:
                pass  # Ignore if the file is not found

    pg.display.flip()
    clock.tick(60)



