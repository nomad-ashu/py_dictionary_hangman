# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:10:21 2021

@author: Ashu
"""

import json
from difflib import get_close_matches
import random

data = json.load(open('data.json', 'r'))

mode = ['dictionary', 'hangman']
def mode_selection():
    selected_mode = input('Select mode: \nPress "1" for dictionary\nPress "2" for Hangman\nPress "X" to quit\n')
    if selected_mode == '1':
        dictionary()
    elif selected_mode == '2':
        hangman()
    elif ((selected_mode == 'X') or (selected_mode == 'x')):
        return(0)
    else:
        print('Kindly select a valid option.')
        mode_selection()

# Dictonary mode
def dictionary():
    input_word = input('Enter a word: ').lower()
    if (input_word in data):
        print(input_word)
        for item in data[input_word]:
            print(f'-- {item}')
    else:
        suggested_word = get_close_matches(input_word, data, 1)
        print(f'"{input_word}" not found. Do yu mean "{suggested_word[0]}"?')
        alt_search = input(f'Enter Y if you want to search for {suggested_word[0]}, else press any other key: ').upper()
        if (alt_search == 'Y'):
            print(suggested_word[0])
            for item in data[suggested_word[0]]:
                print(f'-- {item}')
        else:
            dictionary()
        
#dictionary()

#hangman game mode

def hangman():
    level_conditions = [{"level": 1,"allowed_chars": [4,7],"allowed_lives": 5,"hint_enabled": True},{"level": 2,"allowed_chars": [8,10],"allowed_lives": 5,"hint_enabled": True},{"level": 3,"allowed_chars": [11,15],"allowed_lives": 5,"hint_enabled": True}]
    
    lvl_input = int(input('Enter the level you want to play [1, 2, 3]: '))
    all_words = list(data.keys())
    
    #get a word from all words list
    def get_word_level():
        word_found = False
        while not word_found:
            word_level = all_words[random.randint(1, len(all_words))]
            word_length_limit = level_conditions[lvl_input-1]['allowed_chars']
            if ((len(word_level) >= word_length_limit[0]) and (len(word_level) <= word_length_limit[1])):
                if ' ' not in word_level:
                    word_found = True
                    return word_level
    
    selected_word_raw = get_word_level()
    selected_word = selected_word_raw.upper()
    #print(selected_word)
    
    #Starting the game. Showing first blanks
    total_lives = level_conditions[lvl_input-1]['allowed_lives']
    input_string = []
    show_string = ""
    game_status = {'won': False, 'complete': False, 'lives_remaining': total_lives}
    for i in range(0,len(selected_word)):
        input_string.append('-')
        show_string += input_string[i] 
    print(show_string)
    
    #Take input and show current string
    def check_input(input_string, game_status):
        char_found = False
        show_string = ""
        input_char = input("Enter a character: ").upper()
        for i in range(0,len(selected_word)):
            if (selected_word[i] == input_char):
                input_string[i] = input_char
                char_found = True
                if '-' not in input_string:
                    game_status['won'] = True
                    game_status['complete'] =  True
        if not char_found:
            if game_status['lives_remaining'] == 1:
                game_status['complete'] = True
            else:
                game_status['lives_remaining'] -= 1
                print('Wrong char selected. Remaining lives: ', game_status['lives_remaining'])
        for i in range(0,len(input_string)):
            show_string += input_string[i]
        print(show_string)
        return game_status
    #Call until gane is not complete
    while not game_status['complete']:
        check_input(input_string, game_status)
    
    if game_status['won'] == True:
        print('Congratulations, you won!!!')
    else:
        print('Sorry, you lost!!!')
        print('Word: ', selected_word)
        for item in data[selected_word_raw]:
            print(f'-- {item}')
 
#hangman()
        
mode_selection()