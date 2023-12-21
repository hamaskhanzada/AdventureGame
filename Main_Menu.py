#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Created on: Mon Nov 20 2023
@Author: Mackenzie Furgerson, Daniel Buccos, Michele Sandhu, Hamas Khanzada
@Course: INF 6050
@University: Wayne State University
@Assignment: Character Stats of Final Project
    
@Python Version: 3.9.13x   
@Required Modules: Time, Sys, Adventure_Game, Pandas
    
@Description: input character stats and allows for choosing of characters
"""

########################### 
# IMPORT MODULES
###########################

import time, sys
import pandas as pandasForSortingCSV 

########################### 
# GLOBAL VARIABLES
###########################

# Character information and stats
characters = [
    {
        "Name": "Sir Hackalot",
        "Class": "Warrior",
        "HP": 90,
        "Attack": 10,
        "Defense": 14,
        "Speed": 6,
        "Description": "Sir Hackalot, a valiant warrior, wields a mighty sword"
        + " and dons sturdy armor. With a balance of offense and defense," 
        + " he excels in close combat. His special attack can turn the tide of"
        + " battle."
    },
    {
        "Name": "Merlin the Wise",
        "Class": "Wizard",
        "HP": 80,
        "Attack": 17,
        "Defense": 5,
        "Speed": 10,
        "Description": "Merlin the Wise is a master of arcane arts, wielding"
        + " powerful spells and mystical abilities. Though not as robust as a"
        + " warrior, Merlin's magical prowess allows for devastating attacks"
        + " and clever tricks."
    },
    {
        "Name": "Aria Swiftshadow",
        "Class": "Rogue",
        "HP": 70,
        "Attack": 13,
        "Defense": 7,
        "Speed": 14,
        "Description": "Aria Swiftshadow, a skilled rogue, relies on agility"
        + " and cunning. Armed with dual daggers, she excels at swift, precise"
        + " strikes and evasion. Aria's speed allows her to outmaneuver foes"
        + " and land critical hits."
    }
]

# Define rooms
character_creation = {
    "Name": "Character Creation",
    "Description": "\nCreate your character. Choose a class.",
}

########################### 
# USER-DEFINED FUNCTIONS
###########################

# Function to allow text to appear slowly
def print_slow(str):
    for letter in str:
        print(letter, end='', flush=True)
        time.sleep(0.005)
    print()
    
# Function to display the home menu
def show_home_menu():
    print_slow("\n+=======================+")
    print_slow("|=== Adventure Game === |")
    print_slow("+-----------------------+")
    print_slow("| 1. Play Game          |")
    print_slow("| 2. How to Play        |")
    print_slow("| 3. About              |")
    print_slow("| 4. High Scores        |")
    print_slow("| 5. Exit               |")
    print_slow("+=======================+")
    
# Function to display the how to play section
def show_how_to_play():
    content = ["Enter commands to navigate through the game.",
               "Type 'quit' to exit the game."]
    max_length = max(len(line) for line in content)

    print_slow("+" + "=" * (max_length + 4) + "+")
    print_slow("|\t\t\t\t=== HOW TO PLAY ===\t\t\t\t |")
    for line in content:
        print(f"|{line.center(max_length + 4)}|")
    print_slow("+" + "=" * (max_length + 4) + "+")
    
# Function to display the about section
def show_about():
    content = [
        "This is an adventure game created by Daniel Buccos,",
        "Kenzie Furgerson, Michele Sandhu, and Hamas Khanzada.",
        "",
        "In this game, you create your own character and launch them into a",
        "world full of chaos, adventure, and challenges. Your main goal is",
        "to level up your character and gain as much experience as possible!",
        "Be careful that the power does not go to your head!",
    ]
    max_length = max(len(line) for line in content)

    print_slow("+" + "=" * (max_length + 4) + "+")
    print_slow("|\t\t\t\t\t\t\t=== ABOUT ===\t\t\t\t\t\t\t   |")
    for line in content:
        print(f"|{line.center(max_length + 4)}|")
    print_slow("+" + "=" * (max_length + 4) + "+")

# Function to display the room information
def show_room(room):
    print_slow(f"\n| Welcome to {room['Name']} |")
    print(room["Description"])
    if "Classes" in room:
        print("Available Classes:")
        for class_name in room["Classes"]:
            print(f"- {class_name}")

#This will print and sort the high scores of the game!
def high_scores():
    print_slow("\n|Please see High Scores as follows!|")
    print_slow("|Experience gained determines rank!|\n")
    csvData = pandasForSortingCSV.read_csv("high_scores.csv") 
    csvData = csvData.sort_values(by='Experience')
    csvData.sort_values(["Experience"],  
                        axis=0, 
                        ascending=[False],  
                        inplace=True)
    print(csvData.to_string(index=False))

########################### 
# MAIN SCRIPT
###########################

current_room = character_creation

while True:
    show_home_menu()

    choice = input("\nSelect an option (1, 2, 3, 4, 5): ")

    if choice == "1":
        while True:
            show_room(current_room)

            # Print available characters with information
            print("\nAvailable characters:")
            for char_info in characters:
                print(
                    f"- {char_info['Name']} (Class: {char_info['Class']}, HP:"
                    f" {char_info['HP']}, Attack: {char_info['Attack']}," 
                    f" Defense: {char_info['Defense']}, Speed:" 
                    f" {char_info['Speed']})"
                )

            action = input("\nPlease select your character or enter 'quit' to" 
                           + " exit the game: ")

            if action.lower() == "quit":
                print_slow("\nThanks for playing. Goodbye!")
                sys.exit()

            # Check if the entered character name is valid
            chosen_char = next(
                (char_info for char_info in characters if 
                 char_info['Name'].lower() == action.lower()), None)
            if chosen_char:
                print_slow(f"\nYou have chosen {chosen_char['Name']}.")
                print(chosen_char['Description'])

                # Ask if the user wants to choose a different character
                change_char = input("\nDo you want to choose a different"
                                    + " character? (yes/no): ").lower()
                if change_char == "yes":
                    # Continue the loop to choose another character
                    continue
                else:
                    print_slow("\nLet the adventure begin!")
                    
                    #Had to include this even though it flags a warning in
                    #Spyder. Task does not run without it!
                    
                    import Adventure_Game
                        
                    if change_char == "no":
                        sys.path.append('/module')   
            else:
                print_slow("Invalid action. Try again.")

    elif choice == "2":
        show_how_to_play()
        input("\n|Press Enter to return to the main menu.|")

    elif choice == "3":
        show_about()
        input("\n|Press Enter to return to the main menu.|")
        
    elif choice == "4":
        high_scores()
        input("\n|Press Enter to return to the main menu.|")

    elif choice == "5":
        print_slow("\nThanks for playing. Goodbye!")
        sys.exit()

    else:
        print_slow("\nInvalid choice. Try again.")