"""
Ultimate Hangman Quiz Game – Final Year Project
Author: Vidyashree V Naik
"""

import random
import time
import os
from datetime import datetime

HANGMAN_PICS = [
    """
     +---+
     |   |
         |
         |
         |
         |
    =========""", """
     +---+
     |   |
     O   |
         |
         |
         |
    =========""", """
     +---+
     |   |
     O   |
     |   |
         |
         |
    =========""", """
     +---+
     |   |
     O   |
    /|   |
         |
         |
    =========""", """
     +---+
     |   |
     O   |
    /|\  |
         |
         |
    =========""", """
     +---+
     |   |
     O   |
    /|\  |
    /    |
         |
    =========""", """
     +---+
     |   |
     O   |
    /|\  |
    / \  |
         |
    ========="""
]

QUIZ_DATA = {
    "Technology": [
        {"word": "python", "hint": "Popular programming language"},
        {"word": "algorithm", "hint": "Step-by-step procedure"},
        {"word": "compiler", "hint": "Translates source code to machine code"},
    ],
    "Movies": [
        {"word": "inception", "hint": "A dream within a dream"},
        {"word": "avatar", "hint": "Blue-skinned aliens"},
        {"word": "interstellar", "hint": "Time dilation in space"},
    ],
    "General Knowledge": [
        {"word": "oxygen", "hint": "Essential element to breathe"},
        {"word": "gandhi", "hint": "Father of Indian nation"},
        {"word": "amazon", "hint": "Largest rainforest"},
    ]
}

HIGH_SCORE_FILE = "scoreboard.txt"

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def get_random_question(category):
    return random.choice(QUIZ_DATA[category])

def display_game_state(hidden_word, wrong_attempts, used_letters, hint):
    print(HANGMAN_PICS[wrong_attempts])
    print(f"Hint: {hint}")
    print(f"Word: {' '.join(hidden_word)}")
    print(f"Used Letters: {', '.join(sorted(used_letters))}")
    print(f"Remaining Attempts: {len(HANGMAN_PICS) - 1 - wrong_attempts}")

def play_round(category, score, time_limit=30):
    question = get_random_question(category)
    word = question["word"]
    hint = question["hint"]
    hidden_word = ["_" for _ in word]
    wrong_attempts = 0
    used_letters = set()
    start_time = time.time()
    max_attempts = len(HANGMAN_PICS) - 1

    while wrong_attempts < max_attempts and "_" in hidden_word:
        clear_screen()
        display_game_state(hidden_word, wrong_attempts, used_letters, hint)
        elapsed_time = time.time() - start_time
        remaining_time = int(time_limit - elapsed_time)

        if remaining_time <= 0:
            print("⏰ Time's up!")
            break

        print(f"⏳ Time left: {remaining_time} seconds")
        guess = input("🔠 Enter a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("❌ Invalid input. Try again.")
            time.sleep(1)
            continue
        if guess in used_letters:
            print("⚠️ You've already used that letter.")
            time.sleep(1)
            continue

        used_letters.add(guess)

        if guess in word:
            for i, letter in enumerate(word):
                if letter == guess:
                    hidden_word[i] = guess
        else:
            wrong_attempts += 1
            print("❌ Wrong guess!")
            time.sleep(1)

    clear_screen()
    if "_" not in hidden_word:
        print(HANGMAN_PICS[wrong_attempts])
        print(f"🎉 Correct! The word was: {word}")
        print("✅ You Win this round!
")
        return score + 10
    else:
        print(HANGMAN_PICS[wrong_attempts])
        print(f"❌ You Lost! The word was: {word}
")
        return score - 5

def save_score(player_name, score):
    with open(HIGH_SCORE_FILE, "a") as file:
        file.write(f"{player_name} - {score} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
")

def show_high_scores():
    print("🏆 High Scores:")
    if not os.path.exists(HIGH_SCORE_FILE):
        print("No scores yet.")
        return
    with open(HIGH_SCORE_FILE, "r") as file:
        lines = file.readlines()
        scores = [line.strip() for line in lines if line.strip()]
        top_scores = sorted(scores, key=lambda x: int(x.split(" - ")[1]), reverse=True)[:5]
        for i, entry in enumerate(top_scores, 1):
            print(f"{i}. {entry}")
    print()

def main():
    score = 0
    clear_screen()
    print("🎮 Welcome to ULTIMATE HANGMAN QUIZ GAME!")
    player_name = input("Enter your name: ").strip().capitalize()
    while True:
        clear_screen()
        print(f"Player: {player_name} | Score: {score}")
        print("Categories:")
        for idx, cat in enumerate(QUIZ_DATA.keys(), 1):
            print(f"{idx}. {cat}")
        try:
            choice = int(input("Choose category (1/2/3): "))
            category = list(QUIZ_DATA.keys())[choice - 1]
        except (ValueError, IndexError):
            print("Invalid input. Try again.")
            time.sleep(1)
            continue

        score = play_round(category, score)
        print(f"💯 Total Score: {score}")
        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            break

    print(f"Thank you for playing, {player_name}!")
    save_score(player_name, score)
    show_high_scores()

if __name__ == "__main__":
    main()
