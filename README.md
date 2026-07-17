# blackjack-python
Blackjack python game - Isabel Edwards Cohort 20 

I chose to make a single player Blackjack game where you play against the computer for the First Python Project. It follows traditional casino rules so you can get the full experience of the casino without even leaving your room!

I made two versions:

-	Blackjack_gui.py which is a full graphical version built using Pygame. There is colour coded cards, buttons, live stats, and background music. All of this is made using code so there are no external images / audio files which hopefully should make everything run smoothly. 
-	Blackjack.py this is the original version which follows the same core logic but doesn’t include the fun visuals

How to Run 
GUI version 
	pip install pygame numpy 
python blackjack_gui.py
Terminal version
python blackjack.py

How to Play
1.	Both players (player and the dealer) are dealt two cards. One of the Dealer’s card stays hidden until games over
2.	On your turn you have two choices, 
a.	Hit – take another card (click the HIT button or type H in the terminal version)
b.	Stand – keep current hand and end your turn 
3.	If your hand goes over 21 you are bust and lose the game immediately 
4.	Once you stand the dealer will reveal their hidden card and must keep hitting until their value is either 17 or higher. 
5.	After this whoever is closer to 21 without going over wins the round!!!!!
a.	A two card 21 is a natural blackjack which is an automatic win, with its own fun victory jingle in the GUI version 
b.	Equal player and dealer hands results in a push (tie)
6.	Statistics are then shown and you can pick play again or quit, but obviously you’ll want to play again 

Card Values 

2 – 10 = Face value
J, Q, K	= 10 
Ace =	11 or 1 (whatever keeps you closer to 21 without busting)

Features

-	Shuffled 52 card deck each round 
-	Ace changes value depending on its role 
-	Input validation, in the GUI version buttons make invalid inputs impossible and in the terminal version it will make you type again rather than crashing 
-	Colour coded playing cards and casino table drawn directly in Pygame so no laggy image files required 
-	Sound effects and background music with sine waves in code so no audio file needed
-	Running session stats on screen
o	Games played
o	Player wins / Dealer wins / Pushes 
o	Blackjack hit 
o	Win rate

Project Structure

Blackjack_gui.py = the graphical version using Pygame
Blackjack.py = the terminal version 
Flowchart.png = visual flowchart of game 
README.md = this file 

AI Use

I used AI for the sound effects and the background music as audio on python wasn’t something I had done before so needed a little help. I did make sure that I actually understood what the code was doing before including it so in the future I’d be able to without the help of AI. The rest of the project is my own work. 

Requirements 

Python 3.x
GUI version needs pygame, numpy (pip install pygame numpy) 
Terminal version needs no external libraries 

Hope you have fun playing the game!

