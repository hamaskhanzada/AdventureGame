#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Created on: Fri Nov  3 07:08:51 2023
@Author: Mackenzie Furgerson, Daniel Buccos, Michele Sandhu, Hamas Khanzada
@Course: INF 6050
@University: Wayne State University
@Assignment: Combat Section of Final Project
    
@Python Version: 3.9.13x   
@Required Modules: random, json, BeautifulSoup
    
@Description: handles combat and encounters for the final group project.
"""
########################### 
# IMPORT MODULES
###########################

import random, json, sys, csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
from Main_Menu import chosen_char

########################### 
# GLOBAL VARIABLES
###########################

#This gets a list of vowels for monster names, sets the acceptable comat loop
#options, and sets a dictionary for use with the JSON file.
vowel = "aeiou"
options = ["a","d","r","quit"]
table_data = []
encounter_chance = ""

#This assigns character stats from Main_Menu python file.

player_hp = chosen_char["HP"]
player_attack = chosen_char["Attack"]
player_defense = chosen_char["Defense"]
player_speed = chosen_char["Speed"]
player_level = 1
player_exp = 0
xp_to_level = 1000
completed = "No"

########################### 
# USER-DEFINED FUNCTIONS
###########################

#User defined function is here for dice rolls in comabt.
def roll():
    return random.randrange(1, 20)

#This calculates the stat differential based on the attacker's stat,
#defender's stat, and roll. The varaible "c" is returns the total score.
#Any total value over a 0 should be counted as a success.
def calculation(r, attacker_stat, defender_stat):
    global c
    c = int(r) + int(attacker_stat) - int(defender_stat)

#This prints the results of the roll along with the stats used to calculate.
def results(c, attacker_stat, defender_stat):
    print("\nA roll of " + str(r) + " is logged, plus the aggresors's " +
          str(attacker_stat) + ", minus the defender's " +
          str(defender_stat) + " equaling: " + str(c))
    print("\n+" + "=" * 100 + "+")

#This function prints the experience accumulated if the user quits or dies.
#and writes to high_scores.csv.
def quitter():
    print("\nThank you for playing! You managed to accumulate " +
          str(player_exp) + " experience this run and attained level " +
          str(player_level) + ".")
    i = input("Please enter your name for scoring purposes:")
    list = [i, player_exp, player_level, completed, chosen_char["Name"]]
    
    with open(r'high_scores.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(list)
        f.close()
    sys.exit()

########################### 
# SCRIPT HERE
###########################

i = ""
while i != "quit":
    
    #If conditional for when a player levels ups starts here.
    if player_exp > xp_to_level:
        player_level = player_level + 1
        print("\n+" + "*" * 100 + "+")
        chosen_char["HP"] = chosen_char["HP"] + 2
        chosen_char["Attack"] = chosen_char["Attack"] + 2
        chosen_char["Defense"] = chosen_char["Defense"] + 2
        chosen_char["Speed"] = chosen_char["Speed"] + 2
        print("Congratulation! You have reached level " + str(player_level) +
              "! Your HP is now " + str(chosen_char["HP"]) + ", attack is " + 
                str(chosen_char["Attack"]) + ", defense is " +
                str(chosen_char["Defense"]) + ", and speed is " +
                str(chosen_char["Speed"]) + ".")
        xp_to_level = xp_to_level + 1000
        
        #If player hits level 7, the game concludes.
        if player_level == 7:
            print("\n"*50)
            print("\n+" + "*" * 100 + "+")
            print("\n+" + "*" * 100 + "+")
            print("\n+" + "*" * 100 + "+")
            print("The broken bones and rendered flesh of your foes all lie " +
            "before you in a crumpled mess. You sharply breathe in through " +
            "your nose, deeply inhaling the " +
            "scent of decomposition. The local " +
            "villagers implore you to stop your culling, but their shouts " +
            "fall on deaf ears. You have finalized the ritual and " +
            "ascended to Godhood.")
            print("\nCongratulations! You have won, but find that you were " +
                  "the true monster all along... May God have mercy on " +
                  "your soul...")
            print("+" + "*" * 100 + "+")
            print("\n+" + "*" * 100 + "+")
            print("\n+" + "*" * 100 + "+")
            completed = "Yes"
            quitter()
        
    
    #THis refreshes the player's stats after each encounter.
    player_hp = chosen_char["HP"]
    player_attack = chosen_char["Attack"]
    player_defense = chosen_char["Defense"]
    player_speed = chosen_char["Speed"]
    
    #This randomizes encounters and battles.
    encounter_chance = random.randrange(1, 3)
    
    if encounter_chance == 1:
        #This opens the table of Monsters and Encounters.
        with open('Monsters and Encounters.json') as json_file:
            table_data = json.load(json_file)
        
    # This gets weather details for today in Detroit.
    my_page = ('http://forecast.weather.gov/MapClick.' + 
    'php?lat=42.3754&lon=-83.0791#.WgxdZhOPLb8')
    webpage = urlopen(my_page)
    soup = BeautifulSoup(webpage.read(), 'html.parser')
    seven_day = soup.find(id="seven-day-forecast")
    forecast_items = seven_day.find_all(class_="tombstone-container")
    today = forecast_items[0]
    attribute_val_from_image = today.find('img')['alt']
    
    #This gets monsters from monster's JSON based on player_level and challenge
    #rating.
    if encounter_chance == 1:
        while True:
            Monster = random.choice(table_data["Monsters"])
            if int(Monster["Challenge Rating"]) < player_level * 30:
                break
    
    #This gets battlefied conditions from weather in Detroit, MI and prints.
    #The character and monster stats are impacted by the current weather.
    #After combat, please reload all player stats to undo status effects from
    #combat encounter to combat encounter.
    if encounter_chance == 1:
        if "cloudy" in attribute_val_from_image:
            conditions = ("The battlefied is choked with clouds this day! "
            + "Your movements, along with your oppostion's, are slowed!")
            player_speed = player_speed - 2
            Monster["Speed"] = int(Monster["Speed"]) - 2
        elif "sun" in attribute_val_from_image:
            conditions = ("The bright orb of the sun beats down "
            + "upon the field of battle. You lose health for playing video "
            + "games when it is so nice outside.")
            player_hp = player_hp - 10
        elif "showers" or "rain" in attribute_val_from_image:
            conditions = ("Heavy clouds, weighted with accumulation, pour down"
            + " upon "
            + "the battlefiend. You sense defects in your opponent's defenses."
            )
            Monster["Defense"] = int(Monster["Defense"]) - 2
        elif "snow" in attribute_val_from_image:
            conditions = ("White puffy snow softly descends before you and" + 
            " your opponent. You feel a sense of disquiet before the" +
            " inevitable struggle. The ground is slicker slowing you both" + 
            " down.")
            player_speed = player_speed - 2
            Monster["Speed"] = int(Monster["Speed"]) - 2
        elif "hail" or "sleet" in attribute_val_from_image:
            conditions = ("A cold percipitation makes the battlefied "
            + "conditions far more dangerous! You and your foe take damage!")
            player_hp = player_hp - 5
            Monster["HP"] = int(Monster["HP"]) - 5
        
        #This appends the monster's name with the correct indefinite article.
        if (Monster["Name"][0]).lower() in vowel:
           Monster["Name"] = "An " + Monster["Name"]
        else:
           Monster["Name"] = "A " + Monster["Name"]
        
        #Print conditions and Monster details in advance of combat loop and 
        #print instructions for the user.
        print("\n+" + "-" * 100 + "+")
        print("\n" + Monster["Name"] + " chooses to bar your progress with " +
              "violent malice. You will have to fight your way though or " + 
              "runaway!")
        print(Monster["Description"])
        print ("\n" + conditions)
        print('\nAttack by entering "a"')
        print('Defend by entering "d"')
        print('Attempt to run by entering "r"')
        print('Quit the game and end your adventure by entering "quit"')
        
        #The combat cycle begins here and continues until either the user runs,
        #dies, or defeats the monster.
        counter = 0
        while True:
            
            #This flushes variables between rounds and ups the round counter.
            counter = counter + 1
            attacker_stat = ""
            defender_stat = ""
            
            #This prints a divider between rounds and prints the round number.
            print("\n+" + "-" * 100 + "+")
            print("\n" + Monster["Name"] + " yet blocks your path forwards. " + 
                      "Round: " + str(counter) + " will begin with your " +
                      "decision.")
            i = input("Enter a, d, r, or quit now please:")
            i = i.lower()
            
            #This will execute the quitter logic if the user quits.
            if i == "quit":
                quitter()
                break
            
            #Logic for when a player chooses to attack begins here.
            if i == "a":
                print("\nYou attack with ferocity! Your speed stat will be" +
                      " compared against your opponent's speed.")
                
                #The check to see if the player hits starts here.
                attacker_stat = player_speed
                defender_stat = Monster["Speed"]
                r = roll()
                calculation(r, attacker_stat, defender_stat)
                results(c, attacker_stat, defender_stat)
                
                #Damage calculation is as follows on a succesful hit.
                if c > 0:
                    print("\nThe attack lands! Your attack will now be " +
                          "compared against your opponent's defense.")
                    attacker_stat = player_attack
                    defender_stat = Monster["Defense"]
                    r = roll()
                    calculation(r, attacker_stat, defender_stat)
                    results(c, attacker_stat, defender_stat)
                    if c > 0:
                        Monster["HP"] = int(Monster["HP"]) - int(c)
                        print("\n" + Monster["Name"] + " takes " + str(c) + 
                              " damage.")
                    
                #Message prints here if the hit fails or the damage is 
                #negative.
                if c <= 0:
                    print("\nYour adversary defltly deflects the assualt.")
                    
                #Logic for when a monster runs out of HP begins here. Combat
                #ends here and player is awarded experience points based on 
                #the monster's challenge rating.
                if int(Monster["HP"]) < 0:
                    print("\n" + Monster["Name"] + " has received a " +
                          "debilitating blow. You gracefully deliver a coupe " 
                          + "de grace and the monster expires. Your way " + 
                          "forwards is now clear.")
                    print("\nYou have received " + 
                          str(Monster["Challenge Rating"]) +
                          " experience from the combat event.")
                    player_exp = int(Monster["Challenge Rating"])
                    + int(player_exp)
                    break
                
            #Logic for when a player chooses to run begins here and initiates
            # roll.
            if i == "r":
                print("You scramble to make a cowardly retreat from the " + 
                      "threat. Your speed will be compared against your " + 
                      "opponent's speed.")
                attacker_stat = Monster["Speed"]
                defender_stat = player_speed
                r = roll()
                calculation(r, attacker_stat, defender_stat)
                results(c, attacker_stat, defender_stat)
                
                #Monster success message is printed here.
                if c >= 0:
                    print("\nYou daftly stumble backwards over your own two " +
                          "feet and grant your opposition a free attack!")
                    
                #Player success message begins here and combat loop is exited.
                if c < 0:
                    print("\nYou succesfully evade a blow and slip away into "
                          + "the shadows undetected. After a short period, "+
                          "your foe loses intrest in relocating you and moves" 
                          + " on. Once it feels safe, you come out of hiding"
                          +" and resume your adventure.")
                    break
            
            #Logic for when a player chooses to defend begins here. Each 
            #defense selection will increase the player's defenses by 5. 
            #This bonus defense should be wiped out at the conclusion of 
            #combat. I would recommend reloading all player stat variables at 
            #combat conclusion, other than experience which should increase 
            #from encounter to encounter.
            if i == "d":
                print("\nYou forgo making an assualt on your opposition's" +
                      " defenses and choose to bolster your own instead.")
                player_defense = player_defense + 5
                
            #This handles if the user makes an incorrect selection.
            if i not in options:
                print("\nInvalid selection. Please try again.")
                counter = counter - 1
                continue
                
            #The Monster's attack logic begins here and roll is initiated.
            print("\nYour opposition lurchs forward and lashes out in "+
                  "violence! Your speed will be compared against the " + 
                  "aggressor's speed.")
            attacker_stat = Monster["Speed"]
            defender_stat = player_speed
            r = roll()
            calculation(r, attacker_stat, defender_stat)
            results(c, attacker_stat, defender_stat)
            
            #Logic for if the monster lands a succesful blow begins here and 
            #assigns damage to the player.
            if c > 0:
                print("\nYour adversary catches you off guard and pierces your" 
                      + " defenses. Their attack will now be compared against"
                      + " your defense to determine the damage you have "
                      + "suffered.")
                attacker_stat = Monster["Speed"]
                defender_stat = player_speed
                r = roll()
                calculation(r, attacker_stat, defender_stat)
                results(c, attacker_stat, defender_stat)
                if c > 0:
                    player_hp = player_hp - c
                    print("\nYou suffer " + str(c) + " damage from the attack "
                          + "leaving you with " + str(player_hp) + " hit " + 
                          "points left.")
                
                #Logic for if the player runs out of HP begins here. The game 
                #should end here.
                if player_hp <= 0:
                    print("With that last strike, you fall to the earth, " + 
                          "slowly your vision blurs" + 
                          " and your conciousness fades into blackness. " + 
                          "You have perished from the combat encounter.")
                    quitter()
                    break
                    
            #This prints a message if the monster's attack fails or the damage
            #roll ends up being negative.
            if c <= 0:
                print("\nA bob, weave, parry, and block get you out of" + 
                      " danger this time. You receive no damage from the "+ 
                      "attack.")
    
    if encounter_chance == 2 or 3:
        #This opens the table of Monsters and Encounters.
        with open('Monsters and Encounters.json') as json_file:
            table_data = json.load(json_file)
            Encounter = random.choice(table_data["Random Encounters"])
            print("\n+" + "-" * 100 + "+")
            print("\n" + str(Encounter["Encounter"]))
            xp_gain = Encounter["Experience Gain"]
            xp_gain = xp_gain[:-3]
            player_exp = player_exp + int(xp_gain)
            print("\nYou have gained " + xp_gain + " experience points")
