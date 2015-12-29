import random
import sys
import datetime

import argparse
parser = argparse.ArgumentParser(description="Give me a next action")

# I must use nargs ? to make optional positional arguments, (could also use *)
parser.add_argument('section',
        type=str,
        nargs='?',
        help='string contained in section',
        default="")

# TODO: make it list all the categories on a flag or something.

args = parser.parse_args()

with open("Everyday notes.txt","r") as todos:
    lines = todos.read().splitlines()
    assert lines.index("~END LIST") > -1
    lines = lines[1 : lines.index("~END LIST") - 1]


    save_lines = []

    if args.section:
        args.section = args.section.lower()
        end = lines.index("")
        while True:
            if args.section in lines[0].lower():
                save_lines.extend(lines[0 : lines.index("")])
                for thing in save_lines:
                    print thing
            lines = lines[lines.index("") + 1 : ]
            if len(lines) < 1:
                break

        if len(save_lines) < 1:
            save_lines.append('No sections matched "' + args.section + '"')
        lines = save_lines

    #TODO: stop being lazy and make an actual iterable
    def get_line():
        next_line = ""
        while next_line == "":
            next_line = random.choice(lines[:])
        return next_line


    print ""
    returned_line = get_line()
    print returned_line

    response = raw_input(" save Y/n/e: ")
    if response.lower() in ["y","yes",""]:
        with open('tasks.log','a') as taskfile:
            taskfile.write(datetime.datetime.now().ctime()
                    + "  -> "
                    + returned_line + "\n")
            print 'saved'
    elif response.lower() in ["e","edit","c","change"]:
        response = raw_input(" > ")
        with open('tasks.log','a') as taskfile:
            taskfile.write(datetime.datetime.now().ctime()
                    + "  ->  "
                    + response + "\n")
            print 'saved'

    else:
        pass
    print ""
