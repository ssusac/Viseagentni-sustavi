# common.py
import time
import random

current_symbol = None
correct_answer = None


def start_new_level(level=1):
    # Generiranje novog simbola za svaku razinu
    symbols = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]  # Možete promijeniti popis simbola prema svojim potrebama
    new_symbol = random.choice(symbols)
    duration = 6 - level

    return new_symbol, duration


def check_answer(user_input, current_symbol):
    return user_input == current_symbol


def measure_time(start_time):
    return time.time() - start_time
