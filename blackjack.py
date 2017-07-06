
# coding: utf-8

# In[ ]:

import random

def cards_start():
    #using a dict instead of list so I can reference the card name directly instead of having to find
    #its place in the list with list.index(card)... and because I started out using a dict because
    #I wanted practice with them.
    return {'ace': [4, 11], 'two': [4, 2], 'three': [4, 3], 'four': [4, 4],
            'five': [4, 5], 'six': [4, 6], 'seven': [4, 7], 'eight': [4, 8],
            'nine': [4, 9], 'ten': [4, 10], 'jack': [4, 10], 'queen': [4, 10],
            'king': [4, 10]}

def tally(item):
    print(player_dict[item].name, player_dict[item].points, ':', player_dict[item].hand)

class Deck_class(object):
    
    def __init__(self):
        self.cards_left = cards_start()
    
    def deal(self):
        # create a list of all the individual cards left and choose one randomly from that list
        all_cards_left = []
        for key in self.cards_left.keys():
            for val in range(self.cards_left[key][0]):
                all_cards_left.append(key)
        card = random.choice(all_cards_left)
            
        self.cards_left[card][0] -= 1
        if self.cards_left[card][0] < 1:
            self.cards_left.pop(card)
        
        if len(self.cards_left) == 0:
            self.cards_left = cards_start()
            print('Deck ran out of cards so a new deck has been started.')
        
        #finding the point for the card to return from cards_start() instead of self.cards_left as
        #the card in self.cards_left may have been deleted just after it was drawn
        return (card, cards_start()[card][1])
    
    
class Player_class(object):
        
    def __init__(self, name):
        self.points = 0
        self.hand = []
        self.bust = False
        self.hit = True
        self.ace_count = 0
        self.name = name
        
    
    def add_to_hand(self, card, points):
        self.hand.append(card)
        
        if card == 'ace':
            self.ace_count += 1
        
        self.points += points
        
        if self.points == 21:
            self.hit = False
        if self.points > 21:
            if self.ace_count > 0:
                self.points -= 10
                self.ace_count -= 1
            else:
                self.bust = True
                self.hit = False
        
        #check for 21 after any potential ace changes to stop
        #a player hitting again.
        if self.points == 21:
            self.hit = False
        
        

print('Welcome to Blackjack! \nNew game started.')
while True:
    try:
        p_count = int(input('How many players are there? (1-5 allowed)'))
        if p_count in range(1,6):
            break
        else:
            print('You must enter a digit between 1 and 5')
        
    except:
         print('You must enter a digit between 1 and 5')             

deck = Deck_class()

#start a dict with the dealer then add the amount of players needed
#will be used later to create
player_list = ['d']
for p in range(1, p_count + 1):
    player_list.append('p' + str(p))

player_dict = {}
for item in player_list:
    player_dict[item] = Player_class(item)

    
while True:
    #initialise values before loop for dealing out cards
    hit_again = len(player_list)
    for item in player_list:
        player_dict[item].hit = True
        player_dict[item].bust = False
        player_dict[item].hand = []
        player_dict[item].points = 0
        player_dict[item].ace_count = 0
    
    #deal initial two cards
    for n in (1, 2):
        for item in player_list:
            player_dict[item].add_to_hand(*deck.deal()) #*asterisk unpacks the tuple
    
    #print initial hands and tell any players if they got blackjack
    for item in player_list:
        if item.lower().startswith('d'):
            dhand = [player_dict[item].hand[0], 'hole card']
            print(player_dict[item].name, ':', dhand)
        else:
            tally(item)
            if player_dict[item].points == 21:
                print('!!! Congrats', player_dict[item].name, 'you got Blackjack! You win!!!')
                
    #check if dealer has blackjack
    if player_dict['d'].hand[0].lower() in ('ace', 'ten', 'jack', 'queen', 'king'):
        print('Checking if dealer has blackjack...')
        if player_dict['d'].points == 21:
            print('Dealer has Blackjack!')
            print("Sorry anyone who doens't already have 21. This hand is over and no more cards will be dealt")

        else:
            print("... Dealer doesn't have blackjack.")
    
    #loop that does hits
    for n in range(1, len(player_list) + 1):
        #do dealer last 
        if n >= len(player_list):
            n = 0

        item = player_list[n]
        while player_dict[item].hit:
            if n == 0 and player_dict[item].points < 17:
                player_dict[item].add_to_hand(*deck.deal()) #*asterisk unpacks the tuple
                tally(item)
                if player_dict[item].bust:
                    print('The dealer went bust!')

            elif n != 0 and input(player_dict[item].name + ' want to hit (y/n)?').lower().startswith('y'):
                player_dict[item].add_to_hand(*deck.deal()) #*asterisk unpacks the tuple
                tally(item)
                if player_dict[item].bust:
                    print('Sorry, you gone bust! Your turn is over.')

            else:
                player_dict[item].hit = False

            if player_dict[item].points == 21:
                print('Congrats', player_dict[item].name, "you hit 21. You can't hit again now.")
    
    #say who won and lost
    print('_________________________')
    print('_________________________')
    print('The hand is over. \nThe results are...')
    print('-------------------------')
    if player_dict['d'].bust:
        print('The dealer went bust')
    else:
        print('The dealer got', player_dict['d'].points)
    
    for n in range(1, len(player_list)):
        print('-------------------------')
        
        item = player_list[n]
        if player_dict[item].bust:
            print(player_dict[item].name, "went bust. You didn't win anything, sorry.")
        else:
            print(player_dict[item].name, 'got', player_dict[item].points)
            if player_dict['d'].bust:
                print('The dealer went bust so you win!')
            elif player_dict[item].points > player_dict['d'].points:
                print("That's more than the dealer so you won!")
            elif player_dict[item].points == player_dict['d'].points:
                print("That's the same as the dealer so you've drawn")
            else:
                print("That's not as good as the dealer so you lost, sorry!")


    if not input('Want to play another hand?').lower().startswith('y'):
        print('Exiting game...\nBye!')
        break
    
    #if playing another hand print two lines to make it look nicer
    print('_________________________')
    print('_________________________')

