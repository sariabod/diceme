import random
from collections import Counter, OrderedDict
from .scores import standard_values
from rich.console import Console
from rich.table import Table
import sys



class Engine:
    def __init__(self):
        self.total = 0
        self.turn_total = 0
        self.current_role = None
        self.current_choices = None
        self.dice = 6
        self.turns = 0
        self.game_total = 10000

    def reset_turn(self):
        self.turn_total = 0
        self.current_choices = None
        self.dice = 6
        self.current_role = None
        self.turns = self.turns + 1
        #lets do a score check
        if self.total >= self.game_total:
            self.end_game()



    def roll(self):
        results = []
        for x in range(self.dice):
            results.append(random.randint(1,6))
        self.current_role = Counter(results)


    def build_choices(self):
        temp_choices = OrderedDict()
        choice_number = 1
        for r in self.current_role.most_common():
            if r[1] > 2:
                temp_choices[choice_number]={
                        "value":r[0],
                        "die":r[1],
                        "points":standard_values[r[0]][r[1]]
                        }
                choice_number = choice_number + 1
            elif r[0]==1 or r[0]==5:
                for n in range(r[1]):
                    temp_choices[choice_number]={
                            "value":r[0],
                            "die":1,
                            "points":standard_values[r[0]][1]
                            }
                choice_number = choice_number + 1
        self.current_choices = temp_choices

    def print_current_total(self,console):
        console.print(f"Your current Total is: {self.turn_total} and you have {self.dice} Die")

    def print_grand_total(self):
        console = Console()
        console.print(f"Your current Score is: {self.total}")

    def end_game(self):
        console = Console()
        console.print(f"Congratulations! Your final Score is: {self.total} taking {self.turns} turn(s)")
        sys.exit()


    def save_choices(self,val):
        temp_points = 0
        temp_dice = 0
        parts = val.split(" ")
        for p in parts:
            try:
                c = self.current_choices[int(p)]
                temp_points = temp_points + c['points']
                temp_dice = temp_dice + c['die']
            except:
                pass

        self.turn_total = self.turn_total + temp_points
        self.dice = self.dice - temp_dice
        if self.dice < 1:
            self.dice = 6
        self.round()

    def end_turn(self):
        #need last round of points
        temp_points = 0
        for key, value in self.current_choices.items():
            temp_points = temp_points + value['points']

        self.turn_total = self.turn_total + temp_points
        self.total = self.total + self.turn_total
        self.reset_turn()


    def round(self):
        self.roll()
        self.build_choices()
        if len(self.current_choices)<1:
            print(f"No valid choices, turn over, you lost {self.turn_total} points")
            self.reset_turn()
            self.print_grand_total()
        else:
            self.print_choice_menu()


    def print_choice_menu(self):

        console = Console()
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("")
        table.add_column("Die")
        table.add_column("Count")
        table.add_column("Points")
        for key, value in self.current_choices.items():
            table.add_row(str(key), str(value['value']),str(value['die']),str(value['points']))

        console.print(table)
        self.print_current_total(console)
