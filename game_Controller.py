#Currently handles the manual running of processes.

class Controllerclass:
    def __init__(self):
        pass

    def get_input(self, input_string, datatype = "str", valid_options = None):
        string = ""
        if datatype == "bool": string += " (y/n)"
        if valid_options:
            string += ("\nOptions: ")
            i = 0
            for item in valid_options:
                i += 1
                string += ("[%d: %s] " % (i, item))
                if i % 3 == 0: string += "\n"
        string += "\n"
        string += input_string
        user_input = input(string + " ")
        flag = False
        while True:
            valid_input = True
            if flag == True: user_input = input()
            flag = True

            if valid_options:
                try:
                    user_input = int(user_input)
                    if user_input <= len(valid_options) and user_input >= 1: user_input = valid_options[user_input - 1]
                    else: valid_input = False
                except ValueError: valid_input = False

            if valid_input:
                if datatype == "str": return user_input
                elif datatype == "int":
                    try: return int(user_input)
                    except ValueError: print("That's not an integer")
                elif datatype == "bool":
                    if user_input == "y": return True
                    else: return False
            else: print("Invalid input")
