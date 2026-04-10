import textwrap

# === Game Data ===

rooms = {
    "dining": {
        "description": "You wake up strapped into a chair at a dining table you don't recognize."
          "\nThere is a hallway opening to your west and a knife next to a dinner plate of rotting food in front of you.",
        "items": ["knife"],
        "exits": {},
        "bound": True
    },
    "hallway": {
        "description": "A long hallway. There is a locked door at the end of the hall to the east. To your left is a chest of drawers. \nUnder the lamp that flickers an ominous yellow light, you see a glimmer of metal that appears to be a key!",
        "items": ["key"],
        "exits": {},
        "locked": True
    },
    "bedroom": {
        "description": "You've entered what appears to be the homeowner's bedroom. The room is filthy, with a pungent rotting smell emanating from dark brown stains on the walls.",
        "items": ["photograph", "bills"],
        "exits": {"east": "foyer"}
    },
    "foyer": {
        "description": "You are in the foyer of the house. You try the front door, but its locked. Windows surrounding the door are boarded up with planks of wood and haphazardly placed nails. Upon peering through the peephole in the door, you see a car parked in the driveway of the home. This appears to be your way out.",
        "items": [],
        "exits": {"north": "outside", "south": "den"},
        "locked": True
    },
    "den": {
        "description": "You enter the den, searching frantically for the key to the padlock on the front door. Suddenly, a hard item strikes your head and you fall to the ground! It is the homeowner!",
        "items": ["keyring"],
        "exits": {"north": "foyer"}
    }
}

inventory = []
current_room = "dining"

found_letter = False
found_revolver = False
bullet_count = 8


# === Functions ===

# shows user what room they're in, what they can see, inventory and what items the room contains
def show_status():
    print("\n")
    # print(f"You are in the {current_room}.")

    # dining room description changes after escape
    if current_room == "dining":
        if rooms["dining"]["bound"]:
            print("You wake up strapped into a chair at a dining table you don't recognize."
            "\nThere is a hallway opening to your west and a knife next to a dinner plate of rotting food in front of you.")
        else:
            print("You are standing in the dining room. The ropes that bound you lay torn on the chair behind you. There is a hallway to the west.")
    
    # hallway description
    elif current_room == "hallway":
        print("A long hallway. There is a locked door at the end of the hall to the east. To your left is a chest of drawers.  \nUnder the lamp that flickers an ominous yellow light you see a glimmer of metal that appears to be a key!")

        if rooms["hallway"]["locked"]:
            print("There is a locked door to the east.")
        else:
            print("The door to the east is open.")

    # all other rooms
    else:
        print(rooms[current_room]["description"])

    print(f"\nInventory: {inventory}")

    if rooms[current_room]["items"]:
        print(f"You see: {rooms[current_room]['items']}")


# gets the command from the user of what they want to do next
def get_command():
    return input("\nWhat do you want to do? ").lower()

# movement implementation
def move(direction):
    global current_room

    if direction not in rooms[current_room]["exits"]:
        print("You can't go that way.")
        return
    
    next_room = rooms[current_room]["exits"][direction]

        # check for locked door (hallway)
    if next_room == "bedroom" and rooms["hallway"]["locked"]:
        print("The door is locked. You need a key.")
        return
    
    if next_room == "outside" and rooms["foyer"]["locked"]:
        print("The front door is locked. You need to find the homeowner's keyring.")
        return

    current_room = next_room
    print(f"You move {direction}.")
    show_status()

# removes item from the room and adds to inventory
def take_item(item):
    if item in rooms[current_room]["items"]:
        inventory.append(item)
        rooms[current_room]["items"].remove(item)
        print(f"You picked up {item}.")
    else:
        print("That item is not here.")

# drops item from inventory into the room you are in
def drop_item(item):
    if item in inventory:
        inventory.remove(item)
        rooms[current_room]["items"].append(item)
        print(f"You dropped the {item}.")
    else:
        print("You do not have that item.")

# allows player to use items they find for their specific purpose
def use_item(item):
    global found_letter, found_revolver, bullet_count
    
    if item not in inventory:
        print(f"You do not have the {item}.")
        return
    
    # check for using knife in the dining room
    if item == "knife" and current_room == "dining":
        if rooms["dining"]["bound"]:
            print("You freed yourself from the chair with the knife!")
            rooms["dining"]["exits"]["west"] = "hallway"
            rooms["dining"]["bound"] = False
        else:
            print("You have already freed yourself.")

    # check for using key in the hallway
    elif item == "key" and current_room == "hallway":
        if rooms["hallway"]["locked"]:
            print("You unlock the door to the east!")
            rooms["hallway"]["exits"]["east"] = "bedroom"
            rooms["hallway"]["locked"] = False
        else:
            print("The door is already unlocked.")

    # check for using keyring in the foyer
    elif item == "keyring" and current_room == "foyer":
        if rooms["foyer"]["locked"]:
            print("You unlock the front door!")
            rooms["foyer"]["exits"]["north"] = "outside"
            rooms["foyer"]["locked"] = False
        else:
            print("The door is already unlocked.")

    # check for using photograph in the bedroom
    elif item == "photograph":
        print(f"This {item} depicts a tall, lanky man in his late 20's scowling in between what appears to be his parents. The father, holding a rifle, has a scowl to match the young man's and the mother's eyes are deadpan into the camera. On the young man's belt is a small holster from which glints the hilt of a revolver.")

    # check for using bills in the bedroom
    elif item == "bills":
        print("There are stacks of several overdue bills littering the desk in the bedroom.") 
        print("As you sift through them, you see notices of eviction, credit cards under various names, as well as an oil-stained letter tucked underneath it all.")

        if not found_letter:
            rooms["bedroom"]["items"].append("letter")
            found_letter = True

    # check for using letter once player has used bills
    elif item == "letter":
        if not found_letter:
            print("You haven't found any letter yet.")
            return
    
        print("The letter is frayed and delicate at its seams, indicating perhaps that it has been opened and closed many times. In it appears to be a letter from the son to his father.")
        
        message = """
Pop,
I can't live this way no more. Life on the farm was never for me.
Please let Mama know I love her and that even if I can't see her again with God,
I am happy to be done with this place.

Peter

P.S. Sorry for going through your desk Pop. I promise I ain't touch nothing but my revolver.
"""

        print(textwrap.indent(message, "    "))
        # indents each line with 4 spaces
        #indented_message = textwrap.indent(message, print(indented_message))

        print("\nThe post script catches your attention.")
        print("You put down the letter and shuffle through the papers on the desk and through each drawer. \nFinally, in the second drawer, on the right side of the desk, lays the revolver, fully loaded and safety off. There is no sign of the rifle you saw in the photograph.")

        if not found_revolver:
            rooms["bedroom"]["items"].append("revolver")
            found_revolver = True

    # check for using revolver
    elif item == "revolver":
        if not found_revolver:
            print("You don't know where the revolver is.")
            return
        
        if bullet_count > 0:
            bullet_count -= 1
            print(f"The gun goes off! You now have {bullet_count} bullets left.")
        else:
            print("The revolver is empty.")

    else:
        print(f"You can't use the {item} here.")


# breaks down the command
def process_command(command):
    words = command.split()

    if len(words) == 0:
        return
    
    if words[0] == "go" and len(words) > 1:
        move(words[1])
    
    elif words[0] == "take" and len(words) > 1:
        take_item(words[1])

    elif words[0] == "look":
        print()
        show_status()

    elif words[0] == "inventory":
        if len(inventory) == 0:
            print("You are carrying nothing.")
        else:
            print("You are carrying:")
            for item in inventory:
                print(f"- {item}")
    
    elif words[0] == "drop" and len(words) > 1:
        drop_item(words[1])

    elif words[0] == "use" and len(words) > 1:
        use_item(words[1])

    elif words[0] == "quit":
        return False
    
    else:
        print("Invalid command.")

    return True


# === Game Loop ===
def play_game():
    print("=== MURDER HOUSE SURVIVAL GAME ===")
    print("\nAs you interact with your surroundings, your options in each room are: ") 
    print("\n   - to TAKE, USE or DROP items, enter 'command + item' (ex. take key) ")
    print("\n   - to LOOK at your surroundings, simply enter command 'look'")
    print("\n   - to view your INVENTORY, simply type enter command 'inventory'")
    print("\n   - to GO between rooms, enter 'go + direction' (ex. go east)")
    print("\n   - to QUIT the game, simply enter 'quit'")

    playing = True

    # shows room description once at start
    show_status()

    while playing:
        command = get_command()
        playing = process_command(command)

    print("You use the keyring to start the car. The engine roars as you speed out of the driveway.\n\n")
    print("You have escaped the murder house! Thanks for playing!\n\n")

# start game
play_game()