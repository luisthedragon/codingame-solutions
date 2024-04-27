import sys
import math
from enum import Enum
import random
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


class Player:
    def __init__(
        self,
        health = None,
        mana = None,
        deck = None,
        rune = None,
        draw = None,
    ):
        self.health = health # the remaining HP of the player.
        self.mana = mana # the current maximum mana of the player.
        self.deck = deck # the number of cards in the player's deck. During the Draft phase, the second player has less card in his deck than his opponent.
        self.rune = rune # the next remaining rune of a player.
        self.draw = draw # the additional number of drawn cards - this turn draw for the player, next turn draw (without broken runes) for the opponent.

class Card:
    def __init__(
        self,
        card_number = None,
        instance_id = None,
        location = None,
        card_type = None,
        cost = None,
        attack = None,
        defense = None,
        abilities = '',
        my_health_change = 0,
        opponent_health_change = 0,
        card_draw = 0
    ):
        self.card_number = card_number # the identifier of a card
        self.instance_id = instance_id # the identifier representing the instance of the card (there can be multiple instances of the same card in a game).
        self.location = location # The location of the card
        # 0: in the player's hand
        # 1: on the player's side of the board
        # -1: on the opponent's side of the board
        self.card_type = card_type # The type of the card
        # 0: Creature
        # 1: Green item
        # 2: Red item
        # 3: Blue item
        self.cost = cost # the mana cost of the card
        self.attack = attack
        self.defense = defense
        self.abilities = abilities
        self.my_health_change = my_health_change
        self.opponent_health_change = opponent_health_change,
        self.card_draw = card_draw

    class CardType(Enum):
        CREATURE = 0
        GREEN_ITEM = 1
        RED_ITEM = 2
        BLUE_ITEM = 3

    def is_lethal(self):
        return 'L' in self.abilities

    def is_guarded(self):
        return 'B' in self.abilities

    def is_item(self):
        print("Debug messages...", self.card_type, Card.CardType.CREATURE.value, self.card_type != Card.CardType.CREATURE.value, file=sys.stderr, flush=True)
        return self.card_type != Card.CardType.CREATURE.value

    def receive_damage(self, damage):
        self.defense -= damage


# game loop
while True:
    players_stats = []
    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
        player = Player(
            player_health,
            player_mana,
            player_deck,
            player_rune,
            player_draw,
        )
        players_stats.append(player)
    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    for i in range(opponent_actions):
        card_number_and_action = input()
    card_count = int(input())

    all_cards = [] # Depending on location, cards are in my hand (0), my side of the board (1) or the opponent's side of the board
    opponent_board_cards = []

    for i in range(card_count):
        inputs = input().split()

        # print("Debug messages...", inputs, file=sys.stderr, flush=True)

        card_number = int(inputs[0])
        instance_id = int(inputs[1])
        location = int(inputs[2])
        card_type = int(inputs[3])
        cost = int(inputs[4])
        attack = int(inputs[5])
        defense = int(inputs[6])
        abilities = inputs[7]
        my_health_change = int(inputs[8])
        opponent_health_change = int(inputs[9])
        card_draw = int(inputs[10])

        card_data = Card(
            card_number,
            instance_id,
            location,
            card_type,
            cost,
            attack,
            defense,
            abilities,
            my_health_change,
            opponent_health_change,
            card_draw
        )

        all_cards.append(card_data)

        # Save opponent cards because we want to attack the guards first
        if location == -1:
            opponent_board_cards.append(card_data)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # print("PASS")

    if player_mana == 0:
        # DRAFT PHASE
        card_to_pick = random.randint(0,2)
        print(f"PICK {card_to_pick}")
    else:
        # BATTLE PHASE

        # STRAT 2: Play all the possible actions
        all_actions = []
        for i, current_card in enumerate(all_cards):
            if current_card.location == 0:
                if not current_card.is_item():
                    summon_action = f"SUMMON {current_card.instance_id}"
                    all_actions.append(summon_action)
                else:
                    already_used = False
                    if current_card.card_type == Card.CardType.BLUE_ITEM:
                        # use_action = f"USE {current_card.instance_id}"
                        pass
                    elif current_card.card_type == Card.CardType.RED_ITEM:
                        for j, opponent_board_card in enumerate(opponent_board_cards):
                            if not already_used:
                                use_action = f"USE {current_card.instance_id} {opponent_board_card.instance_id}"
                                already_used = True
                    else:
                        use_action = f"USE {current_card.instance_id} -1"
                    all_actions.append(use_action)

            if current_card.location == 1:
                already_attacked = False # Whether my current card has already attacked
                for j, opponent_board_card in enumerate(opponent_board_cards):
                    if not already_attacked and opponent_board_card.is_guarded() and opponent_board_card.defense > 0:
                        opponent_board_card.receive_damage(current_card.attack)
                        attack_action = f"ATTACK {current_card.instance_id} {opponent_board_card.instance_id}"
                        already_attacked = True
                if not already_attacked:
                    attack_action = f"ATTACK {current_card.instance_id} -1"
                all_actions.append(attack_action)

        print(";".join(all_actions))
