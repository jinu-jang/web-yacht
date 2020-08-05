from typing import List
from random import randint
from collections import Counter

class YachtPlayer:
    def __init__(self) :
        self.state = { 'possible' : [True] * 12,
                       'rollNo' : 0,
                       'curDie' : [0] * 5 }
        self.scores = [-1] * 12
        self.bonusEarned = False

    def currentScore(self) -> int :
        # Bonus points are already included in the scores.
        return sum(self.scores)

    def roll(self, diceIndices: List) -> List:
        """
        Roll specified dices.

        Parameter
        ---------
            indices (List): The specific dices that will be rolled.
                            A number above 4 or any passed in elements after
                            the 5th one will be ignored.

        Return
        ------
            (List): The current state of the dices will be returned.
                    This will always be a size 5 list, and will be equivalent to
                    self.state['curDie']
        """
        if self.state['rollNo'] == 0 :
            # Initial roll. Always roll all 5.
            for i in range(5):
                self.state['curDie'][i] = randint(1, 6)
            self.state['rollNo'] = 1

        elif self.state['rollNo'] == 1 or self.state['rollNo'] == 2 :
            # Only reroll the dices the user chooses.
            for i in diceIndices[:5]:
                if i < 5:
                    self.state['rollNo'][i] = randint(1, 6)

        self.state['curDie'] = sorted(self.state['curDie'])
        return self.state['curDie']

    def recordHand(self, scoringCategory : int) -> int:
        """
        Record the score of the current hand as a certain category.
        Parameter
        ---------
            scoringCategory (int):

        Return
        ------
            (int): The score earned from doing this move.
        """
        score = 0

        # Basic ones, twos, ... , sixes
        # Calculated by adding all of the selected number
        if scoringCategory < 6:
            selectedNum = scoringCategory + 1
            for i in self.state['curDie']:
                if i == selectedNum:
                    score += i

            # Check if you get the bonus
            # If you get over 63 points from the basic 6,
            # there's a 35 point bonus
            if not self.bonusEarned:
                temp = 0
                for i in self.state['curDie'][:6]:
                    if i > 0:
                        temp += i
                if temp > 63:
                    self.bonusEarned = True
                    score += 35

        # The rest of these follow a specific scoring scheme
        # Index 6 : Player choice. A sum of all dices.
        elif scoringCategory == 6:
            score = sum(self.state['curDie'])

        # Index 7 : Full House. A sum of all dices.
        # Can ony be a full house when there's a 3 of a kind and a different pair.
        elif scoringCategory == 7:
            counts = Counter(self.state['curDie'])
            if max(counts.values()) == 3 and min(counts.values()) == 2:
                score = sum(self.state['curDie'])
            else:
                score = 0

        # Index 8 : Four of a Kind. A sum of all dices.
        # Has at least 4 of a certain number.
        elif scoringCategory == 8:
            counts = Counter(self.state['curDie'])
            if max(counts.values()) >= 4:
                score = sum(self.state['curDie'])
            else:
                score = 0

        # Index 9 : Small Straight. 15 points.
        # 4 out of 5 dices form a straight.
        elif scoringCategory == 9:
            sortedDices = sorted(self.state['curDie'])
            straight = False

            for i, dice in enum(sortedDices[:4]):
                if dice != i + sortedDices[0]:
                    straight = False
                    break
                straight = True
            if not straight:
                for i, dice in enum(sortedDices[1:]):
                    if dice != i + sortedDices[1]:
                        straight = False
                        break
                    straight = True

            if straight:
                score = 15
            else:
                score = 0

        # Index 10 : Large Straight. 30 points.
        # All 5 out of 5 dices form a straight.
        elif scoringCategory == 10:
            sortedDices = sorted(self.state['curDie'])
            for i, dice in enum(sortedDices):
                if dice != i + sortedDices[0]:
                    straight = False
                    break
                straight = True

            if straight:
                score = 30
            else:
                score = 0

        # Index 11 : Yacht. 50 points.
        # All 5 dices are the same.
        elif scoringCategory == 11:
            if len(set(self.state['curDie'])) == 1:
                score = 50

        self.scores[scoringCategory] = score
        self.state['possible'][scoringCategory] = False
        self.state['rollNo'] = 0
        return score
