from entities.hand import Hands, Hand

class Player():

    counter = 0

    def __init__(self):
        self.cards = [None] * 2
        self.chance = 0
        self.ties = 0
        self.wins = 0
        self.hands = {}
        self.id = Player.counter
        Player.counter += 1

    def toString(self):
        return f"Id: {self.id}, wins: {str(self.wins)}, tie chance: {str(self.ties)} Cards: [{self.cards[0].toShortString()}, {self.cards[1].toShortString()}]"

    def handsToString(self):
        out = ''
        newline = ''
        for key, val in self.hands.items():
            out += newline + key.name + ': ' + str(val)
            newline = '\n'

        return out
