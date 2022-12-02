## Day 2 - Elf Rock Paper Scissors (with a hint)
# Today's challenge is to calculate what your total score would be based on a set of scoring rules if you have been provided all the moves your opponent
# will make and the moves you should make to give the appearance of fair play. >:)

# Input is in the form:
# A Y
# B X
# C Z
#
# Where each line is two symbols sparated by a space and each symbol represents a move:
# A - Rock
# B - Paper
# C - Scissors
# X - Rock
# Y - Paper
# Z - Scissors

# Scoring is thus:
# Points for shape + round outcome = round score
# 1 for Rock
# 2 for Paper
# 3 for Scissors
# 0 for loss
# 3 for draw
# 6 for win
# ex. If you win a round with Rock, then your score is: 1 (rock) + 6 (win) = 7

import fileinput
import os
from enum import Enum
from functools import reduce

# define the scoring table of moves / wins
class Scoring(Enum):
    Rock = 1
    Paper = 2
    Scissors = 3
    Win = 6
    Draw = 3
    Loss = 0
    
class Names(Enum):
    A = 'Rock'
    B = 'Paper'
    C = 'Scissors'
    X = 'Rock'
    Y = 'Paper'
    Z = 'Scissors'
    win = 'Win'
    draw = 'Draw'
    loss = 'Loss'
    
class DesiredOutcome(Enum):
    X = 'Loss'
    Y = 'Draw'
    Z = 'Win'

# given: desired outcome (enum), look up the desired play (value), by the opponent's play (key)
class DesiredPlay(Enum):
    Win = {Names.A.value:Names.B.value, Names.B.value:Names.C.value, Names.C.value:Names.A.value}
    Loss = {Names.A.value:Names.C.value, Names.B.value:Names.A.value, Names.C.value:Names.B.value}
    Draw = {Names.A.value:Names.A.value, Names.B.value:Names.B.value, Names.C.value:Names.C.value}
    
class Token:
    def __init__(self, symbol):
        self.symbol = symbol
        self.name = Names[self.symbol].value
        self.value = Scoring[self.name].value

    def __str__(self):
        return f'{self.symbol}: "{self.name}", {self.value}'

class Result:
    def __init__(self, outcomeToken, score):
        self.name = outcomeToken.name
        self.score = score
        
    def __str__(self):
        return f'{self.score} ({self.name})'
    
# define a Round object to hold the move/countermove and outcome
class Round:
    def __init__(self, move: Token, countermove: Token):
        self.move = move
        self.countermove = countermove
        
        # determine win/loss/draw based on the move values
        # include check for the special cases: Rock (1) beats Scissors (3)
        if (countermove.name == 'Rock' or move.name == 'Rock') and (countermove.name == 'Scissors' or move.name == 'Scissors') and countermove.name != move.name:
            if (countermove.name == 'Rock' and move.name == 'Scissors'):
                winToken = Token('win')
                score = winToken.value + countermove.value
                self.outcome = Result(winToken, score)
            else:
                lossToken = Token('loss')
                score = lossToken.value + countermove.value
                self.outcome = Result(lossToken, score)
        elif countermove.value > move.value:
            winToken = Token('win')
            score = winToken.value + countermove.value
            self.outcome = Result(winToken, score)
        elif countermove.value < move.value:
            lossToken = Token('loss')
            score = lossToken.value + countermove.value
            self.outcome = Result(lossToken, score)
        else:
            drawToken = Token('draw')
            score = drawToken.value + countermove.value
            self.outcome = Result(drawToken, score)
    
    def __str__(self):
        return f'{{move: {{{self.move}}}, countermove: {{{self.countermove}}}, score: {self.outcome}}}'

    def __repr__(self):
        return f'{self.move},{self.countermove},{self.outcome}'

# interrim testing to verify basic gameplay results in the correct win/loss/draw outcome
# testRound1 = Round(Token('A'), Token('A'))
# testRound2 = Round(Token('A'), Token('B'))
# testRound3 = Round(Token('A'), Token('C'))
# testRound4 = Round(Token('B'), Token('A'))
# testRound5 = Round(Token('B'), Token('B'))
# testRound6 = Round(Token('B'), Token('C'))
# testRound7 = Round(Token('C'), Token('A'))
# testRound8 = Round(Token('C'), Token('B'))
# testRound9 = Round(Token('C'), Token('C'))
# print(f'Test round: {testRound1}')
# print(f'Test round: {testRound2}')
# print(f'Test round: {testRound3}')
# print(f'Test round: {testRound4}')
# print(f'Test round: {testRound5}')
# print(f'Test round: {testRound6}')
# print(f'Test round: {testRound7}')
# print(f'Test round: {testRound8}')
# print(f'Test round: {testRound9}')

# read the file as Round objects into the rounds array
rounds = []
print(os.getcwd())
for line in fileinput.input('input.txt'):
    (m, c) = line.strip().split(' ')
    rounds.append(Round(Token(m), Token(c)))
    
print(f'Rounds played: {len(rounds)}')

# now calculate the total score for the entire game
totalScore = 0
# This is more complicated, but basically we're going to take the Result object's score from each round in the list and create a new list of scores
# (lambda round: round.outcome.score)
# Then we'll reduce that list of scores down to a single score by adding each element together (lambda x,y: x + y)
print(f"Total score: {reduce(lambda x, y: x + y, list(map(lambda round: round.outcome.score, rounds)))}")

# oops! second column isn't a countermove, it's the desired outcome (X -> lose, Y -> draw, Z -> win), so assuming we select the desired outcome, what's our total score?

# run through each round, ignoring score and produce a new list of scores based on the new definition of 'countermove'
def manipulate_score(round: Round):
    #print(f"round: {round}, desiredOutcome: {DesiredOutcome[round.countermove.symbol].value}")

    # we want the score of the _desired_ outcome, not the original meaning of 'countermove'
    outcomeValue = Scoring[DesiredOutcome[round.countermove.symbol].value].value
    #print(f'desired outcome: {DesiredOutcome[round.countermove.symbol].value}')
    
    # don't forget we also need the value of the desired play to acheive the outcome - inverse of the round score
    desiredPlay = DesiredPlay[DesiredOutcome[round.countermove.symbol].value].value[round.move.name]

    #print(f'desiredPlay: {str(desiredPlay)}')
    #print(f'desiredPlay score: {Scoring[desiredPlay].value}')
    return outcomeValue + Scoring[desiredPlay].value
    
#print(f'list of manipulated scores: {list(map(lambda round: manipulate_score(round), rounds[0:2]))}')
print(f"Total score (manipulating outcomes): {reduce(lambda x, y: x + y, list(map(lambda round: manipulate_score(round), rounds)))}")