#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:10:49 2019

@author: jmcleod
"""

import math

class Point:
    ''' Represents a point in 2-D space'''

blank = Point()

blank.x = 3.0
blank.y = 4.0

print(blank.y)

print('(%d, %d)' % (blank.x,blank.y))

dist = math.sqrt(blank.x**2+blank.y**2)
print(dist)

def print_point(p):
    print('(%d, %d)'%(p.x,p.y))
print_point(blank)
#%%

class Rectangle:
    '''Implements a 2D rectangle
    Attributes: width, length, corner'''
    

box = Rectangle()

box.width = 100
box.height = 200

box.corner = Point()
box.corner.x = 0.0
box.corner.y = 0.0

print(box)

def find_center(rect):
    p=Point()
    p.x = (rect.corner.x + rect.width)/2
    p.y = (rect.corner.y + rect.height)/2
    return(p)

center = find_center(box)
print_point(center)

#%% objects are mutable- we can alter them

#box.width +=50
#box.height +=100

#center = find_center(box)
#print_point(center)
box.width = 100
box.height = 200

def grow_rectangle(rect,dwidth,dheight):
    rect.width+=dwidth
    rect.height+=dheight
    return(rect)

print(box.width, box.height)

grow_rectangle(box,50,100)
print(box.width, box.height)

#%%
import copy

p1 = Point()
p1.x = 3
p1.y = 4

p2  = copy.copy(p1)

print_point(p1)
print_point(p2)

p1 is p2 # objects are not the same
p1.x is p2.x # but defining parameters are


p3 = copy.deepcopy(p1)
p1 is p3
p1.x is p3.x


#%%

class Time:
    """Represents time of day
    attributes: hour, minute, second"""

time = Time()
time.hour = 11
time.minute = 59
time.second = 30

def print_time(t):
    print('%02d : %02d : %02d' % (t.hour,t.minute,t.second))

print_time(time)

def add_time(t1,t2):
    sum = Time()
    sum.hour = t2.hour + t1.hour
    sum.minute = t2.minute + t1.minute
    sum.second = t2.second + t1.second
    
    if sum.second >= 60:
        sum.second -= 60
        sum.minute += 1
    if sum.minute >= 60:
        sum.minute -= 60
        sum.hour +=1
    return(sum)

start = Time()
start.hour = 9
start.minute = 45
start.second = 0

duration = Time()
duration.hour = 1
duration.minute = 35
duration.second = 0

done = add_time(start,duration)
print_time(done)


def increment(time,seconds):
    time.second +=seconds
    
    if time.second >= 60:
        time.second -= 60
        time.minute += 1
    if time.minute >= 60:
        time.minute -= 60
        time.hour +=1
    return(time)

t = Time()
t.hour = 1
t.minute = 30
t.second = 35
print_time(t)
new_t = increment(t,47)
print_time(new_t)

#%%

class Time:
    '''Represents time of day
    Attributes: hour, minute, second'''
    def print_time(self):
        print('%02d : %02d : %02d' % (self.hour, self.minute, self.second))
    def time_to_int(self):
        minutes = self.hour *60 +self.minute
        seconds = minutes * 60 +self.second
        return(seconds)
    def int_to_time(self, seconds):
        time = Time()
        minutes, time.second = divmod(seconds,60)
        time.hour, time.minute = divmod(minutes,60)
        return(time)
    def increment(self, seconds):
        seconds += self.time_to_int()
        return(self.int_to_time(seconds))
    def is_after(self, other):
        return(self.time_to_int()>other.time_to_int())
    def __init__(self,hour=0,minute=0,second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
    def __str__(self):
        return('%02d : %02d : %02d' % (self.hour, self.minute, self.second))
    def __add__(self,other):
        seconds = self.time_to_int() + other.time_to_int()
        return(self.int_to_time(seconds))
        

start = Time()
start.hour = 11
start.minute = 59
start.second = 30

Time.print_time(start)

sec = Time.time_to_int(start)
print(sec)

start2 = Time.int_to_time(Time,sec)
Time.print_time(start2)

start_end = Time.increment(start,300)
Time.print_time(start_end)

print(Time.is_after(start,start_end))


t = Time(9)
t.print_time()

t = Time(9,45)
t.print_time()

t = Time(9,45,37)
t.print_time()


t = Time(hour = 9, second = 37)
t.print_time()

print(t)
q = Time(3,23,14)
print(q+t)


t1 = Time(7,43)
vars(t1)

def print_attributes(obj):
    for attr in vars(obj):
        print(attr, getattr(obj,attr))

print_attributes(t1)

#%%

class Card:
    '''Representing Playing Cards'''
    def __init__(self,suit=0,rank=2):
        self.suit = suit
        self.rank = rank
    suit_names = ['Spades','Diamonds','Clubs','Hearts']
    rank_names = ['2','3','4','5','6','7','8','9'\
                  ,'10','Jack','Queen','King','Ace']
    def __str__(self):
        return('%s of %s' %(Card.rank_names[self.rank], \
                            Card.suit_names[self.suit])) 
    def __lt__(self, other):
        #checking suits
        if self.suit<other.suit: return(True)
        if self.suit>other.suit: return(False)
        return(self.rank<other.rank)
        
        
class Deck:
    '''Implement a standard 52 card deck'''
    def __init__(self):
        self.cards = []
        for suit in range(0,4):
            for rank in range(0,13):
                card = Card(suit,rank)
                self.cards.append(card)

    def pop_card(self):
        return(self.cards.pop())
    def add_card(self, card):
        self.cards.append(card)
    def shuffle(self):
        import random
        random.shuffle(self.cards)
    def sort(self):
        pass
    def move_cards(self,hand,num):
        for i in range(num):
            hand.add_card(self.pop_card())
    def __str__(self):
        res=[]
        for card in self.cards:
            res.append(str(card))
        return('\n'.join(res))

class Hand(Deck):
    '''Implements a hand of cards'''
    def __init__(self,label=''):
        self.cards=[]
        self.label = label

deck1=Deck()
#print(deck1,'\n')
deck2= Deck()
deck2.shuffle()
#print(deck2)

hand1 = Hand('New Hand')
#hand.cards
#hand.label

deck = Deck()
deck.shuffle()

deck.move_cards(hand1,5)


print(hand1,'\n\n',deck)












































