#-------------------------------------------------------------------------------
# Name:		kevinli_cpt_assignment.py
# Purpose:		A role-playing interactive game for ICS3U1 course
#
# Author:		Li.K
#
# Created:		18/06/2016
#------------------------------------------------------------------------------
"""
Features of the game:
1. Functional Save/Load system                         Compatible for first time playing, saving important progress
2. Functional Shopping system                          Allows player to sell/buy loots
3. Functional Currency system                          Player can use earn/spend gold
4. Functional Combat system                            Player can engage in combat in certain areas
5. Functional Inventory system                         Player can store monster's loots in their inventory
6. Interactive lore and story-line                     A rpg experience
7. Somewhat Functional Cooking system                  Allows player to bake
8. Uses 70% of the rooms                               Medium-sized world map for player to explore
9. Command list in main menu                           Inexperienced player support for unfamiliar commands
10.Player stats                                        Allow player to gain experience and level up
11.Player equipments                                   Allow player to wield (a sword for time being)
12.Bug-less                                            80% of the bugs/errors were abled to be ironed out
"""


import random


str_form = '*' * 3
#Mapping of the game
room_list = []
room = ["Forest: You're in the chilling woods.", None, None, 3, None]
room_list.append(room)
room = ["Kitchen: Suppose cooking could be done here...", 0, 2, 5, None]
room_list.append(room)
room = ["Mansion: An abandoned mansion, crumbled and dusty.", 0, 3, 5, 1]
room_list.append(room)
room = ["Road: Dull and bumpy.", 0, 4, 6, 2]
room_list.append(room)
room = ["Weapon Smith: Commonwares, sharp edges lie here.", 0, None, 7, 3]
room_list.append(room)
room = ["Wheat Farm: S-wheat.", 2, 6, 8, None]
room_list.append(room)
room = ["Road: Traders seldom pass by here.", 3, 7, 9, 5]
room_list.append(room)
room = ["Butchery: Finest steak's origin.", 4, None, 10, 6]
room_list.append(room)
room = ["Spice Field: Spicey.", 5, 9, 11, None]
room_list.append(room)
room = ["Road: More civilization appears.", 6, 10, 12, 8]
room_list.append(room)
room = ["Windmill: Less labour work for the cows.", 7, None, 13, 9]
room_list.append(room)
room = ["Animal Farm: 'Moooooo'", 8, 12, None, None]
room_list.append(room)
room = ["Road: This road is crowded. Better walk along.", 9, 13, None, 11]
room_list.append(room)
room = ["General Store: Trade your things", 10, None, None, 12]
room_list.append(room)


#Inventory and money pouch
inventory = []
moneypouch = 1000


#Stats, lvl/exp/equipment bonus
attack = [1, 0, 0]
hitpoint = [1, 0, 0]
cooking = [1, 0, 0]


#Monster list [name, health, atk, loots, chance]
mon_list = []
mons = ['Cow', 5, 1, ['Cow Leather', 'Cow Meat'], 90]
mon_list.append(mons)
killcount = 0


#Opponent Interaction
opp_styles = []
atk_style = 'Attack'
opp_styles.append(atk_style)
flee_style = 'Flee'
opp_styles.append(flee_style)


#Quest
quest_list = []
#1. Kill cows
quest = ['1. Kill 5 monsters', 'You can start off by killing some cows in the field!', 0]
quest_list.append(quest)
#2. Sell items
quest = ['2. Sell a cow meat', 'You got some goods, now sell it!', 0]
quest_list.append(quest)
#3. Pick wheat
quest = ['3. Pick 10 wheats', 'Wheats are great ingredients...Now where do we find them', 0]
quest_list.append(quest)
#4. Grind wheat
quest = ['4. Make flour', 'Use that sweet wheat to make some flour', 0]
quest_list.append(quest)
#5. Make bread
quest = ['5. Make a loaf of bread', 'Bread requires wheat', 0]
quest_list.append(quest)
#6. Find the secret dungeon
quest = ["6. Find the Demon's lair", "Avenge your family!", 0]
quest_list.append(quest)
#7. Find Kayeffsee
quest = ["7. Defeat the Demon", "Oh better grind cows a little bit and get a sword", 0]
quest_list.append(quest)


#Store
shop = []
item = ['Cow Leather', 100, 5]
shop.append(item)
item = ['Cow Meat', 30, 2]
shop.append(item)


#Weapon Smith
weapon_shop = []
item = ['Sword', 100, 10]
weapon_shop.append(item)


#Wheatstack 
wheatstack = 0


#Boss room unlocked variable
unlocked = False


#current_room global variable
current_room = 0


#Basic walking function
def walk():
    global current_room, unlocked
    #Location Events > fn
    def checkroom(room):
        if room == 11:
            if action.lower() == 'fight' or action.lower() == 'kill':
                combat(11) 
                current_room = 11
                done = False
            else:
                done = False
        elif room == 14:
            if action.lower() == 'fight' or action.lower() == 'kill':
                combat(14)
                current_room = 14
                done = False
            else:
                done = False
        elif room == 13:
            if action.lower() == 'sell' or action.lower() == 'store' or action.lower() == 'buy':
                store()
                current_room = 13
                done = False
        elif room == 4:
            if action.lower() == 'sell' or action.lower() == 'store' or action.lower() == 'buy':
                store()
                current_room = 4
                done = False
            
        elif room == 5:
            if action.lower() == 'farm' or action.lower() == 'pick' or action.lower() == 'harvest':
                pickwheat()
                done = False
        elif room == 10:
            if action.lower() == 'grind':
                windmill()
                done = False
        elif room == 1:
            if action.lower() == 'bake' or action.lower() == 'cook':
                cook()
                done = False


    done = False
    action = ''
    while done != True:
        done = True
        checkroom(current_room)
        
        #Completes the quest by unlocking the last room
        if current_room == 14 and quest_list[5][2] == 0:
            quest_list[5][2] = 1
            print "You've completed a quest!"
            
        #Notifies player that they completed all requirements for the boss
        if quest_list[0][2] == 1 and quest_list[1][2] == 1 and quest_list[2][2] == 1 and quest_list[3][2] == 1 and quest_list[4][2] == 1 and unlocked == False:
            room_list[0][1] = 14
            room = ["Devil's Lair: The Demon that slaughtered your whole village", None, None, 0, None]
            room_list.append(room)            
            print "You've unlocked the Devil's Lair, north of the Forest"
            mons = ['Demon', 200, 5, ['Sword', 'Demon Horn'], 20]
            mon_list.append(mons)
            unlocked = True
            
        #North        
        print '*' * 3, room_list[current_room][0], '*' * 3
        action = raw_input("What thee going to doth: ")


        if action.lower() == 'north' or action.lower() == 'n':
            next_room = room_list[current_room][1]
            if next_room == None:
                print str_form, "Thy shan't pass this way.", str_form
                done = False
                continue
            else:
                current_room = next_room
                done = False
        #East
        elif action.lower() == 'east' or action.lower() == 'e':
            next_room = room_list[current_room][2]
            if next_room == None:
                print str_form, "Thy shan't pass this way.", str_form
                done = False
                continue
            else:
                current_room = next_room
                done = False


        #South
        elif action.lower() == 'south' or action.lower() == 's':
            next_room = room_list[current_room][3]
            if next_room == None:
                print str_form, "Thy shan't pass this way.", str_form
                done = False
                continue
            else:
                current_room = next_room
                done = False   
        #West
        elif action.lower() == 'west' or action.lower() == 'w':
            next_room = room_list[current_room][4]
            if next_room == None:
                print str_form, "Thy shan't pass this way.", str_form
                done = False
                continue
            else:
                current_room = next_room
                done = False
        #Quest and requirements
        elif action.lower() == 'quest' or action.lower() == 'quests':
            quests()
            done = False




        #Show inventory
        elif action.lower() == 'inventory':
            show_inventory()
            done = False
        #Show stats
        elif action.lower() == 'stats' or action.lower() == 'stat':
            print "Attack Level: {0:0}|Hitpoint Level: {1:0}".format(attack[0], hitpoint[0])
            print "Cooking Level: {0:0}".format(cooking[0])
            done = False
            
        #Quiting/saving
        elif action.lower() == 'quit':
            gamesave = open("gamesave.txt", 'w')
            save()
            main()
            done = True




        #ignore, replaced with checkroom function so 'else' would not trigger
        elif action.lower() == 'kill' or action.lower() == 'fight' or action.lower() == 'sell' or action.lower() == 'bake' or action.lower() == 'cook' or action.lower() == 'store' or action.lower() == 'buy' or action.lower() == 'farm' or action.lower() == 'pick' or action.lower() == 'harvest' or action.lower() == 'grind':
            done = False


        else:
            print str_form, 'Thee cannot doth that', str_form              
            done = False
def load():
    global current_room, moneypouch, inventory, quest_list, attack, hitpoint, cooking
    #Loading savefile, if gamesave.txt does not exist, all variables set with default value
    try:
        game_load = open('gamesave.txt', 'r')
    except IOError:
        game_load = open('gamesave.txt', 'w+')
    try:
        current_room = int(game_load.readline().strip('\n'))
    except ValueError:
        current_room = 0
    try:
        moneypouch = int(game_load.readline().strip('\n'))
    except ValueError:
        moneypouch = 0
    inventory = game_load.readline().strip('\n').strip("[']").split(',')
    if inventory[-1] == '':
        inventory.pop(-1)
    try:
        quest_list[0][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[0][2] = 0
    try:
        quest_list[1][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[1][2] = 0
    try:
        quest_list[2][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[2][2] = 0        
    try:
        quest_list[3][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[3][2] = 0        
    try:
        quest_list[4][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[4][2] = 0 
    try:
        quest_list[5][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[5][2] = 0    
    try:
        quest_list[6][2] = int(game_load.readline().strip('\n'))
    except ValueError:
        quest_list[6][2] = 0                            
    
    #Stats loading    
    attack_load = game_load.readline().strip('\n')
    try:
        attack[0] = int(attack_load)
    except ValueError:
        attack[0] = 1
        
    hitpoint_load = game_load.readline().strip('\n')
    try:
        hitpoint[0] = int(hitpoint_load)
    except ValueError:
        hitpoint[0] = 1
        
    cooking_load = game_load.readline().strip('\n')
    try:
        cooking[0] = int(cooking_load)
    except ValueError:
        cooking[0] = 1
    game_load.close()
    
#Store function
def store():
    global moneypouch, inventory
    sellcowquest = 0
    #Checks which one of the two shops they're in
    if current_room == 13:
        prompt_ask = raw_input("I ain't got time fo yo bizness, make it quick! (buy/sell/leave/sell all)")
        if prompt_ask.lower() == 'sell':
            sold = False
            while sold != True:
                for i in range(len(inventory)):
                    for j in range(len(shop)):
                        if inventory[i] == shop[j][0]:
                            sell_value = shop[j][2]
                            item = inventory[i]
                            print "Ya sellin that {0} for {1}? (y/n)".format(item, sell_value)
                            prompt_sell = raw_input("Sell?")
                            if prompt_sell.lower() == 'y':
                                sold = True
                                moneypouch += sell_value
                                inventory.remove(item)
                                print inventory                                
                                print "You've gained {0:0}g in that gold pouch of yours!".format(sell_value)
                                if item == 'Cow Meat' and sellcowquest == 0 and quest_list[1][2] == 0:
                                    quest_list[1][2] = 1
                                    sellcowquest = 1
                                    print "You've completed a quest!"
                                return
                            elif prompt_sell.lower() == 'n':
                                print "Get out of my shop if you got no bizness!"
                                sold = True
                                break
                            else:
                                print "You mind speaking properly? You filthy mentally disabled individual!"
                        elif inventory[i] == "Stack of Wheat" or inventory[i] == "Bag of Flour":
                            sold = True
        #Sell all
        elif prompt_ask.lower() == 'sell all':
            threshhold = 0
            sellables = ['Cow Meat', 'Cow Leather']
            for i in range(len(inventory)):
                    for j in range(len(shop)):
                        if inventory[i] == shop[j][0]:
                            sell_value = shop[j][2]
                            item = inventory[i]
                            threshhold += sell_value
            print "Do you wish to sell all for", threshhold, 'g?'
            prompt_sell = raw_input("Sell?")
            if prompt_sell == 'y':
                for i in inventory:
                    if i in sellables:
                        inventory.remove(i)
                moneypouch += threshhold
                
                        
        elif prompt_ask.lower() == 'buy':
            print "Nothing!"
                
    elif current_room == 4:     
        prompt_ask = raw_input("Welcome to the smith! (buy/sell/leave)")
        if prompt_ask.lower() == 'sell':
            for i in range(len(inventory)):
                for j in range(len(weapon_shop)):
                    if inventory[i] == weapon_shop[j][0]:
                        sell_value = weapon_shop[j][2]
                        item = inventory[i]
                        print "Do you want to sell {0} for {1}? (y/n)".format(item, sell_value)
                        sold = False
                        while sold != True:
                            prompt_sell = raw_input("Sell?")
                            if prompt_sell.lower() == 'y':
                                print "You've gained {0:0}g in that gold pouch of yours!".format(sell_value)
                                moneypouch += sell_value
                                sold = True


                            elif prompt_sell.lower() == 'n':
                                print "Get outta my shop you urchin!"
                                sold = True
                            else:
                                print "Didn't quite catch what you were saying..."
                                sold = False        
        elif prompt_ask.lower() == 'buy':
            for x in range(len(shop)-1):
                #item = ['Sword', 1000, 50]
                print "{0}. {1} for {2}g".format(x+1 ,weapon_shop[x][0], weapon_shop[x][1])
                itembuy = input("Which item you want to buy?")
                confirm = raw_input("Confirm? (y/n):")
                if moneypouch >= weapon_shop[itembuy-1][1]:
                    if confirm.lower() == 'y':
                        moneypouch -= weapon_shop[itembuy-1][1]
                        inventory.append(weapon_shop[itembuy-1][0])
                        print "You've successfully purchased {0}!".format(weapon_shop[itembuy-1][0])
                        done = False
                elif confirm.lower() == 'n':
                    print "Get outta my shop fam."
                    done = False
                elif moneypouch < weapon_shop[itembuy-1][1]:
                    print "You ain't got money fam!"
                else:
                    print "Nah fam cant quite hear what yu sayin homie."
    elif prompt_ask.lower() == 'leave':
        done = False
    else:
        done = False       
        
#Quest function, displays quests and their status
def quests():
    queststate = False
    while queststate != True:    
        print str_form, 'Quests', str_form
        for i in range(len(quest_list)):
            if quest_list[i][2] == 1:
                print quest_list[i][0], '{0:>30}'.format('***DONE***')
            if quest_list[i][2] == 0:
                print quest_list[i][0]
        print "{0:0}.".format(i+2), 'Continue'


        choice = input("Enter your command: ")
        if choice == 1:
            print 'Quest Info:', quest_list[0][1]
        elif choice == 2:
            print 'Quest Info:',quest_list[1][1]
        elif choice == 3:
            print 'Quest Info:',quest_list[2][1]
        elif choice == 4:
            print 'Quest Info:',quest_list[3][1]
        elif choice == 5:
            print 'Quest Info:',quest_list[4][1]
        elif choice == 6:
            print 'Quest Info:',quest_list[5][1]
        elif choice == 7:
            print 'Quest Info:',quest_list[6][1]
        elif choice == 8:
            queststate = True
            
#Allows user to pick wheat in "Wheat Farm"
def pickwheat():
    global wheatstack
    wheatstack += 1
    print "You've picked a wheat ({0}/10)".format(wheatstack)
    #For 10 wheats, a stack of wheat would be generated
    if wheatstack == 10:
        inventory.append('Stack of Wheat')
        wheatstack = 0
        print "You've gained a stack of wheat!"
        if quest_list[2][2] == 0:
            quest_list[2][2] = 1
            print "You've completed a quest!"
            
#Allows user to grind wheat in "Windmill"
def windmill():
    #Finds stack of wheat in inventory
    for i in range(len(inventory)):
        if inventory[i] == "Stack of Wheat":
            if quest_list[3][2] == 0:
                quest_list[3][2] = 1
                print "You've completed a quest!"
            #remove stack of wheat and append bag of flour to inventory
            inventory.pop(i)
            inventory.append('Bag of Flour')
            print "You've obtained a Bag of Flour!"
            break
    else:
        print "You got nothing to grind with!"
        
#Cooking System
def cook():
    global cooking
    if 'Bag of Flour' in inventory:
        burnchance = random.randint(0, cooking[0] * 2)
        if burnchance == 0:
            inventory.remove('Bag of Flour')
            print "You've failed to bake: Bread"
            cooking[1] += 2
        elif burnchance != 0:
            inventory.remove('Bag of Flour')
            inventory.append('Bread')
            print "You've sucessfully baked: Bread"
            cooking[1] += 5
            if quest_list[4][2] == 0:
                quest_list[4][2] = 1
                print "You've completed a quest!"
    else:
        print 'You got no flour to bake with'


#Displays inventory
def show_inventory():
    if len(inventory) > 0:
        for i in range(len(inventory)):
                print i+1,'.',inventory[i]
        print moneypouch, 'g'


    if len(inventory) == 0 and moneypouch == 0:
        print "You've got nothing in that bag of yours"


#Checks any equipment in inventory, give stat boost
def check_equipment():
    for i in range(len(inventory)):
        if inventory[i-1] == "Sword":
            attack[2] += 5
    if 'Bread' in inventory:
        opp_styles.append('Eat')


#Combat system
def combat(room):
    global killcount, current_room
    check_equipment()
    min_hit = attack[0] + attack[2]
    max_hit = attack[0]* 3 + attack[2]
    player_hp = (hitpoint[0] + hitpoint[2]) * 5
    if room == 11:
        current_monster = mon_list[0]
        original_monsterhp = current_monster[1]
    elif room == 14:
        current_monster = mon_list[1]
        original_monsterhp = current_monster[1]
        #troubleshoot: print mon_list, current_monster, original_monsterhp
    print 'Approached!'
    
    while current_monster[1] > 0:
        damage = random.randint(min_hit, max_hit)           
        print 'Opponent: ', current_monster[0], '-', current_monster[1], 'HP -|- You: ', player_hp, 'HP|Damage:{0}-{1}'.format(min_hit, max_hit)


        #Printing available attack styles
        for i in range(len(opp_styles)):
            print i+1, '.', opp_styles[i]
        #Prompting user input for action
        atk_action = raw_input('What are you going to do with your opponent: ')
        if atk_action != '1' and atk_action != '2' and atk_action != '3':
            print 'invalid interaction'        
        elif int(atk_action) == 1:
            atk_count = 0
            enemy_atk_count = 0
            current_monster[1] -= damage
            atk_count += 1
            player_hp -= current_monster[2]
            enemy_atk_count += 1
            #Battle result
            if current_monster[1] <= 0:
                killcount += 1 
                print "You've defeated monsters", killcount, 'time(s)'
                #Exp
                #Troubleshoot commands : print current_monster[1], current_monster[2]
                exp_gain = current_monster[2] * 3
                hitpoint_exp_gain = exp_gain*1.5
                hitpoint[1] += hitpoint_exp_gain
                if killcount == 5:
                    quest_list[0][2] = 1
                    print "You've completed a quest!"
                if atk_count > 0:
                    attack[1] += exp_gain
                    if enemy_atk_count > 0:
                        print "You've gained", exp_gain, "attack exp &", hitpoint_exp_gain, "hitpoint exp." 
                #looting
                loot_items = len(current_monster[3])
                loot_chance = random.randint(current_monster[4], 100)
                loot_req = random.randint(0, 100)
                loot_amount = random.randint(1, loot_items)
                #troubleshoot : print loot_items, loot_chance, loot_req, loot_amount
                if loot_chance >= loot_req:
                    print "You've obtained the following: "
                    if loot_items > 1:
                        for i in range(loot_amount):
                            inventory.append(current_monster[3][i])
                            print current_monster[3][i]
                    elif loot_items == 1:
                        inventory.append(current_monster[3][0])
                        print current_monster[3][0]
                        break
                elif current_monster[0] == "Demon":
                    print "*****You've completed all quests!!!!!!!*****"
                    quest_list[6][2] = 1
                    endgame()
                elif loot_chance <= loot_req:
                    print "You were unlucky to obtain any loots from this opponent"
            elif player_hp <= 0:
                print "You're too weak, you fleed back to your home in the forest."
                current_room = 0
                break
        elif int(atk_action) == 2:
            print "You ran for your life"
            return
        elif int(atk_action) == 3:
            player_hp += 20
            inventory.remove('Bread')
            opp_styles.remove('Eat')
    current_monster[1] = original_monsterhp    
    checkstat()


#Checks if player acquired a level    
def checkstat():
    atkexp_50 = []
    hpexp_50 = []
    cookexp_50 = []
    for i in range(50):
        atkexp_50.append(i)
        hpexp_50.append(i)
        cookexp_50.append(i)
    if attack[1] >= (atkexp_50[0] ** 3) + 10:
        attack[0] += 1
        atkexp_50.remove(atkexp_50[0])
        attack[1] = 0
        print "You've gained a level in attack!"
    elif hitpoint[1] >= (hpexp_50[0] ** 3) + 10:
        hitpoint[0] += 1
        hpexp_50.remove(hpexp_50[0])
        hitpoint[1] = 0
        print "You've gained a level in hitpoint!"
    elif cooking[1] >= (cookexp_50[0] ** 3) + 10:
        cooking[0] += 1
        cookexp_50.remove(hpexp_50[0])
        cooking[1] = 0
        print "You've gained a level in cooking!"           


#Displays goal of the game
def help():
    print ''
    print str_form, "Complete all the quest and requirements.", str_form
    print str_form, "You will only win if the program tells you you've won, make sure to check commands!", str_form
    print ''
    mainstate = False
    
#Saves quest's progress
def savequest():
    for i in range(len(quest_list)):
        gamesave.write(str(quest_list[i][2]))
        gamesave.write('\n')     
        
#Save function
def save():
    global gamesave
    #Saving indexes
    #current room, stats, money, inventory, 3 quest's states    
    gamesave = open('gamesave.txt', 'w')  
    #Wrties current room's data
    gamesave.write(str(current_room))
    gamesave.write("\n")
    #Writes player's money
    gamesave.write(str(moneypouch))
    gamesave.write('\n')
    #writes players's inventory
    if inventory[0] == '':
        inventory.remove(inventory[0])     
    for i in range(len(inventory)):
        gamesave.write(str(inventory[i]))
        gamesave.write(',')
    gamesave.write('\n')
    #Saves quests' progression
    savequest()
    #Saves stats
    #attack = [1, 0, 0]hitpoint = [1, 0, 0]cooking = [1, 0, 0]
    gamesave.write(str(attack[0]))
    gamesave.write('\n')
    gamesave.write(str(hitpoint[0]))
    gamesave.write('\n')
    gamesave.write(str(cooking[0]))
    gamesave.write('\n')
    gamesave.close()


#Commands that user can use
def commands():
    print 'All commands are not case-sensitive'
    print "Walking: 'North'/'East'/'West'/'South'"
    print "Quests: 'Quests'/'Quest'"
    print "Stats: 'Stats'/'Stat'"
    print "Combat: 'Kill'/'Fight'/'Flee'/'Eat'"
    print "Store: 'Store'/'Buy'/'Sell'/'Leave'/'Sell all' @ General Store"
    print "1. Next"
    print "2. Back"
    choice = input("Enter command: ")
    if choice == 2:
        mainstate = False
    if choice == 1:
        print "Inventory: 'Inventory'"
        print "Quitting: 'Quit'"
        print "Cooking: 'Cook'/'Bake'"
        print "Windmill: 'Grind'"
        print "Wheat Field: 'Pick'"
        print "1. Back"
        choice = input("Enter command: ") 
        if choice == 1:
            commands()


#Storyline
def storyline():
    print "You were born as a poor child, you have no skills, talents, or great ambition to survive in this cruel world."
    print "One day the Black Demon plundered your entire village, you fleed with great effort, managed to escape the devil's grasp."
    print "You hid in the forest for days, you've learned basic survival skill through your sharp instinct."
    print "Months gone by, you have a home in the forest, but that wasn't enough, you want to learn more"
    print "You've decided it is time, not to hunt just to sleep without an empty stomach, but to do something great."
    print "You decided, to go to the city, the Great City of Kayeffsee, 500 miles south of the forest."
    print "To avenge your village, and earn fame, power, and riches."


#End game story
def endgame():
    print "The Demon stood no chance against your talents and blessings"
    print "You have avenged the members of your village, you spent your following years rebuilding what was yours."
    print "Not only did you became a mayor, your fame and power allowed you to claim the throne of the entire Kingdom of MacRonald"
    print "The Lore of Kayeffsee marked an end with a hero saving the village"
    save()
    main()
    
#Main Menu
def main():
    load()
    mainstate = False  
    while mainstate != True:
        print str_form, 'The Lore of Kayeffsee', str_form
        print '{0:^5}  {1:^5} {2:^5}'.format("1. Play", "2. Help", "3. Commands")   
        try:
            user_option = int(raw_input("Enter your commands: "))
            if user_option == 1:
                quests()
                walk()
                mainstate = True
            elif user_option == 2:
                help()
            elif user_option == 3:
                commands()
            elif user_option == 4:
                mainstate = True
        except ValueError:
            print "Invalid Command!"
storyline()
main()




