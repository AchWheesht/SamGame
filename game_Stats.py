#This class handles the stats for the player. It is primarrily responsible for holding and keeping track of the stats,
#not changing them.

class Statsclass:
    def __init__(self):
        self.supplies = {}
        self.is_alive = True
        self.nobles_count = 0

#Initialise stats function, as talked about in game_game.py

    def initialise_stats(self, Nobles, Stats, Events):
        self.supplies = {
        "Food": 10,
        "Water": 10,
        "Air": 10,
        }
        self.nobles_count = len(Nobles.nobles)

        print("Initial Stats Set")
        print("Currnet Noble Count is %d" % self.nobles_count)

#Refreshes stats that are dependant on other variables. This feels like it shouldn't be neccesary, but it a nice backup in case a value is
#altered somewhere else without updating it here.

    def refresh_stats(self, Nobles, Stats, Events):
        self.nobles_count = len(Nobles.nobles)

#This is part of a possible method of storing complex information outside thhe program. It lets me store variables as a dictionary key,
#then replace them with the appropriate variables.

    def return_stat(self, lookup):
        stats_dict = {
        "stat_food": self.food,
        "stat_water": self.water,
        "stat_air": self.air,
        "stat_nobles_count": self.nobles_count
        }
        return stats_dict[lookup]
