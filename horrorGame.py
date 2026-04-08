# === Game Data ===

rooms = {
    "dining": {
        "description": "You wake up strapped into a chair at a dining table you don't recognize."
          "There is a hallway opening to your left and a knife next to a dinner plate of rotting food in front of you.",
        "items": ["knife"],
        "exits": {"west": "hallway"},
        "bound": True
    },
    "hallway": {
        "description": "A long hallway. There is a locked door at the end of the hall to the east. To your left is a chest of drawers.",
        "items": ["key"],
        "exits": {"east": "bedroom"},
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

# gets the command from the user of what they want to do next
def get_command():
    return input("\nWhat do you want to do? ").lower()

# movement implementation
def move(direction):
    global current_room

    if direction in rooms[current_room]["exits"]:
        next_room = rooms[current_room]["exits"][direction]

        # check for locked door (hallway)
        if next_room == "bedroom" and "key" not in inventory:
            print("The door is locked. You need a key.")
        else:
            current_room = next_room
            print(f"You move {direction}.")
    else:
        print("You can't go that way.")

    if direction in rooms[current_room]["exits"]:
        next_room = rooms[current_room]["exits"][direction]

        # check for locked door (foyer)
        if next_room == "foyer" and "keyring" not in inventory:
            print("The door is locked. You need to find the homeowner's keyring.")
        else:
            current_room = next_room
            print(f"You move {direction}.")
    else:
        print("You can't go that way.")

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
    
    if item == "knife" and current_room = "dining":
        




