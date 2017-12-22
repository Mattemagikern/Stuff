#!/usr/bin/env python
import random as r
import pprint
from operator import itemgetter

sets = [(1,3),(5,15,20,25),(6,8,9),(11,13,14),(12,28),(16,18,19),(21,23,24),(26,27,29),(31,32,34),(37,39)]
names = [("Old Kent Road","Whitechapel Road"),("King's Cross Station","Marylebone Station","Fenchurch St Station","Liverpool Street Station"),("The Angel Islington","Euston Road","Pentonville Road"),("Pall Mall","Whitehall","Northumberland Avenue"),("Electric Company","Water Works"),("Bow Street","Marlborough Street","Vine Street"),("The Strand","Fleet Street","Trafalgar Square"),("Leicester Square","Coventry Street","Piccadilly"),("Regent Street","Oxford Street","Bond Street"),("Park Lane","Mayfair")]

iterations = 10000000
"""
Simulates a dice throw in monopoly
"""
def dices():
    return r.randint(1, 6) + r.randint(1, 6)
"""
Monopoly walk generator.
Finds which streets you are most likely to land on while playing monopoly.
not compleatly random but enough. 
"""
def generate_places():
    places = {}
    stat_places = {}
    road = 0
    for i in range(40):
        places[i] = 0
    for i in range(iterations):
        road += dices()
        road %= 40
        #Chance cards
        if road in {7,22,36} and r.randint(1,17) < 7:
            sample = r.sample({0,39,24,12,10,11,"train_station", int(road-3)},1)[0]
            if sample == "train_station":
                if road == 7:
                    road = 5
                elif road == 22:
                    road = 25
                elif road == 36:
                    road = 35
            else:
                road = sample
        #Community Chest
        elif road in {2,17,33} and r.randint(1,17) < 2:
            road = r.sample({0,10},1)[0]
        elif road == 30:
            road = 10
        places[road] += 1
    for i in range(len(places)):
        stat_places[i] = places[i] / float(iterations)
    set_places = {}
    for s in sets:
        nbr_set = 0
        for i in s:
            nbr_set += places[i]
        set_places[s] = nbr_set
    for i in set_places:
        set_places[i] /= float(iterations)
    return stat_places, set_places 

def gen_names():
    n = {}
    for s in range(len(sets)):
        n[sets[s]] = names[s]
    return n
"""
values, maximize amount erned by limiting money to 0.75 of start amount. 
"""
def networkflow(set_places):
    pass

name = gen_names()
places, set_places = generate_places()

print "---------------Erly Game----------------------"
start_game = {}
for set in sets:
    for i in range(len(set)):
        start_game[name[set][i]] = places[set[i]]

pprint.pprint(sorted(((v,k) for k,v in start_game.iteritems()), reverse=True))

print "----------------Late Game---------------------"
pprint.pprint(sorted(((v,name[k]) for k,v in set_places.iteritems()), reverse=True))
