#!/usr/bin/env python3
import os
import sys
import logging
import time
from colorama import init
from pyfiglet import Figlet
from InquirerPy import inquirer
from InquirerPy.validator import ValidationError

# Inicializa o Colorama
init(autoreset=True)

APP_VERSION = "Beta 2.4"

def configurar_logging(log_filename):
    try:
        logging.basicConfig(filename=log_filename, level=logging.INFO,
                            format="%(asctime)s - %(message)s")
        logging.info("Logging configured successfully.")
    except PermissionError:
        print("[ERROR]: Unable to access the log file at {log_filename}.")
        sys.exit(1)

def verificar_permissoes():
    if os.geteuid() != 0:
        print("[ERROR]: This script requires elevated permissions.")
        sys.exit(1)

def display_intro():
    f = Figlet(font='slant')
    print(f.renderText('Lbug-wlm'))
    print(f"Version: {APP_VERSION}\n")

def display_disclaimer():
    disclaimer = """
⚠️  This script is intended for educational purposes only.
The author assumes no responsibility for misuse or damage caused by this script.

Part of this code was generated via a Large Language Model (LLM). 

Feel free to use, modify, and fork this script without any restrictions. 🔓
    """
    print(disclaimer)

def list_files():
    return [f for f in os.listdir('.') if os.path.isfile(f)]

def select_files(files):
    selected_files = []
    while True:
        choices = [f"{file} (selected)" if file in selected_files else file for file in files]

        message = "Select a wordlist (minimum 2, maximum 10):"
        selected_file = inquirer.select(
            message=message,
            choices=choices,
        ).execute()
        
        if selected_file in selected_files:
            print(f"The file {selected_file} has already been selected.")
        else:
            selected_files.append(selected_file)
            print(f"File {selected_file} selected.")

        if len(selected_files) >= 2:
            message = "Do you want to add another file?"

            if len(selected_files) >= 10 or not inquirer.confirm(
                message=message,
                default=True
            ).execute():
                break

    return selected_files

def get_validated_input(prompt):
    while True:
        try:
            return int(inquirer.text(message=prompt).execute())
        except ValueError:
            print("Invalid input. Please enter a number.")

def merge_wordlists(files, min_length, max_length=None):
    unique_words = set()
    total_words = 0
    duplicate_words_count = 0

    for file in files:
        try:
            with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                for word in f.read().splitlines():
                    total_words += 1
                    if min_length <= len(word) <= (max_length or float('inf')):
                        if word in unique_words:
                            duplicate_words_count += 1
                        else:
                            unique_words.add(word)
        except FileNotFoundError:
            print(f"Error: File {file} not found.")
            sys.exit(1)

    sorted_words = sorted(unique_words, key=lambda x: (len(x), x))
    return total_words, sorted_words, duplicate_words_count

def save_wordlist(words, filename):
    print("\nSaving wordlist... 💾")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(words))
    logging.info(f"Wordlist saved as {filename}")

def preview_words(words, num=10):
    print(f"\nPreview of the first {num} words:\n")
    for word in words[:num]:
        print(f"- {word}")
    print("")  # Add a space after the last previewed word

def format_number(number):
    return f"{number:,}".replace(",", ".")

def get_file_size(filename):
    return os.path.getsize(filename)

def validate_output_filename(path):
    if not path.endswith('.txt'):
        raise ValidationError(message="The file must have a .txt extension")
    return True

def display_hack_the_planet():
    f = Figlet(font='slant')
    print(f.renderText('Hack the Planet!'))

def display_processing_animation(duration=10, description="Processing"):
    spinner = "|/-\\"
    for i in range(duration, 0, -1):
        sys.stdout.write(f"\r{description}... {spinner[i % len(spinner)]} {i} seconds remaining")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rDone!                              \n")  # Clear the line after completion

def main():
    verificar_permissoes()
    configurar_logging("lbug-wlm.log")
    display_intro()
    display_disclaimer()

    files = list_files()
    files_to_merge = select_files(files)

    min_length = get_validated_input("Enter the minimum number of characters: ")
    max_length_input = inquirer.text(message="Enter the maximum number of characters (or leave blank to ignore):").execute()
    max_length = int(max_length_input) if max_length_input else None

    # Exibe a animação de processamento após a escolha do número máximo de caracteres
    display_processing_animation(description="Validating input")

    total_words, sorted_words, duplicate_words_count = merge_wordlists(files_to_merge, min_length, max_length)
    
    preview_words(sorted_words)

    print("")  # Space between preview and the next prompt

    output_file = inquirer.text(
        message="Enter the name of the output file (with .txt):",
        validate=validate_output_filename
    ).execute()

    # Exibe a animação de processamento após definir o nome do arquivo
    display_processing_animation(description="Saving wordlist")

    save_wordlist(sorted_words, output_file)

    file_size = get_file_size(output_file)

    print(f"\n📁 Size of saved file: {format_number(file_size)} bytes")
    print(f"📊 Total words (all lists): {format_number(total_words)}")
    print(f"📊 Total unique words: {format_number(len(sorted_words))}")
    print(f"📊 Total duplicate words: {format_number(duplicate_words_count)}\n")

    display_hack_the_planet()
    
    print("Your feedback is important and will be greatly appreciated. Please send your impressions to littlebug.br@gmail.com.")

if __name__ == "__main__":
    main()
