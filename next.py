import random

with open("Everyday notes.txt","r") as todos:
    lines = todos.read().splitlines()
    print ""
    print random.choice(lines[0:lines.index("~END LIST")])
    print ""
