from Entities.Suits import Suits
from Entities.Card import Card
from Entities.Player import Player
from Entities.Hand import handEnum

class PokerStatter():
    
    visibleCards = []

    allCardsDict = {}
    remainCardsDict = {}
    audienceCards = []

    def getHighestCurrentHand(self):
        return handEnum.default
    
    def genChancePerPlayer(self, allCardsDict, players):

        chancesPerPlayer = {}
        audienceCards = []

        for key in allCardsDict:
            audienceCards = audienceCards + allCardsDict[key]

        remainCardsDict = self.retrieveRemainingCards(audienceCards)
        
        self.allCardsDict = allCardsDict
        self.remainCardsDict = remainCardsDict
        self.audienceCards = audienceCards

        currentHighestHand = handEnum.default

        for p in players:
            if p.currentHighestHand.value > currentHighestHand.value:
                currentHighestHand = p.currentHighestHand
            

        for p in players:
            p.handsToCheck = self.getHandsToCheck(p, currentHighestHand) # this will need to be filtered by what is above the currentHighestHand
            

        return chancesPerPlayer

    def getHandsToCheck(self, player, currentHighestHand):
        possibleHands = self.getPossibleHands(player)

        handsToCheck = {}

        for h, c in possibleHands:
            if handEnum[h] > handEnum[currentHighestHand]:
                
                

        return handsToCheck



    def getPossibleHands(self, player):

        possibleHands = {}

        player.handChances = self.getHandChances(player)

        for h, c in player.handChances.items():
            #Possible outcomes
            # 1 - player hit hand - need to check his currentHighestHand
            # % - some percent chance of player getting that card
            # 0 - player cannot hit 

            if c != 0:
                possibleHands[h] = c

        return possibleHands

    def getHandChances(self, player):

        chancesPerHand = {
            "onePair" : self.chanceOfOnePair(player)
            #handEnum[3] : self.chanceOfTwoPair
            #handEnum[4] : self.chanceOfTrips
            #handEnum[5] : self.chanceOfStraight
            #handEnum[6] : self.chanceOfFlush
            #handEnum[7] : self.chanceOfFullHouse
            #handEnum[8] : self.chanceOfQuads
            #handEnum[9] : self.chanceOfStraightFlush
        }

        return chancesPerHand
    
    def chanceOfOnePair(self, player):
                              
        totalChance = 0 

        remainingCardsCount = float(52 - len(self.audienceCards))

        onePairReqirementsForPlayer = self.genRequiredCards(self.allCardsDict["TableCards"] + self.allCardsDict[player.Id])

        if len(onePairReqirementsForPlayer) == 0:
            # player has hit one pair
            return 1

        for c in onePairReqirementsForPlayer:
            totalChance += self.chanceOfGettingCard(remainingCardsCount, self.remainCardsDict[c.value])

        return  totalChance
        
    def retrieveRemainingCards(self, visibleCards):
        occurencesPerCard = self.getOccurencesPerCard(visibleCards)
        remaining = {}

        for i in range(13):
            if (i+1) in occurencesPerCard:
                remaining[i+1] = 4 - occurencesPerCard[i+1]
            else:
                remaining[i+1] = 4

        print("\nRemaining cards: " + str(remaining))

        return remaining

    def getOccurencesPerCard(self, visibleCards):
        tempDict = {}

        for c in visibleCards:
            if c.value in tempDict:
                tempDict[c.value] = tempDict[c.value] + 1 
            else:
                tempDict[c.value] = 1

        return tempDict

    def chanceOfGettingCard(self, cardCount, cardsLeft):
        return float(cardsLeft/cardCount)

    def genRequiredCards(self, visibleCards):

        _onePairReq = self.checkFor1Pair(visibleCards)

        return _onePairReq

    def checkFor1Pair(self,visibleCards):

        cardsOut = []
        
        for c in visibleCards:
            for v in visibleCards:
                if (c.value == v.value) and (c.suit == v.suit):
                    #skip if the same card
                    continue
                elif c.value == v.value:
                    #Found 1 pair - return 0 required cards
                    return []
                    
            cardsOut.append(Card(-1, c.value, Suits.Undefined))

        return cardsOut

        # do this line per player
        # only pass in cards for each player at a time
        # do this by passing in a dict to this method, that contains 
        # player 1 cards, players2 cards, and all table cards. Then use 
        # that to pass player ones visible cards to the method to determind 
        # his potention chance of getting what he needs
