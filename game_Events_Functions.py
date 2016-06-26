class Event_Functions:
    def __init__(self):
        self.function_database = {}

    def famine(self, mode, choice, event_name, event_database, Nobles, Stats, Events):
        if mode == "start":
            event = event_database[event_name]
            print(event["Name"])
            print(event["Description"])
            print(event["Choice 1"])
            choices = [1]
            if Stats.supplies["Water"] > 5 and Stats.supplies["Air"] > 5:
                print(event["Choice 2"])
                choices.append(2)
            if Stats.nobles_count > 5:
                print(event["Choice 3"])
                choices.append(3)
            if Nobles.stat_check("is_true", "wealth", ">=", 5):
                print(event["Choice 4"])
                choices.append(4)
            return (choices, "first choice")
        if mode == "first choice":
            if choice == 1:
                print("You Lose")
                Stats.is_alive = False
                return (None, "done")
            if choice == 2:
                print("It costs you 5 air and 5 water, but you survive")
                Stats.supplies["Water"] = Stats.supplies["Water"] - 5
                Stats.supplies["Air"] = Stats.supplies["Air"] - 5
                return (None, "done")
            if choice == 3:
                print("All your nobles suddenly get a little bit poorer")
                for k, v in Nobles.nobles.items():
                    Noble = Nobles.nobles[k]
                    Noble["wealth"] = Noble["wealth"] - 1
                Nobles.save_file()
                return (None, "done")
            if choice == 4:
                print("Tax which noble?")
                noble_list = Nobles.stat_check("list", "wealth", ">=", 5)
                for i in range(len(noble_list)):
                    noble = Nobles.nobles[noble_list[i]]
                    print("%d: %s, Wealth: %d" % ((i + 1), noble["full_name"], noble["wealth"] ))
                choices = []
                for i in range(len(noble_list)):
                    choices.append(i + 1)
                return (choices, "noble choice")
        if mode == "noble choice":
            noble_list = Nobles.stat_check("list", "wealth", ">=", 5)
            noble = Nobles.nobles[noble_list[choice - 1]]
            print("%s suddenly gets a lot poorer! (-5 wealth)" % noble["full_name"])
            noble["wealth"] = noble["wealth"] - 5
            return (None, "done")

    def initialise_database(self):
        self.function_database = {
        "famine": self.famine
        }
