import random
import re
from datetime import datetime

# with open("aliefs", "w") as writer:
#     with open("aliefs.csv", "r+") as f:
#         all_lines = f.readlines()
#         for i, line in enumerate(all_lines):
#             if line[0] == '"':
#                 start = line.find('"',1)
#                 all_lines[i] = line[1:start] + line[start + 1:].replace(",","|")
#             else:
#                 all_lines[i] = line.replace(",", "|")
#         writer.writelines(all_lines)




# If-Then Statement|Actual|Date Review|Estimated Probability of Resonance|Date Predicted|Comments
# format of aliefs file

tb_lines = []
old_lines = []
with open("aliefs", "r") as f:
    all_lines = [x.replace("\r\n", "\n") for x in f.readlines()]
    for i, line in enumerate(all_lines):
        # check if 2nd column is blank
        start = line.find("|")
        if start < 0:
            continue
        if line[start:start + 2] == "||":
            tb_lines.append(line)
        else:
            old_lines.append(line)


# seperate the pieces
tb_answered = [re.findall("([^\|]*?)\|", l) for l in tb_lines]

# get the user take on old predictions
def get_num(prompt):
    blah = "hohoho"
    while (not re.search("^10$|^[1-9]$",blah)):
        blah = raw_input(prompt)
        if blah.lower() in ["n", "next", "s", "skip"]:
            return None
    return blah

if len(tb_answered) > 0:
    blah = raw_input("Cash in " + str(len(tb_answered)) + " old predictions?  -> ")
    if blah.lower() in ["y", "yes"]:
        for l in tb_answered:
            prompt = l[4] + " " + l[0] + " (1-10/Skip) -> "
            blah = get_num(prompt)
            if blah is None:
                old_lines.append("|".join(l) + "|")
                continue
            l[1] = blah
            l[2] = datetime.now().strftime("%Y-%m-%d")
            old_lines.append("|".join(l) + "|")

    with open("aliefs", "wb") as f:
        f.writelines(old_lines)
    print ""
    print ""


tb_answered = [x[0] for x in tb_answered]
answerables = set([re.findall("^(.*?)\|",l)[0] for l in old_lines[1:]])
answerables = random.sample(tuple(answerables), 8)


for l in answerables:
    if l not in tb_answered:
        prompt = l + "\n    (RIGHT NOW 1-10/Skip) -> "
        blah = get_num(prompt)
        if blah is not None:
            newl = (l, blah, datetime.now().strftime("%Y-%m-%d"), "", "", "")
            old_lines.append("|".join(newl) + "\n")
        prompt = "    (PREDICT AT NEXT REVIEW 1-10/Skip) -> "
    else:
        prompt = l + "\n    (PREDICT AT NEXT REVIEW 1-10/Skip) -> "
    blah = get_num(prompt)
    if blah is not None:
        newl = (l, "", "", blah, datetime.now().strftime("%Y-%m-%d"), "")
        old_lines.append("|".join(newl) + "\n")
    print ""

with open("aliefs", "wb") as f:
    f.writelines(old_lines)
