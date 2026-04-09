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
        "description": "A long hallway. There is a locked door at the end of the hall to the east. To your left is a chest of drawers. \nUnder the lamp that flickers an ominous yellow light you see a glimmer of metal that appears to be a key!",
        "items": ["key"],
        "exits": {},
        "locked": True
    },
    "bedroom": {
        "description": "You've entered what appears to be the homeowner's bedroom. The room is filthy, with a pungent rotting smell emanating from dark brown stains on the walls.",
        "items": ["photograph", "bills", "revolver"],
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


# === Functions ===

# shows user what room they're in, what they can see, inventory and what items the room contains
def show_status():
    print("\n")
    print(f"You are in the {current_room}.")
    print(rooms[current_room]["description"])
    print(f"\nInventory: {inventory}")

    if rooms[current_room]["items"]:
        print(f"You see: {rooms[current_room]['items']}")

    if current_room == "hallway":
        if rooms["hallway"]["locked"]:
            print("There is a locked door to the east.")
        else:
            print("there is an open door to the east.")

    if current_room == "dining":
        if rooms["dining"]["bound"]:
            print("You wake up strapped into a chair at a dining table you don't recognize."
            "\nThere is a hallway opening to your west and a knife next to a dinner plate of rotting food in front of you.")
        else:
            print("You are standing in the dining room. The ropes that bound you lay torn on the chair behind you.")
    
    else:
        print(rooms[current_room]["description"])

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