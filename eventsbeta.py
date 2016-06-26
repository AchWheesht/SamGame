class Event:
    def __init__(self, Nobles, Stats):
        self.Nobles = Nobles
        self.Stats = Stats

class FamineEvent(Event):
    def __init__(self):
        self.Nobles = Event.Nobles
        self.Stats = Event.Stats

    def run_event(self, mode, choice):
        if mode == "start":
            print("Famine!")
            print("Famine strikes! Your people are starving. How do you react?")
            print("1. Let them starve")
            choices = [1]
            if self.Stats.supplies["Water"] > 5 and self.Stats.supplies["Air"] > 5:
                print(event["2. Force feed them water and air"])
                choices.append(2)
            if self.Stats.nobles_count > 5:
                print(event["3. Tax your nobles to feed them"])
                choices.append(3)
            if Nobles.stat_check("is_true", "wealth", ">=", 5):
                print(event["4. Tax a specific noble to feed them"])
                choices.append(4)
            return (choices, "first choice")
        if mode == "first choice":
            if choice == 1:
                print("You Lose")
                self.Stats.is_alive = False
                return (None, "done")
            if choice == 2:
                print("It costs you 5 air and 5 water, but you survive")
                self.Stats.supplies["Water"] = self.Stats.supplies["Water"] - 5
                self.Stats.supplies["Air"] = self.Stats.supplies["Air"] - 5
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
