__author__ = 'DavidSchechter'

# Student: David Schechter
# Student ID: 009987848
# Student: Gabe Guevara
# Student ID: 007617766

from crazy_eights import CrazyEight

#Driver class for Crazy 8 game
#creates an instance of the game and prompt the user for moves until game is over
#prints out who won the game

#welcome human player and prompt for player id
print("Welcome to the Crazy 8 Game")
print("What player would you like to be?")
print("Enter 0 for player 1 or 1 for player 2")
humanplayernumber_string = raw_input("Please enter your player number: ")
print("You selected player number " + humanplayernumber_string)

#create an instance of  the game
humanplayernumber = int(humanplayernumber_string)
if humanplayernumber == 0:
	human_first = True
	crazy_eight_board = CrazyEight(humanplayernumber, 1)
else:
	human_first = False
	crazy_eight_board = CrazyEight(humanplayernumber, 0)
print("\nYou hand is:")
print(crazy_eight_board.humanhand)
print("Face up card is:")
print(crazy_eight_board.faceupcard)
print("The suit of this card is:")
print(crazy_eight_board.suit)
print("Move made so far are:")
print(crazy_eight_board.historyofmoves)

#play the Crazy 8 until someone wins
while not crazy_eight_board.game_over():
	if human_first:
		human_move_string = raw_input(
			"Please make a legal move (like this (player_number,face_up_card,suit,cards_picked_up) ): ")
		only_number_string = human_move_string.replace("(", "")
		only_number_string = only_number_string.replace(")", "")
		human_move = only_number_string.split(",", 4)
		for i in range(len(human_move)):
			human_move[i] = int(human_move[i])
		human_move = tuple(human_move)
		if human_move[3] != 0:
			for i in range(human_move[3]):
				crazy_eight_board.humanhand.append(crazy_eight_board.deckofcards.pop())
			crazy_eight_board.historyofmoves.append(human_move)
			print("\nYou hand is:")
			print(crazy_eight_board.humanhand)
			print("Face up card is:")
			print(crazy_eight_board.faceupcard)
			print("The suit of this card is:")
			print(crazy_eight_board.suit)
			print("Move made so far are:")
			print(crazy_eight_board.historyofmoves)
			human_first = False
		else:
			if human_move[1] in crazy_eight_board.humanhand:
				crazy_eight_board.humanhand.remove(human_move[1])
				crazy_eight_board.faceupcard = human_move[1]
				crazy_eight_board.suit = human_move[2]
				crazy_eight_board.historyofmoves.append(human_move)
				print("\nYou hand is:")
				print(crazy_eight_board.humanhand)
				print("Face up card is:")
				print(crazy_eight_board.faceupcard)
				print("The suit of this card is:")
				print(crazy_eight_board.suit)
				print("Move made so far are:")
				print(crazy_eight_board.historyofmoves)
				human_first = False
			else:
				print("You tried to play a card that you don't have!!!")
	else:
		print("The Computer is thinking about his move. Be patient!!")
		temp_tuple = (crazy_eight_board.faceupcard, crazy_eight_board.suit, crazy_eight_board.computerhand,
					  crazy_eight_board.historyofmoves)
		movetoplay = crazy_eight_board.move(temp_tuple)
		if movetoplay[3] != 0:
			for i in range(movetoplay[3]):
				crazy_eight_board.computerhand.append(crazy_eight_board.deckofcards.pop())
			crazy_eight_board.historyofmoves.append(movetoplay)
			print("\nYou hand is:")
			print(crazy_eight_board.humanhand)
			print("Face up card is:")
			print(crazy_eight_board.faceupcard)
			print("The suit of this card is:")
			print(crazy_eight_board.suit)
			print("Move made so far are:")
			print(crazy_eight_board.historyofmoves)
			human_first = True
		else:
			crazy_eight_board.computerhand.remove(movetoplay[1])
			crazy_eight_board.faceupcard = movetoplay[1]
			crazy_eight_board.suit = movetoplay[2]
			crazy_eight_board.historyofmoves.append(movetoplay)
			print("\nYou hand is:")
			print(crazy_eight_board.humanhand)
			print("Face up card is:")
			print(crazy_eight_board.faceupcard)
			print("The suit of this card is:")
			print(crazy_eight_board.suit)
			print("Move made so far are:")
			print(crazy_eight_board.historyofmoves)
			human_first = True

#print out who won the game
if len(crazy_eight_board.humanhand) == 0:
	print("You have beaten the computer")
elif len(crazy_eight_board.computerhand) == 0:
	print("You were beaten by the computer!! shame on you!!")
else:
	if len(crazy_eight_board.humanhand)<len(crazy_eight_board.computerhand):
		print("You have beaten the computer")
	else:
		print("You were beaten by the computer!! shame on you!!")
