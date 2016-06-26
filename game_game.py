#This is the main program which runs the game, importing the other files and starting the main
#controller function, and printing the death screen upon death (which is currently only possible via the "suicide" option in events)

import game_Controller
import game_Events
import game_Nobles
import game_Stats
import game_Events_Functions
import game_Events_Database
import eventsbeta

import time
import sys

#Here we set up the class instances for the game

#Next, we tell controller to start collecting inputs. Currently, the main game loop is there - later, there will be periods where
#loops should occur without inputs (running a series of events, for example).

#Design goal: Set up function running from game_game, instead of game_Controller
#

class Game:
    def __init__(self):
        self.current_location = None
        self.locations = None
        self.event_commands = None
        self.noble_commands = None
        self.office_commands = None
        self.location_functions = None

    def load_dictionaries(self):
        self.locations = ["Events", "Nobles", "Office"]
        self.event_commands = {
            "kill_self": Events.kill_self,
            "run_event": Events.run_event,
            "change_location": self.change_location,
            "quit": sys.exit
        }
        self.event_commands_list = ["kill_self", "run_event", "change_location", "quit"]

        self.noble_commands = {
            "Create a new Noble (Manual)": Nobles.create_noble_random,
            "Create a new Noble (Random)": Nobles.create_noble,
            "Delete a Noble": Nobles.remove_noble,
            "Delete all Nobles": Nobles.delete_all,
            "View a Nobles stats": Nobles.get_stats,
            "View all Noble names":Nobles.view_names,
            "Change Location": self.change_location,
            "View all Nobles stats": Nobles.view_everything,
            "Quit": sys.exit
            }

        self.noble_commands_list = ["View all Noble names", "View a Nobles stats", "View all Nobles stats",
                                    "Create a new Noble (Manual)", "Create a new Noble (Random)",
                                    "Delete a Noble", "Delete all Nobles", "Change Location", "Quit"]

        self.office_commands = {
            "view_filled_positions": Nobles.view_filled_positions,
            "view_empty_positions": Nobles.view_empty_positions,
            "fire_noble": Nobles.fire_noble,
            "employ_noble": Nobles.employ_noble,
            "change_location": self.change_location,
            "quit": sys.exit
        }
        self.office_commands_list = ["view_filled_positions", "view_empty_positions", "fire_noble",
                                     "employ_noble", "change_location", "quit"]

        self.location_functions = {
            "Events": (self.event_commands, self.event_commands_list),
            "Nobles": (self.noble_commands, self.noble_commands_list),
            "Office": (self.office_commands, self.office_commands_list),
            "quit": sys.exit
            }


        self.current_location = None

    def change_location(self):
        new_location = Controller.get_input("Go where?", "str", self.locations)
        self.current_location = new_location

    def get_input(self, string, datatype, choice_list = None):
        if choice_list:
            Controller.get_input(string, datatype, choice_list)
        else:
            Controller.get_input(string, datatype)

    def run_function(self):
        function_dictionary = self.location_functions[self.current_location][0]
        function_list = self.location_functions[self.current_location][1]
        function_to_run = Controller.get_input("Do what?", "str", function_list)
        function_to_run = function_dictionary[function_to_run]
        function_to_run()

Game = Game()
Controller = game_Controller.Controllerclass()
Nobles = game_Nobles.Noblesclass()
Stats = game_Stats.Statsclass()
Events = game_Events.EventManager()
Event_Function = game_Events_Functions.Event_Functions()
EventsDatabase = eventsbeta.Event(Nobles, Stats)
#event_database = game_Events_Database.event_database

Game.load_dictionaries()
# Events.initialise_class(Nobles, Stats)
Nobles.load_controller(Controller)
# Stats.initialise_stats(Nobles, Stats, Events)
# Nobles.initialise_nobles()
# Event_Function.initialise_database()


Game.change_location()
while True:
    print("\n\nCurrently in: %s" % Game.current_location)
    Game.run_function()
#Controller.global_commands(Nobles, Stats, Events, Event_Function)

#If the player evver dies, the loops in controller  terminate and we get a death screen.

if Stats.is_alive == False:
    print("Game over, man, game over!")

while Stats.is_alive == False:
      time.sleep(3)
      print("YOU LOSE")
