__author__ = 'DavidSchechter'


# Student: David Schechter
# Student ID: 009987848
# Student: Gabe Guevara
# Student ID: 007617766

import sys
import random
import collections
import copy


#Class definition of CrazyEight - the card game Crazy 8
#human player number,computer player number, deck of cards, the human's hand, the computer's hand,
#what is the face up card now,the suit of the face up card,history of all moves
#builder receives humanplayernumber and computerplayernumber and create a random deck, hands out
#cards for each player, and set the face up card and its suit

class CrazyEight:
	def __init__(self, humanplayernumber, computerplayernumber):
		self.humanplayernumber = humanplayernumber
		self.computerplayernumber = computerplayernumber
		self.deckofcards = []
		self.humanhand = []
		self.computerhand = []
		self.faceupcard = -1
		self.suit = -1
		self.historyofmoves = []
		# for i in range(51):
		# self.deckofcards.append(random.randrange(0, 51, 1))
		self.deckofcards = random.sample(range(52), 52)
		for i in range(7):
			randomchoice = random.choice(self.deckofcards)
			self.humanhand.append(randomchoice)
			self.deckofcards.remove(randomchoice)
		for i in range(7):
			randomchoice2 = random.choice(self.deckofcards)
			self.computerhand.append(randomchoice2)
			self.deckofcards.remove(randomchoice2)
		randomchoice3 = random.choice(self.deckofcards)
		self.deckofcards.remove(randomchoice3)
		if randomchoice3 < 13:
			self.suit = 0
		elif (randomchoice3 > 12) and (randomchoice3 < 26):
			self.suit = 1
		elif (randomchoice3 > 25) and (randomchoice3 < 39):
			self.suit = 2
		else:
			self.suit = 3
		self.faceupcard = randomchoice3


	#Class function for getting a move for the computer from a partial state
	#Class function create 100 randomly genetrated games and uses Minimax algorithm to find
	#best possible move
	# Classfunction receives a tuple of temp state of the game which is: the computer's
	#hand,the face up crad, the suit and history of all moves

	def move(self, temp_tuple):
		hand = temp_tuple[2]
		history = temp_tuple[3]
		humannuberofcards = 8
		for tempmovelist in history:
			if tempmovelist[0] != self.computerplayernumber:
				if tempmovelist[3] != 0:
					humannuberofcards = humannuberofcards + tempmovelist[3]
				else:
					humannuberofcards -= 1
		arrayofbestmoves = []
		for i in range(100):
			tempdeckofcards = random.sample(range(52), 52)
			for card in hand:
				tempdeckofcards.remove(card)
			temphumanhand = []
			for j in range(humannuberofcards):
				randomchoice4 = random.choice(tempdeckofcards)
				temphumanhand.append(randomchoice4)
				tempdeckofcards.remove(randomchoice4)
			full_temp_tuple = (tempdeckofcards, temphumanhand, temp_tuple)
			arrayofbestmoves.append(self.move_perfect_knowledge(full_temp_tuple))
		counts = collections.Counter(arrayofbestmoves)
		mostcommonlist = counts.most_common()
		if len(mostcommonlist) == 1:
			mostcommontuple = mostcommonlist[0]
			mostcommon = mostcommontuple[0]
		else:
			mostcommontuple = mostcommonlist[0]
			mostcommon = mostcommontuple[0]
		return mostcommon

	#Class function for getting a move for the computer from a full state
	#Class function uses Minimax algorithm to find best possible move
	#Class function receives a tuple of full state of the game which is: the human's hand,
	# the deck of card, the computer's, hand,the face up crad, the suit
	# and history of all moves

	def move_perfect_knowledge(self, full_temp_tuple):
		deckofcards = full_temp_tuple[0]
		humanhand = full_temp_tuple[1]
		temp_tuple = full_temp_tuple[2]
		face_up_card = temp_tuple[0]
		suit = temp_tuple[1]
		hand = temp_tuple[2]
		history = temp_tuple[3]
		best_score = -sys.maxint
		best_move = (0, 0, 0, 0)
		is_max = True
		alpha_for_max = -sys.maxint
		beta_for_min = sys.maxint
		possiblemoves = self.getpossiblemoves(self.computerplayernumber, hand, face_up_card, suit, history)
		for move in possiblemoves:
			temp_computer_hand = copy.deepcopy(hand)
			temp_deckofcards = copy.deepcopy(deckofcards)
			temp_history = copy.deepcopy(history)
			copy_face_up_card = copy.copy(face_up_card)
			copy_suit = copy.copy(suit)
			temp_deckofcards, temp_humanhand, temp_face_up_card, temp_suit, temp_hand, temp_history = self.create_temp_game_state(
				move, temp_deckofcards, humanhand, copy_face_up_card, copy_suit, temp_computer_hand, temp_history)
			temp_best_score = self.heuristic_minimax_with_alpha_beta(temp_deckofcards, temp_humanhand,
																	 temp_face_up_card, temp_suit, temp_hand,
																	 temp_history, 0, is_max, alpha_for_max,
																	 beta_for_min)
			if is_max and (temp_best_score > best_score):
				best_move = move
				best_score = temp_best_score
			elif (not is_max) and (temp_best_score < best_score):
				best_move = move
				best_score = temp_best_score
		return best_move


	#Class function for Minimax algorithm with alpha beta prunning
	#Class function uses Minimax algorithm to find best possible move
	#Class function receives a tuple of full state of the game which is: the human's hand,
	# the deck of card, the computer's, hand,the face up crad, the suit
	# and history of all moves
	def heuristic_minimax_with_alpha_beta(self, temp_deckofcards, temp_humanhand, temp_face_up_card, temp_suit,
										  temp_hand, temp_history, depth, is_max, alpha_for_max, beta_for_min):
		if self.cut_off_test(depth, temp_humanhand, temp_hand, temp_deckofcards):
			return self.utility(temp_humanhand, temp_hand)
		temp_possiblemoves = self.getpossiblemoves(self.computerplayernumber, temp_hand, temp_face_up_card, temp_suit,
												   temp_history)
		for move in temp_possiblemoves:
			temp_computer_hand = copy.deepcopy(temp_hand)
			temp_copy_deckofcards = copy.deepcopy(temp_deckofcards)
			temp_copy_history = copy.deepcopy(temp_history)
			copy_face_up_card = copy.copy(temp_face_up_card)
			copy_suit = copy.copy(temp_suit)
			new_temp_deckofcards, new_temp_humanhand, new_temp_face_up_card, new_temp_suit, new_temp_hand, new_temp_history = self.create_temp_game_state(
				move, temp_copy_deckofcards, temp_humanhand, copy_face_up_card, copy_suit, temp_computer_hand,
				temp_copy_history)
			if is_max:
				alpha_for_max = max(alpha_for_max,
									self.heuristic_minimax_with_alpha_beta(new_temp_deckofcards, new_temp_humanhand,
																		   new_temp_face_up_card, new_temp_suit,
																		   new_temp_hand, new_temp_history, depth + 1,
																		   (not is_max), alpha_for_max, beta_for_min))
			else:
				beta_for_min = min(beta_for_min,
								   self.heuristic_minimax_with_alpha_beta(new_temp_deckofcards, new_temp_humanhand,
																		  new_temp_face_up_card, new_temp_suit,
																		  new_temp_hand, new_temp_history, depth + 1,
																		  (not is_max), alpha_for_max, beta_for_min))
			if beta_for_min <= alpha_for_max:
				if is_max:
					return alpha_for_max
				else:
					return beta_for_min
		if is_max:
			return alpha_for_max
		else:
			return beta_for_min

	#Class function for Minimax algorithm with alpha beta prunning - cut off test
	#Class function checks if algorithm is at a cut of state of the game
	#Class function receives depth,human's hand,computer's hand,deck of cards

	def cut_off_test(self, depth, temp_humanhand, temp_hand, temp_deck):
		if (depth == 10) or self.temp_game_over(temp_humanhand, temp_hand,temp_deck) or (len(temp_deck) == 0):
			return True
		else:
			return False

	#Class function for Minimax algorithm with alpha beta prunning - utility value
	#Class function returns the utility of the algorithm for any state of the game
	#Class function receives human's hand,computer's hand

	@staticmethod
	def utility(temp_humanhand, temp_hand):
		return len(temp_hand) - len(temp_humanhand)

	#Class function for Minimax algorithm with alpha beta prunning - if game is over
	#Class function returns if the game is over
	#Class function receives human's hand,computer's hand, deck of cards

	@staticmethod
	def temp_game_over(temp_humanhand, temp_hand,temp_deck):
		if (len(temp_hand) == 0) or (len(temp_humanhand) == 0) or (len(temp_deck) == 0):
			return True
		else:
			return False

	#Class function returns if the game is over
	#Class function receives human's hand,computer's hand, deck of cards

	def game_over(self):
		if (len(self.computerhand) == 0) or (len(self.computerhand) == 0) or (len(self.deckofcards) == 0):
			return True
		else:
			return False

	#Class function for Minimax algorithm with alpha beta prunning - temp state of game
	#Class function returns a temporary state of the game after a move was made
	#Class function receives human's hand,computer's hand, deck of cards

	@staticmethod
	def create_temp_game_state(move, deckofcards, humanhand, face_up_card, suit, hand, history):
		if move[3] != 0:
			if move[3] > (len(deckofcards) - 1):
				cards_to_pick_up = len(deckofcards) - 1
			else:
				cards_to_pick_up = move[3]
			for i in range(cards_to_pick_up):
				hand.append(deckofcards.pop())
				history.append(move)
		else:
			hand.remove(move[1])
			face_up_card = move[1]
			suit = move[2]
			history.append(move)
		return deckofcards, humanhand, face_up_card, suit, hand, history

	#Class function for Minimax algorithm with alpha beta prunning - possible move in the game
	#Class function returns a list of tuples of all possible moves that can be made
	#from a give state of the game
	#Class function receives player's number, player's hand, face up card
	#face up card's suit, deck of cards

	def getpossiblemoves(self, player_number, hand, face_up_card, suit, history):
		possiblemoves = []
		if face_up_card == 11:
			possiblemoves.append((self.computerplayernumber, face_up_card, suit, 5))
			return possiblemoves
		if (face_up_card == 10) or (face_up_card == 23) or (face_up_card == 36) or (face_up_card == 49):
			# possiblemoves.append((self.computerplayernumber,face_up_card,suit,0))
			return possiblemoves
		elif (face_up_card == 1) or (face_up_card == 14) or (face_up_card == 27) or (face_up_card == 40):
			two_cards_in_hand = []
			for i in range(len(hand)):
				if (hand[i] == 1) or (hand[i] == 14) or (hand[i] == 27) or (hand[i] == 40):
					two_cards_in_hand.append(hand[i])
			if len(two_cards_in_hand) == 0:
				if len(history) > 1:
					last_move_location = len(history) - 1
					played_a_two_card = True
					how_many_to_pick_up = 0
					while played_a_two_card:
						prev_move = history[last_move_location]
						if (prev_move[1] == 1) or (prev_move[1] == 14) or (prev_move[1] == 27) or (prev_move[1] == 40):
							how_many_to_pick_up += 2
						else:
							played_a_two_card = False
						last_move_location -= 1
						if last_move_location < 0:
							played_a_two_card = False
					possiblemoves.append((self.computerplayernumber, face_up_card, suit, how_many_to_pick_up))
				else:
					possiblemoves.append((self.computerplayernumber, face_up_card, suit, 2))
				return possiblemoves
			else:
				for card in two_cards_in_hand:
					if card < 13:
						tempsuit = 0
					elif (card > 12) and (card < 26):
						tempsuit = 1
					elif (card > 25) and (card < 39):
						tempsuit = 2
					else:
						tempsuit = 3
					possiblemoves.append((self.computerplayernumber, card, tempsuit, 0))
				return possiblemoves
		else:
			for i in range(len(hand)):
				if hand[i] < 13:
					tempsuit = 0
				elif (hand[i] > 12) and (hand[i] < 26):
					tempsuit = 1
				elif (hand[i] > 25) and (hand[i] < 39):
					tempsuit = 2
				else:
					tempsuit = 3
				if hand[i] + 13 == face_up_card:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif hand[i] + 26 == face_up_card:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif hand[i] + 39 == face_up_card:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif hand[i] == face_up_card - 13:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif hand[i] == face_up_card - 26:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif hand[i] == face_up_card - 39:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif (hand[i] == 7) or (hand[i] == 20) or (hand[i] == 33) or (hand[i] == 46):
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
				elif tempsuit == suit:
					possiblemoves.append((self.computerplayernumber, hand[i], tempsuit, 0))
			if len(possiblemoves) == 0:
				possiblemoves.append((self.computerplayernumber, face_up_card, suit, 1))
			return possiblemoves