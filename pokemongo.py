from data import pokemon_dict, moves_dict, types_dict, stats_dict

import random

RED_COLOR = "#F62222"
BLUE_COLOR = "#0055FF"
STAB_RATIO = 1.25
POKEMON_LIST = stats_dict.keys()
DAMAGE_DAMPEN_MODIFIER = 50

class OrderStrategy:
    def __init__(self):
        self.choose_next_pokemon = make_default_order_strat()

class MoveStrategy:
    def __init__(self):
        self.choose_next_move = make_default_move_strat()

def run():
    simulate_default_single_battle()

def simulate_default_single_battle():
    # Make Trainer
    red = make_default_trainer("Red", RED_COLOR);
    blue = make_default_trainer("Blue", BLUE_COLOR);
    # Play
    battle(red, blue)

def choose_random_pokemon_all():
    return random.choice(POKEMON_LIST)

def get_trainers_off_cooldown(trainers, cooldowns):
    return [t for t in trainers if t.name not in cooldowns]

def get_type_of_attack(move):
    return moves_dict[move]['Type']

def get_duration_of_attack(move):
    return moves_dict[move]['Duration']

def update_cooldowns(cooldowns):
    if not cooldowns:
        return
    min_cd = min(cooldowns.values())
    to_remove = []
    for k, v in cooldowns.iteritems():
        if v == min_cd:
            to_remove.append(k)
        else:
            cooldowns[k] = round(v-min_cd, 1)
    for k in to_remove:
        cooldowns.pop(k, None)


def battle(red, blue):
    red.set_opponent(blue)
    blue.set_opponent(red)
    red_first_pokemon = red.choose_next_pokemon(blue)
    blue_first_pokemon = blue.choose_next_pokemon(red)
    red.choose_active_pokemon(red_first_pokemon)
    blue.choose_active_pokemon(blue_first_pokemon)
    
    cooldowns = {}
    # random.shuffle(idle_list)
    # active = idle_list.pop(0)
    while(not game_over(red, blue)):
        update_cooldowns(cooldowns)
        if cooldowns:
            for k, v in cooldowns.iteritems():
                message(k + " is still on cooldown for " + str(v) + " ms before able to attack.")
        draw_state(red, blue)
        active_trainers = get_trainers_off_cooldown([red, blue], cooldowns)
        # random.shuffle(active_trainers)
        for trainer in active_trainers:
            if trainer.active_pokemon and not trainer.active_pokemon.is_fainted():
                next_move = trainer.choose_next_move(trainer.opponent)
                damage = trainer.get_active_pokemon().do_damage(next_move)
                trainer.get_active_pokemon().change_special_meter(next_move)
                trainer.opponent.get_active_pokemon().take_damage(damage, get_type_of_attack(next_move))
                cooldowns[trainer.name] = get_duration_of_attack(next_move)
        for trainer in [red, blue]:
            trainer.update()

    finish_game(red, blue)

def draw_state(red, blue):
    return

# def take_turn(trainer, opponent):
#     if trainer.get_active_pokemon():

def game_over(red, blue):
    return (red.get_alive_count() == 0 or blue.get_alive_count() == 0)

def finish_game(red, blue):
    if (red.get_alive_count() == 0 and blue.get_alive_count() == 0):
        red.tie_game()
        blue.tie_game()
        message("Tie game! Well played by both players.")
        message("Stats: \n" + get_battle_stats(red, blue))
        return
    elif (red.get_alive_count() > 0):
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
        s = trainer.name + " stats:\n"
        s += "*  Pokemon total: " + str(len(trainer.party)) + "\n"
        s += "*  Pokemon alive: " + str(trainer.get_alive_count()) + "\n"
        s += "*  Average health: " + str(trainer.get_average_hp()) + "\n"
        s += "*  Average CP: " + str(trainer.get_average_cp()) + "\n"
        s += "*  Trainer W/L now: " + str(trainer.wlt[0]) + " wins"
        s += " / " + str(trainer.wlt[1]) + " losses"
        s += " / " + str(trainer.wlt[2]) + " ties\n"
        s += "-------------------------------------------\n"
        return_string += s
    return return_string

def message(s):
    print("-------------------------------------------")
    print(s)

def make_default_order_strat():
    def choose_next_pokemon(me, opp):
        alive = me.get_alive_pokemon()
        if alive:
            return random.choice(alive)
        else:
            return None
    return choose_next_pokemon

def make_default_move_strat():
    def choose_next_move(me, opp):
        active = me.get_active_pokemon()
        if active:
            moves = active.get_available_moves()
            return random.choice(moves)
        else:
            return None
    return choose_next_move

def make_default_trainer(name = "Ash", color=RED_COLOR):
    return Trainer(name=name, color=color)

def make_default_party(size = 6):
    party = []
    for _ in range(size):
        pkmn = Pokemon()
        party.append(pkmn)
    return party

"""
Returns a list of the types for the pokemon.
"""
def get_types_for_pokemon(pname):
    if pname in pokemon_dict:
        t = pokemon_dict[pname]["Types"]
        return [x for x in t if x]
    else:
        return []

"""
Returns a list of the standard moves for the pokemon.
"""
def get_standard_moves(pname):
    if pname in pokemon_dict:
        t = pokemon_dict[pname]["Standard"]
        return [x for x in t if x]
    else:
        return []

"""
Returns a list of the special moves for the pokemon.
"""
def get_special_moves(pname):
    if pname in pokemon_dict:
        t = pokemon_dict[pname]["Special"]
        return [x for x in t if x]
    else:
        return []

"""
Returns attack, defense, and hp based on CP given.
"""
def get_stats_for_pokemon(name, cp):
    stats = stat_dict[name]
    base = float(stats['Attack'] + stats['Defense'] + stats['Stamina'])
    attack = float(round(cp*stats['Attack']/base, 0))
    defense = float(round(cp*stats['Defense']/base, 0))
    hp = float(round(cp*stats['Stamina']/base, 0))
    return attack, defense, hp

class Pokemon:
    def __init__(self, name=choose_random_pokemon_all(), cp=1000.0):
        self.name = name
        self.standard = get_standard_moves(self.name)
        self.special = get_special_moves(self.name)
        self.types = get_types_for_pokemon(self.name)
        self.cp = cp
        hp, attack, defense = get_stats_for_pokemon(self.name, cp)
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_meter = 0.0

    """
    Subtracts hp off this pokemon.
    Arguments:
    n -- damage given
    type -- string of type that the move trying to damage you does
    """
    def take_damage(self, n, mtype):
        n = round(n, 1)
        damage = n/float(self.defense)
        ratio = 1.0
        for t in self.types:
            mtype_converted = mtype.lower()
            t_converted = t.lower()
            ratio *= types_dict[mtype_converted][t_converted]
        damage = round(damage * ratio, 1)
        print("*  incoming move has " + str(n) + " power.\n" + "*  Ratio is " + str(ratio)+"\n")
        print("*  " + self.name + " taking " + str(damage) + " damage after calculations.")
        if self.hp > 0.0:
            self.hp = max(0.0, self.hp - damage)
        else:
            print("*** You are trying to take damage when you're fainted!")

    """
    Calculates damage given.
    damage = (AttackStat * AttackPower / DefenseStat / 50) * STAB * Effectiveness
    """
    def do_damage(self, move):
        if not move:
            return 0.0
        m = moves_dict[move]
        n = float(m['Power'])
        if m['Type'] in self.types:
            n *= STAB_RATIO
        n *= (self.attack / DAMAGE_DAMPEN_MODIFIER)
        return n

    """
    Handles special meter for using a move.
    """
    def change_special_meter(self, move):
        original = self.special_meter
        change_amount = self.calculate_special_meter(move)
        self.add_special_meter(change_amount)
        message("After using " + move + " , special meter went from " + \
                str(original) + " to " + str(self.special_meter) + ".")

    """
    Calculates if you have enough special for a move.
    """
    def calc_enough_special(self, move):
        m = moves_dict[move]
        if m["Energy Cost"]:
            return m["Energy Cost"] <= self.special_meter
        return True

    """
    Calculates special meter increase or not.
    """
    def calculate_special_meter(self, move):
        n = 0.0
        if move in moves_dict:
            m = moves_dict[move]
            if m["Energy Cost"]:
                n += m["Energy Cost"]
            if m["Energy Per Hit"]:
                n -= m["Energy Per Hit"]
        return n

    """
    Adds to special meter.
    """
    def add_special_meter(self, n):
        self.special_meter += n
        self.special_meter = min(100.0, round(self.special_meter, 1))

    """
    Subtracts from special meter.
    """
    def subtract_special_meter(self, n):
        self.special_meter -= n
        self.special_meter = max(0.0, round(self.special_meter, 1))

    """
    Gets list of useable moves.
    """
    def get_available_moves(self):
        available = [move for move in self.special if self.calc_enough_special(move)]
        available += self.standard
        return available

    """
    Returns if pokemon is fainted or not.
    """
    def is_fainted(self):
        return self.hp <= 0.0

class Trainer:
    # def __init__(self, name = "Ash", color = RED_COLOR):
    #     self.order_strategy = OrderStrategy();
    #     self.move_strategy = MoveStrategy();
    #     self.party = make_default_party();
    #     self.active_pokemon = None
    #     self.wlt = [0, 0, 0]
    #     self.name = name
    #     self.color = color
    #     self.opponent = None

    def __init__(self, order_strategy = OrderStrategy(), move_strategy = MoveStrategy(), \
                party = make_default_party(), name = "Ash", color = RED_COLOR):
        self.order_strategy = order_strategy
        self.move_strategy = move_strategy
        self.party = party
        self.active_pokemon = None
        self.wlt = [0, 0, 0]
        self.name = name
        self.color = color
        self.opponent = None

    def set_opponent(self, opp):
        self.opponent = opp

    def get_active_pokemon(self):
        return self.active_pokemon

    def get_alive_pokemon(self):
        return [poke for poke in self.party if not poke.is_fainted()]

    def choose_active_pokemon(self, pokemon):
        if pokemon:
            if pokemon.is_fainted():
                self.active_pokemon = None
            else:
                self.active_pokemon = pokemon

    def choose_next_pokemon(self, opp):
        poke = self.order_strategy.choose_next_pokemon(self, opp)
        message(self.name + " sends out " + poke.name + ".")
        return poke

    def choose_next_move(self, opp):
        move = self.move_strategy.choose_next_move(self, opp)
        message(self.name + " chooses " + move + " as the next attack.")
        return move

    def get_alive_count(self):
        count = 0
        for poke in self.party:
            if not poke.is_fainted():
                count += 1
        return count

    def get_average_hp(self):
        return sum([poke.hp for poke in self.party]) / float(len(self.party))

    def get_average_cp(self):
        return sum([poke.cp for poke in self.party]) / float(len(self.party))

    def win_game(self):
        self.wlt[0] += 1

    def lose_game(self):
        self.wlt[1] += 1

    def tie_game(self):
        self.wlt[2] += 1

    def update(self):
        if not self.active_pokemon or self.active_pokemon.is_fainted():
            message(self.name + " does not have an active pokemon. Choosing new pokemon.")
            next_pokemon = self.order_strategy.choose_next_pokemon(self, self.opponent)
            if next_pokemon:
                message(self.name + " chose to send out " + next_pokemon.name)
                self.choose_active_pokemon(next_pokemon)
            else:
                message(self.name + " could not send out a pokemon!")
            message(self.name + " has " + str(self.get_alive_count()) + " pokemon left.")


if __name__ == '__main__':
    run()