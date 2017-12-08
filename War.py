#  File: War.py
#  Description: This program simulates a game of War. Each player is dealt a hand and during each round, they
#  remove the top card and see who has the higher card. The winner collects all the cards dealt. If both players
#  play cards with the same value, then each player continues to play 3 facedown cards and 1 faceup card until someone
#  wins war. The game ends when one player has all the cards.
#  Student's Name: Brian Tsai
#  Student's UT EID: byt76
#  Course Name: CS 313E
#  Unique Number: 51465
#
#  Date Created: 9/26/17
#  Date Last Modified: 9/27/17

import random

class Card:

    # Dictionary of card ranks
    Rank = {"2" : 2, "3" : 3, "4" : 4, "5" : 5, "6" : 6, "7" : 7, "8" : 8, "9" : 9, "10" : 10, "J" : 11, "Q" : 12, "K" : 13, "A" : 14}

    # Initialize a new card
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    # Return a string indicating which card has the higher value
    def __eq__(self, other):
        if (self.Rank[self.rank] > self.Rank[other.rank]):
            return str(self) + " >  " + str(other)
        elif (self.Rank[self.rank] < self.Rank[other.rank]):
            return str(other) + " >  " + str(self)
        else:
            return str(self) + " =  " + str(other)

    # Return the rank of the card according to the dictionary
    def getRankOrder(rank):
        return Card.Rank[rank]

    # Return which value and suit of the card is
    def __str__(self):
        return str(self.rank) + str(self.suit)

class Deck:

    # List of the different values and suits cards can have
    Suit = ["C", "D", "H", "S"]
    Rank = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

    # Create a new deck of 52 cards unshuffled
    def __init__(self):
        self.cardList = []
        for suit in range(len(self.Suit)):
            for rank in range(len(self.Rank)):
                self.cardList.append(Card(self.Rank[rank], self.Suit[suit]))

    # Deal one card to the player
    def dealOne(self, player):
        player.hand.append(self.cardList.pop(0))
        player.handTotal += 1

    # Shuffle the cards
    def shuffle(self):
        random.shuffle(self.cardList)

    # Return a string containing all the cards in the deck in the order they appear
    def __str__(self):
        deck = ""
        for row in range(4):
            for col in range(13):
                deck += '{:>4}'.format(str(self.cardList[row * 13 + col]))
            deck += "\n"
        return deck



class Player:

    # Create a new player
    def __init__(self):
        self.hand = []
        self.handTotal = 0

    # Return whether the player's hand is not empty
    def handNotEmpty(self):
        return self.handTotal != 0

    # Return whether the player's hand in empty
    def handEmpty(self):
        return self.handTotal == 0

    # Remove the top card from the player's deck
    def removeOne(self):
        self.handTotal -= 1
        return self.hand.pop(0)

    # Add one card to the bottom of the player's deck
    def addOne(self, card):
        self.handTotal +=1
        self.hand.append(card)

    # Add multiple cards to the bottom of the player's deck
    def addWarPile(self, warPile):
        self.handTotal += len(warPile)
        self.hand.extend(warPile)

    # Return a string containing the player's hand in the order that they appear
    def __str__(self):
        playerHand = ['{:>3}'.format(str(row)) for row in self.hand]
        playerHand = [playerHand[card: min(card + 13, len(self.hand))] for card in range(0, len(self.hand), 13)]
        for item in playerHand:
            item[0] = '{:>4}'.format(item[0])
        playerHand = [' '.join(row) for row in playerHand]
        return '\n'.join(playerHand)


# Start the game
def playGame(cardDeck, player1, player2):

    # Output the all the players' initial hand
    print("\n")
    print("Initial hands: ")
    print("Player 1: ")
    print(player1)
    print("\n")
    print("Player2: ")
    print(player2)
    print("\n\n")


    round = 1

    # Loop until one player runs out of cards
    while(player1.handNotEmpty() and player2.handNotEmpty()):
        print("ROUND ", '{}'.format(round) + ":")

        # Both players play the top card in their hand
        card1 = player1.removeOne()
        card2 = player2.removeOne()
        print("Player 1 plays: ", card1)
        print("Player 2 plays: ", card2)

        # Determine who wins the current round
        roundWinner(player1, player2, card1, card2, round)

        # Output the updated hand of each player
        print("Player 1 now has", player1.handTotal, "card(s) in hand:")
        print(player1)
        print("Player 2 now has", player2.handTotal, "card(s) in hand:")
        print(player2)
        print("\n")

        # Go to the next round
        round += 1

# Determine who wins the current round
def roundWinner(player1, player2, card1, card2, round):

    # If player 1 wins, then add all played cards to his hand
    if (Card.getRankOrder(card1.rank) > Card.getRankOrder(card2.rank)):
        print("\nPlayer 1 wins round", '{}'.format(round) + ": ", card1 == card2, "\n")
        player1.addOne(card1)
        player1.addOne(card2)

    # If player 2 wins, then add all played cards to his hand
    elif (Card.getRankOrder(card1.rank) < Card.getRankOrder(card2.rank)):
        print("\nPlayer 2 wins round", '{}'.format(round) + ": ", card1 == card2, "\n")
        player2.addOne(card1)
        player2.addOne(card2)

    # Else, war starts
    else:
        print("\nWar starts: ", card1 == card2)
        war(player1, player2, card1, card2, round)



def war(player1, player2, card1, card2, round):

    # Create the war pile
    warPile1 = []
    warPile2 = []
    warPile1.append(card1)
    warPile2.append(card2)

    # Loop until one person has no more cards
    while (player1.handNotEmpty() and player2.handNotEmpty()):

        # Each player puts three cards face down
        for card in range(3):

            # If any players run out of cards, then end war
            if (player1.handEmpty() or player2.handEmpty()):
                break
            faceDown1 = player1.removeOne()
            faceDown2 = player2.removeOne()
            warPile1.append(faceDown1)
            warPile2.append(faceDown2)
            print("Player 1 puts", '{:>3}'.format(str(faceDown1)), "face down")
            print("Player 2 puts", '{:>3}'.format(str(faceDown2)), "face down")

        # If player 1 runs out of cards, then player 2 wins
        if (player1.handEmpty()):
            print("\n")
            player2.addWarPile(warPile1)
            player2.addWarPile(warPile2)
            break

        # If player 2 runs out of cards, then player 1 wins
        if (player2.handEmpty()):
            print("\n")
            player1.addWarPile(warPile1)
            player1.addWarPile(warPile2)
            break

        # Each player puts one card face up
        faceUp1 = player1.removeOne()
        faceUp2 = player2.removeOne()
        warPile1.append(faceUp1)
        warPile2.append(faceUp2)
        print("Player 1 puts", '{:>3}'.format(str(faceUp1)), "face up")
        print("Player 2 puts", '{:>3}'.format(str(faceUp2)), "face up")

        # If player 1 has the higher card on the fourth card, then he wins war
        if (Card.getRankOrder(faceUp1.rank) > Card.getRankOrder(faceUp2.rank)):
            print("\nPlayer 1 wins round", '{}'.format(round) + ": ", faceUp1 == faceUp2, "\n")
            player1.addWarPile(warPile1)
            player1.addWarPile(warPile2)
            break

        # If player 2 has the higher card on the fourth card, then he wins war
        elif (Card.getRankOrder(faceUp1.rank) < Card.getRankOrder(faceUp2.rank)):
            print("\nPlayer 2 wins round", '{}'.format(round) + ": ", faceUp1 == faceUp2, "\n")
            player2.addWarPile(warPile1)
            player2.addWarPile(warPile2)
            break

        # Else, keep playing war until one person wins
        else:
            continue



def main():

    # Create a deck of 52 cards
    cardDeck = Deck()
    print("Initial deck:")

    # Print the deck out
    print(cardDeck)

    # Seed the random number generator
    random.seed(15)

    # Shuffle the deck
    cardDeck.shuffle()
    print("Shuffled deck:")
    print(cardDeck)

    # Create a player
    player1 = Player()
    # Create another player
    player2 = Player()

    # Deal 26 cards to each player, one at a time, alternating between players
    for i in range(26):
        cardDeck.dealOne(player1)
        cardDeck.dealOne(player2)

    # Start the game
    playGame(cardDeck, player1, player2)

    # Determine who wins the game
    if player1.handNotEmpty():
        print("\n\nGame over.  Player 1 wins!")
    else:
        print("\n\nGame over.  Player 2 wins!")

    print("\n\nFinal hands:")
    print("Player 1:   ")

    # Printing a player object should print that player's hand
    print(player1)
    print("\nPlayer 2:")

    # One of these players will have all of the cards, the other none
    print(player2)


main()
