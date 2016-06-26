#Currently the most fleshed out module. Deals with creating, storing, modifying, deleting and inspecting "nobles" - people
#who can be employed by the player to make decisions for them. This is a major part of the game!

#Do I need to import these here? or can I import them in game_game?

import json
import os
import random
import time

class Noblesclass:

    def __init__(self):
        self.nobles = {}
        self.noblenames = {}
        self.filename = "nobles_dict.json"
        if os.path.isfile(self.filename):
           self.load_file()
        self.positions = {                          #Dictionary of positions, and who holds them. Initially filled by initialise_nobles.
        "Keeper of the King's Weasels": None,
        "Official Boot Licker": None,
        "King's Personal Murderer": None,
        "King's least favourite individual": None,
        "King's second best cook": None
        }

    def load_controller(self, Controller):
        self.Controller = Controller

    #Looks for nobles who are employed, and updates the self.positions dictionary to reflect this.
    def initialise_nobles(self):
        for k, v in self.nobles.items():
            noble = self.nobles[k]
            if noble["employed"] == True:
                key = noble["position"]
                self.positions[key] = noble["full_name"]

    #Displays all positions which are not filled by a noble
    def view_empty_positions(self, mode):
        alist = []
        if mode == "print": print("")
        for k, v in self.positions.items():
            if not self.positions[k]:
                if mode == "list": alist.append(k)
                elif mode == "print": print('"%s" is vacant' % k)
                else: return
        if mode == "print": print("")
        if mode == "list":
            alist.sort()
            return alist

    def view_filled_positions(self, mode):
        alist = []
        if mode == "print": print("")
        for k, v in self.positions.items():
            if self.positions[k]:
                if mode == "list": alist.append((k, self.positions[k]))
                elif mode == "print": print('"%s": %s' % (k, self.positions[k]))
                else: return
        if mode == "print": print("")
        if mode == "list":
            alist.sort()
            return alist

    #Assigns a noble to a position
    def employ_noble(self):
        available_nobles = self.stat_check("list", "employed", "=", False)
        available_nobles.append("Cancel")
        available_positions = self.view_empty_positions("list")
        available_positions.append("Cancel")
        hold = True
        noble_input = self.Controller.get_input("Employ Which Noble? (or cancel)", "str", available_nobles)
            #noble_input = input("Employ Which Noble? (or cancel)")
        if noble_input == "Cancel": return
        hold = True
        position_input = self.Controller.get_input("For which position?", "str", available_positions)
        if position_input == "Cancel": return
        noble = self.nobles[noble_input]
        noble["employed"] = True
        noble["position"] = position_input
        self.positions[position_input] = noble_input
        self.save_file()
        print("%s is now the %s" % (noble_input, position_input))

    #Fires a noble from a position
    def fire_noble(self):
        print("\nCurrently Employed Nobles")
        position_list = self.view_filled_positions("list")
        formatted_list = []
        for i in range(len(position_list)):
            hold = position_list[i]
            formatted_list.append("%s: %s" % (hold[0], hold[1]))
        formatted_list.append("Cancel")
        fire_input = self.Controller.get_input("Fire Which Noble?)", "str", formatted_list)
        if fire_input == "Cancel":
            return
        location = formatted_list.index(fire_input)
        hold = position_list[location]
        new_vacant = hold[0]
        fired_noble = hold[1]
        self.positions[new_vacant] = None
        noble = self.nobles[fired_noble]
        noble["employed"] = False
        del noble["position"]
        self.save_file()
        print("%s successfully fired" % (fired_noble))

    #Shows Names of all Nobles
    def view_names(self):
        print("")
        for k, v in self.nobles.items():
            print(k)
        print("")

    def list_names(self):
        noble_list = []
        for k, v in self.nobles.items():
            noble_list.append(k)
        return noble_list

    #Shows Names, Stats and Positions of all Nobles
    def view_everything(self):
        for k, v in self.nobles.items():
            self.get_stats(k)

    #asks for a Nobles name, then shows their stats and positions
    def get_stats(self):
        noble_list = self.list_names()
        request = self.Controller.get_input("Which Noble?", "str", noble_list)
        if request == "Cancel":
            print("Operation Cancelled")
            return
        try:
            noble = self.nobles[request]
            print("\nFull Name:   %s" % noble["extended_title"])
            print("Intelligence    %d  Ambition:    %d\nNetwork:        %d  Wealth:      %d"
                  % (noble["intel"], noble["ambition"], noble["network"], noble["wealth"]))
            try:
                print("A member of the kings court: %s\n" % noble["position"])
            except KeyError:
                pass
            return
        except KeyError:
            print("Name not in database")
            return

    #Sub-function called by create_noble - generates a full name and title for a noble.
    #This is also contained in a seperate file called noblename_app
    def create_noble_name(self, gender, nobility):
        flag = True
        while flag == True:
            flag = False
            if gender == "m":                                   #Setting appropriate lists to use based on the Nobles stats.
                first_name = self.noblenames["first_male"]           #This part gets the appropriate gender lists
                titles = self.noblenames["titles_male"]
            else:
                first_name = self.noblenames["first_female"]
                titles = self.noblenames["titles_female"]
            if nobility >= 7:                                   #This part sets the appropriate ranked nobility lists
                placenames = self.noblenames["placenames_major"]
            elif nobility >= 4:
                placenames = self.noblenames["placenames_minor"]
            else:                                               #This bit unsets some variables of the noble is too shitty to have a title
                placenames = None
                titles = None
                full_title = None
            surname = self.noblenames["surname"]                     #Setting final lists
            nickname = self.noblenames["nicknames"]
            full_name = "%s %s" % (                                     #Generates First and second name, stores under full_name
                first_name[random.randint(1, len(first_name) -1)],
                surname[random.randint(1, len(surname) -1)]
                )
            if titles:                                                  #Generates a title and place, stores under full_title"
                full_title = "%s %s" % (
                    titles[random.randint(1, len(titles) -1)],
                    placenames[random.randint(1, len(placenames) -1)]
                    )
            extended_title = full_name + nickname[random.randint(1, len(nickname) -1)]  #adds a nickname to full_name, stores in extended_title
            if titles:                                          #If the nobility has a title (i.e. they are not shitty), adds it to extended title
                extended_title = "%s, %s" % (
                    extended_title,
                    full_title
                    )

            for k, v in self.nobles.items():                    #Checks to see if a full name or full title is shared by any other noble
                if (v["full_title"] == full_title and titles != None) or v["full_name"] == full_name:
                    flag = True

        return[full_name, full_title, extended_title]           #Returns a list of three values

    #Creates a noble. Is passed "manual", it will asks for stats. If passed "random" it will randomly generate them.
    def create_noble_random(self):
        self.create_noble("random")

    def create_noble(self, mode = "manual"):
        if mode == "manual":
            intel = self.Controller.get_input("What is the Nobles intelligence? (0 - 10)", "int")
            ambition = self.Controller.get_input("What is the Nobles ambition? (0 - 10)", "int")
            network = self.Controller.get_input("How strong is the Nobles network? (0 - 10)", "int")
            wealth = self.Controller.get_input("How wealthy is the Noble? (0 - 10)", "int")
            while True:
                gender = str(input("Male or Female? (m/f)"))
                gender = gender.lower()
                if gender == "m" or gender == "f":
                    break
                print("Sorry, I don't have enough programming skill to deal with non-binary genders")

        elif mode == "random":
            intel = int(round(random.triangular(0, 10)))
            ambition = int(round(random.triangular(0, 10)))
            network = int(round(random.triangular(0, 10)))
            wealth = int(round(random.triangular(0, 10)))
            gender = random.choice(["m", "f"])

        nobility = (network + wealth) / 2

        names = self.create_noble_name(gender, nobility)
        egg = self.egg_checker(names[0])
        if egg:
            names = egg
            stats = egg[3]
            intel = stats[0]
            ambition = stats[1]
            network = stats[2]
            wealth = stats[3]
            gender = stats[4]

        full_name = names[0]
        full_title = names[1]
        extended_title = title = names[2]

        stats = {
            "full_name": full_name,
            "full_title": full_title,
            "extended_title": extended_title,
            "intel": intel,
            "ambition": ambition,
            "network": network,
            "wealth": wealth,
            "gender": gender,
            "employed": False                   #Adding an "employed" stat here
        }
        self.nobles[full_name] = stats

        self.save_file()
        print("")
        print("New noble added!\nName: %s\nIntelligence: %d\nAmbition: %d\nNetwork: %d\nWealth: %s" % (
            extended_title,
            intel,
            ambition,
            network,
            wealth
            ))
        print("")


    #Sub-function of create noble. Checks to see is the nobles full name matches one of ours, and returns a specific set of characters
    #if it does.
    def egg_checker(self, full_name):
        eggs = self.noblenames["eggs"]
        try:
            return eggs[full_name]
        except KeyError:
            return False

    #Removes a noble from the database.
    def remove_noble(self, Noble):
        if Noble == "cancel":
            print("Operation Cancelled")
            return
        try:
            del self.nobles[Noble]
            self.save_file()
            print("")
            print("%s deleted." % Noble)
            print("")
            return
        except KeyError:
            print("Name not in database")

    #removes all nobles from the database
    def delete_all(self):
        if self.Controller.get_input("Are you sure?", "bool"):
            all_nobles = []
            for k, v in self.nobles.items():
                noble = self.nobles[k]
                all_nobles.append(noble["full_name"])
            print(all_nobles)
            for i in range(len(all_nobles)):
                self.remove_noble(all_nobles[i])
        else:
            return

    #specialised function, currecntly unused. For each noble, it takes the a stat (statcheck) and compares (comparator) to a supplied value (value)
    #In mode "list", it return a list of all nobles who pass the check. In mode "is true", returns True if a single noble passes the check.
    def stat_check(self, mode, statcheck, comparator, value):
        true_list = []
        for k, v, in self.nobles.items():
            noble = self.nobles[k]
            stat = noble[statcheck]
            if comparator == ">":
                if stat > value:
                    true_list.append(k)
            if comparator == "<":
                if stat < value:
                    true_list.append(k)
            if comparator == "=":
                if stat == value:
                    true_list.append(k)
            if comparator == ">=":
                if stat >= value:
                    true_list.append(k)
            if comparator == "<=":
                if stat <= value:
                    true_list.append(k)
        if mode == "is_true":
            if len(true_list) != 0:
                return True
            else:
                return False
        if mode == "list":
            if len(true_list) != 0:
                true_list.sort()
                return true_list
            else:
                return None
        return False

    #Saves the nobles database file
    def save_file(self):
        self.initialise_nobles()
        coded = json.dumps(self.nobles)
        with open(self.filename, "w") as file:
            file.write(coded)

    #loads the nobles database file
    def load_file(self):
        with open(self.filename, "r") as file:
            coded = file.read()
        self.nobles = json.loads(coded)
        with open("noblenames.json", "r") as file:
            coded = file.read()
        self.noblenames = json.loads(coded)
