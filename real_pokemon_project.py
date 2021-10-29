import random

class User(object):
    def __init__(self, name):
        self.name = name
        self.pokemon = []
        self.attacking_pokemon = None

    def set_pokemon(self, set_of_pokemon):
        self.pokemon = set_of_pokemon

    def list_pokemon(self):
        #listing pokemon
        print(f"{self.name}'s Pokemon:")
        num = 1
        for pokemon in self.pokemon:
            print(f"{num}: {pokemon}")
            num += 1

    def switch(self, pokemon_number):
        self.attacking_pokemon = self.pokemon[pokemon_number - 1]
        print(f"{self.name} has successfully set the attacking pokemon to {self.attacking_pokemon}")

    def attack(self, attack_name, enemy):
        print(enemy)
        print(f"{self.name} is attacking with pokemon {self.attacking_pokemon} using : {attack_name}")
        self.attacking_pokemon.attack(attack_name, enemy)

class Computer(User):
    def attack(self, attack_name, enemy):
        print(enemy)
        print(f"{self.name} is attacking with pokemon {self.attacking_pokemon} using : {attack_name}")
        self.attacking_pokemon.attack(attack_name, enemy)

    def switch(self, pokemon_number):
        self.attacking_pokemon = self.pokemon[pokemon_number]

        print(f"{self.name} has successfully set the attacking pokemon to {self.attacking_pokemon}")
    
    def heal(self):
        self.attacking_pokemon.hp += 20

class Pokemon(object):
    def __init__(self, hp, max_ap, name):
        self.hp = hp
        self.max_ap = max_ap
        self.name = name
        self.knocked_out = False
        self.attacks = self.set_attacks()
        self.pokemon_type = self.set_type()

    def set_type(self):
        return None

    def set_attacks(self):
        self.attacks = {}

    def get_attacks(self):
        return list(self.attacks.keys())

    def print_attacks(self):
        for attack in self.attacks:
            print(attack)

    def add_attacks(self, attack_dictionary):
        self.attacks = attack_dictionary

    def attack(self, attack_name, enemy):
        atk_acc = random.randint(0, 100)
        if atk_acc <= self.attacks[attack_name][1]:
            print("Attack is working! ")
            print(f"Attack Power: {self.attacks[attack_name][0]}")
            damage = self.attacks[attack_name][0]
            enemy.take_damage(damage)
        else:
            print("You missed!")

    def take_damage(self, damage_amount):
        self.hp -= damage_amount
        if self.hp <= 0:
            self.hp = 0
            self.knocked_out = True
        print(f"{self.name} just got attacked!!!! His health is: {self.hp}")

    def heal(self):
        self.hp += 20

class GrassType(Pokemon):
    def set_type(self):
        return 'grass'

    def set_attacks(self):
        return {"Leaf Storm": [130, 90],
            "Mega Drain":[50, 100],
            "Razor Leaf": [55, 95]}

    def __str__(self):
        return f"{self.name}, TYPE: Grass, HP: {self.hp}, Max AP: {self.max_ap}"

class WaterType(Pokemon):
    def set_attacks(self):
        return {"Bubble": [40, 100],
            "Hydro Pump": [185, 30],
            "Surf": [70, 90]}

    def set_type(self):
        return 'water'

    def __str__(self):
        return f"{self.name}, TYPE: Water, HP: {self.hp}, Max AP: {self.max_ap}"

class FireType(Pokemon):
    def set_type(self):
        return 'fire'

    def set_attacks(self):
        return {"Ember": [60, 100],
            "Fire Punch": [85, 80],
            "Flame Wheel": [70, 90]}

    def __str__(self):
        return f"{self.name}, TYPE: Fire, HP: {self.hp}, Max AP: {self.max_ap}"
    
def game_loop():
    pokemon_list = [
        GrassType(60, 40, 'Bulbasoar'),
        GrassType(40, 60, 'Bellsprout'),
        GrassType(50, 50, 'Oddish'),
        FireType(25, 70, 'Charmainder'),
        FireType(30, 50, 'Ninetails'),
        FireType(40, 60, 'Ponyta'),
        WaterType(80, 20, 'Squirtle'),
        WaterType(70, 40, 'Psyduck'),
        WaterType(50, 50, 'Polywag')]

    user_name = input("What is your name? ") 
    player = User(user_name)
    print(f"Welcome {player.name}, let's play Pokemon!")
    print()
    print("Choose three Pokemon from the list:")
    print()
    # player pokemon setup
    user_choices = []
    choices = ["first", "second", "third"]
    # Getting player's choices for pokemon and converting them into indicies of lists
    for i in range(3):
        num = 1
        for pokemon in pokemon_list:
            print(f"    {num}.{pokemon}")
            num += 1
        while True:
            print()
            choice = int(input(f"Choose your {choices[i]} Pokemon. > "))
            print()
            if pokemon_list[choice - 1] not in user_choices:
                user_choices.append(pokemon_list[choice - 1])
                pokemon_list.remove(pokemon_list[choice - 1])
                break
            else:
                print("You cannot do that, choose a new Pokemon.")
    
    player.set_pokemon(user_choices)
    player.list_pokemon()    

    # computer pokemon setup
    computer_name = input("What would you like your opponent's name to be? ")
    print()
    comp = Computer(computer_name)
    
    computer_choices = list(random.sample(pokemon_list, 3))

    comp.set_pokemon(computer_choices)
    print()
    comp.list_pokemon()
    print()
    game_over = False

    pokemon_choice = int(input("What pokemon would you like to set as your attacking pokemon?"))
    print()
    player.switch(pokemon_choice)
    print()
    
    comp.switch(random.randint(0, 2))
    # comp.switch(random.randint(0,3))

    turn = 0
    while not game_over:
        #checking to see if player pokemon is knocked out
        if player.attacking_pokemon.knocked_out:
            player.pokemon.remove(player.attacking_pokemon)
            num2_pokemon = len(user_choices)
            if num2_pokemon == 0:
                game_over = True
                print()
                print("Game over, You lost, hahaha.")
            else:
                pokemon_choice = int(input(f"Oh no! {player.attacking_pokemon} was knocked out. What pokemon would you like to set as your attacking pokemon? "))
                print()
                player.switch(pokemon_choice)
                print()
        elif comp.attacking_pokemon.knocked_out:
            #checking to see if comp pokemon is knocked out
            print(f"Oh no! {comp.attacking_pokemon} was knocked out. ")
            print()
            comp.pokemon.remove(comp.attacking_pokemon)
            #switch
            num_pokemon = len(comp.pokemon)
            if num_pokemon == 0:
                game_over = True
                print("The computer lost, good job!")
            else:
                max_pokemon_index = num_pokemon - 1
                cpu_choice = random.randint(0, max_pokemon_index)
                comp.switch(cpu_choice)
        else:
            #player's turn
            player.list_pokemon()
            print()
            comp.list_pokemon()
            if turn % 2 == 0:
                print()
                choice = input("What would you like to do? (attack, heal, or switch) ")
                print()
                #attack
                if choice == 'attack':

                    print(player.attacking_pokemon.set_attacks())

                    attack_choice = int(input(f"{player.name}, choose an attack. "))
                    attack_choice = list(player.attacking_pokemon.attacks)[attack_choice-1]
                    print(f"attack choice: {attack_choice}")
                    player.attack(attack_choice, comp.attacking_pokemon)
                elif choice == 'heal':
                    player.attacking_pokemon.hp += 20
                    print(f"{user_name} is healing, his health is now {player.attacking_pokemon.hp}.")
                elif choice == 'switch':
                    if len(user_choices) == 0:
                        game_over = True
                    else:
                        pokemon_choice = int(input("What pokemon would you like to set as your attacking pokemon? "))
                        player.switch(pokemon_choice)
            else:
                #computer's turn
                move = random.randint(1, 6)
                print()
                print(f"Now it is {computer_name}'s turn.")
                print()
                if move <= 4:
                    #attack
                    print(comp.attacking_pokemon.set_attacks())
                    
                    comp_atk_choice = random.randint(0, 3)
                    comp_atk_choice = list(comp.attacking_pokemon.attacks)[comp_atk_choice-1]
                    print(f"{computer_name} is using the {str(comp_atk_choice)} attack!")

                    comp.attack(comp_atk_choice, player.attacking_pokemon)
                elif move == 5:
                    #heal
                    comp.heal()
                    print(f"{computer_name} is healing, his health is now {comp.attacking_pokemon.hp}.")
                elif move == 6:
                    #switch
                    num_pokemon = len(comp.pokemon)
                    if num_pokemon == 0:
                        game_over = True
                        print("The computer lost, good job!")
                    else:
                        max_pokemon_index = num_pokemon - 1
                        cpu_choice = random.randint(0, max_pokemon_index)
                        comp.switch(cpu_choice)
            turn += 1

game_loop()