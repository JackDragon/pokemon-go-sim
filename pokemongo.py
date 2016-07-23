from data import pokemon_dict, moves_dict

import random

RED_COLOR = "#F62222"
BLUE_COLOR = "#0055FF"
STAB_RATIO = 1.25

@main
def run():
    simulate_default_single_battle()

def simulate_default_single_battle():
    # Make Trainer
    red = make_default_trainer("Red", RED_COLOR);
    blue = make_default_trainer("Blue", BLUE_COLOR);
    # Play
    battle(red, blue)

def battle(red, blue):
    idle_list = [red, blue]
    random.shuffle(idle_list)
    active = idle_list.pop(0)
    while(not game_over(red, blue)):
        draw_state(red, blue)
        take_turn(active, idle[0])
        idle_list.append(active)
        active = idle_list.pop(0)
    finish_game(red, blue)

def draw_state(red, blue):
    return

def take_turn(trainer, opponent):
    if trainer.get_active():


def finish_game(red, blue):
    if (red.get_alive_count > 0):
        winner = red
        loser = blue
    else:
        winner = blue
        loser = red
    winner.win_game()
    loser.lose_game()
    message(winner.name + " has won the battle! \n" + loser.name + " has lost the battle.")
    message("Stats: \n" + get_battle_stats(red, blue))

def get_battle_stats(red, blue):
    return_string = ""
    for trainer in [red, blue]:
        s = trainer.name() + "stats:\n"
        s += "*  Pokemon total: " + len(trainer.party) + "\n"
        s += "*  Pokemon alive: " + str(trainer.get_alive_count) + "\n"
        s += "*  Average health: " + str(trainer.get_average_hp) + "\n"
        s += "*  Average CP: " + str(trainer.get_average_cp) + "\n"
        s += "*  Trainer W/L now: " + str(trainer.wl[0]) + " wins"
        s += " / " + str(trainer.wl[1]) " losses\n"
        s += "-------------------------------------------\n"
        return_string += s
    return return_string

def message(s):
    print("-------------------------------------------")
    print(s)

class Trainer:
    def __init__(self, name = "Ash", color = RED_COLOR):
        self.order_strategy = OrderStrategy();
        self.move_strategy = MoveStrategy();
        self.party = make_default_party();
        self.active_pokemon = None
        self.wl = [0, 0]
        self.name = name
        self.color = color

    def __init__(self, order_strategy, move_strategy, party, name, color):
        self.order_strategy = order_strategy
        self.move_strategy = move_strategy
        self.party = party
        self.active_pokemon = None
        self.wl = [0, 0]
        self.name = name
        self.color = color

    def get_active_pokemon(self):
        return self.active_pokemon

    def choose_active_pokemon(self, pokemon):
        if pokemon:
            if pokemon.is_fainted:
                self.active_pokemon = None
            else:
                self.active_pokemon = pokemon

    def get_alive_count(self):
        count = 0
        for poke in self.party:
            count += 1 if not poke.is_fainted()
        return count

    def win_game(self):
        self.wl[0] += 1

    def lose_game(self):
        self.wl[1] += 1

class OrderStrategy:
    def __init__(self):
        self.order_strategy = make_default_order_strat()

class MoveStrategy:
    def __init__(self):
        self.move_strategy = make_default_move_strat()

class Pokemon:
    def __init__(self, name="Pidgey", cp=100, hp=100):
        self.name = name
        self.standard = self.get_standard_moves()
        self.special = self.get_special_moves()
        self.types = self.get_types()
        self.hp = hp
        self.cp = cp
        self.special_meter = 0

    """
    Returns a list of the standard moves for the pokemon.
    """
    def get_normal_moves(self):
        if self.name:
            t = pokemon_dict[self.name]["Standard"]
            return [x for x in t if x]
        else:
            return []

    """
    Returns a list of the special moves for the pokemon.
    """
    def get_special_moves(self):
        if self.name:
            t = pokemon_dict[self.name]["Special"]
            return [x for x in t if x]
        else:
            return []

    """
    Returns a list of the special moves for the pokemon.
    """
    def get_special_moves(self):
        if self.name:
            t = pokemon_dict[self.name]["Special"]
            return [x for x in t if x]
        else:
            return []

    """
    Subtracts hp off this pokemon.
    Arguments:
    n -- damage given
    type -- string of type that the move trying to damage you does
    """
    def take_damage(self, n, mtype):
        n = round(n, 1)
        damage = n
        ratio = 1
        for t in self.types:
            ratio *= types_dict[mtype][t]
        damage = round(damage * ratio, 1)
        print("*  incoming move has " + str(n) + " power.\n" + "*  Ratio is " + str(ratio)+"\n")
        print("*  " + self.name + " taking " + str(damage) + " damage after calculations.")
        if self.hp > 0:
            self.hp = max(0, self.hp - damage)
        else:
            print("*** You are trying to take damage when you're fainted!")

    """
    Calculates damage given.
    """
    def do_damage(self, move):
        if not move:
            return 0
        n = move['DPS']
        if move.type in self.types:
            n *= STAB_RATIO
        return n

    """
    Calculates if you have enough special for a move.
    """
    def calc_enough_special(self, move):
        return True

    """
    Calculates special meter increase or not.
    """
    def calculate_special_meter(self, move):
        n = 0
        return n

    """
    Returns if pokemon is fainted or not.
    """
    def is_fainted(self):
        return self.hp <= 0



def make_default_order_strat():
    def choose_next_pokemon(myParty, oppParty):
        alive = myParty.get_alive()
        return random.choice(alive)
    return choose_next_pokemon

def make_default_move_strat():
    def choose_next_pokemon(myParty, oppParty):
        active = myParty.get_active()
        if active:
            moves = active.get_available_moves()
            return random.choice(moves)
        else:
            return None

def make_default_trainer(name = "Ash", color=RED_COLOR):
    return Trainer(name=name, color=color)

def make_default_party(size = 6):
    party = []
    for _ in range(size):
        pkmn = Pokemon()
        party.append(pkmn)
    return party