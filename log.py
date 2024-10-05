import os

global history
history = ['', '', '', '', '', '', '', '', '','You find yourself alone in a cave.']

def displayHistory():
    for i in range(len(history)-10,len(history)):
        print(history[i])
    print('###################################################################')

def clear_history():
    global history
    history.clear()
    history = ['', '', '', '', '',''] * 2

def clear():
   os.system('clear')
