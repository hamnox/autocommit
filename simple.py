# mw is main window object
# http://ankisrs.net/docs/addons.html
from aqt import mw
from aqt.utils import showInfo
from aqt.toolbar import Toolbar
from aqt.editor import Editor

from aqt.qt import QAction, SIGNAL
from anki.lang import _
import re
import random
from anki.hooks import addHook


"""
def testFunction():
    card_count = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % card_count)

# create a new menu item
action = QAction("test", mw)
# set to call testFunction when clicked
mw.connect(action, SIGNAL("triggered()"), testFunction)
# add to tools menu
mw.form.menuTools.addAction(action)
"""


# from aqt.editcurrent import EditCurrent
# EditCurrent(mw).editor.note

def fixDamnDivs(note):
    for n, orig in enumerate(note.fields):
        txt = re.sub("(</div>)+","",re.sub("<div>(<br ?/?>)?","<br />",orig))
        txt = re.sub("(<br ?/?>)+$","",txt)
        if txt != orig:
            note.fields[n] = txt
    note.flush()
    return

addHook("editTimer", fixDamnDivs)
addHook("tagsUpdated", fixDamnDivs)


def get_rando_line():
    ans = mw.reviewer.card.a()
    ans = ans.replace("&gt;", ">").replace("&nbsp;", " ").replace("&amp;", "&")
    if re.search("hr id = answer >",ans):
        ans = re.sub(".*hr id = answer >","",ans)
    ans =  re.sub("<style>\.card.*</style>","",ans)
    ans = re.findall("(?:<div>)*(.*?)(?:</div>|<br ?/?>|$)+", ans)

    showInfo(random.choice(ans))

#
#
# def to_wrap_rando_Icons():
#     # create a new menu item
#     return [
#         ["rando", "qrc:/icons/clock16.png",
#            "Give me a random line from this card answer"],
#         ["stats", "qrc:/icons/view-statistics.png",
#          _("Show statistics. Shortcut key: %s") % "Shift+S"],
#         ["sync", "qrc:/icons/view-refresh.png",
#          _("Synchronize with AnkiWeb. Shortcut key: %s") % "Y"]
#         ]
#wrap(Toolbar._rightIcons, to_wrap_rando_Icons, pos="after")

    # need to add to link_handlers for web bridging

action = QAction("Rando Answer Line", mw)
# set to call testFunction when clicked
mw.connect(action, SIGNAL("triggered()"), get_rando_line)
# add to tools menu
mw.form.menuEdit.addAction(action)


# {type: [{fields}]} -> {type: [cleaned output lines]}
"""
def truncate(str):
    return (str[:78] + '..') if (len(str) > 80) else str

assert truncate("Tell me about a time when you had to make a decision without all the information you needed. How did you handle it? Why? Were you happy\n with the outcome?") == ("Tell me about a time when you had to make a decision without all the informati..")
"""



"""
def fix_goals_cards(notelist):
    newcardlist = []
    for note in notelist:
        goal = truncate(note.items()[0][1])
        #notes = truncate(note.items()[1][1])
        oktags = []
        for tag in note.tags:
            if tag not in ["RC", "RC2"]:
                oktags.append(tag)
        lestr = " ".join(oktags) + " goal  -  " + goal + "\n"
        newcardlist.append(lestr)
    with open(file, "w") as f:
        f.writelines(newcardlist)
"""



def cleanup(note, extract):
    retvals = {}
    for k, v in note.items():
        if k in extract:
            newstr = v.replace("&gt;", ">").replace("&nbsp;", " ").replace("&amp;", "&")
            newstr = re.sub("^(<div>)*|(<div>)*(<br ?/?>)*</div>", "",newstr)
            retvals[k] = re.sub("(</?div>|<br ?/?>)+", "  .  ",newstr)

    oktags = []
    for tag in note.tags:
        if tag not in ["RC", "RC2"] and tag[0] != ".":
            oktags.append(tag)

    return oktags, retvals

def export_todos():
    #file = "/Users/hamnox/Documents/Anki/export_todos.csv"
    file = "/Users/hamnox/Spacemonkey/Documents/todos/sharenotes/notes.txt"
    note_dict = {}
    # get notes from todos
    for id in mw.col.findNotes('deck:" Meta*" OR tag:"RC*" OR deck:*Taps'):
        lenote = mw.col.getNote(id)
        lemodel = lenote.model()["name"]
        prev_list = note_dict.get(lemodel, [])
        prev_list.append(lenote)
        note_dict[lemodel] = prev_list

    newcardlist = []
    schedules = []
    for card_type, values in note_dict.items():
        if card_type == "6 - Schedule":
            for note in values:
                oktags, okout = cleanup(note, ['Mode',
                                               'Frog',
                                               'Focus',
                                               'Leisure',
                                               'Liminal'])
                lestr = (okout['Mode'])
                if okout["Frog"] != "":
                    lestr = lestr + "\n - Frog: " + okout['Frog']
                if okout["Focus"] != "":
                    lestr = lestr + "\n - Focus: " + okout['Focus']
                if okout["Leisure"] != "":
                    lestr = lestr + "\n - Leisure: " + okout['Leisure']
                if okout["Liminal"] != "":
                    lestr = lestr + "\n - Liminal: " + okout['Liminal']
                lestr = lestr + "\n\n"
                schedules.append(lestr)
        if card_type == "Goal Card":
            for note in values:
                oktags, okout = cleanup(note, ['Goal'])
                goal = okout['Goal']
                lestr = " ".join(oktags) + " goal  -  " + goal + "\n"
                newcardlist.append(lestr)
        if card_type == "Next Action Card":
            for note in values:
                oktags, okout = cleanup(note, ['Next Action', 'Notes'])
                na = okout['Next Action']
                notes = okout['Notes']
                notes = ("; " + notes) if (len(notes) < 50 and len(notes) > 5) else ""
                lestr = " ".join(oktags) + " NA  -  " + na + notes + "\n"
                newcardlist.append(lestr)
        if card_type == "QA Trial":
            for note in values:
                oktags, okout = cleanup(note, ['Key', 'Question'])
                key = okout['Key']
                question = okout['Question']
                question = (" " + question) if (len(question) > 3) else ""
                lestr = " ".join(oktags) + ' experiment  -  "' + key + '"' + question + "\n"
                newcardlist.append(lestr)
        if card_type == "4 - TAP":
            for note in values:
                oktags, okout = cleanup(note, ['Trigger', 'Action', 'Solution'])
                trigger = okout['Trigger']
                action = okout['Action']
                solution = okout['Solution']
                if (len(solution) < 50 and len(solution) > 5):
                    solution = (" -> " + solution)
                elif (len(solution) > 5):
                    solution = (" -> " + solution[0:47] + "...")
                else:
                    solution = ""
                lestr = " ".join(oktags) + ' TAP  -  ' + trigger + " -> " +  action + solution + "\n"
                newcardlist.append(lestr)


    newcardlist = sorted([str(x) for x in newcardlist], key=str.lower)
    with open(file, "w") as f:
        f.writelines(schedules)
        f.writelines(newcardlist)

    showInfo("%d cards written to file" % (len(newcardlist) + len(schedules)))


# create a new menu item
action = QAction("Export Todos", mw)
# set to call testFunction when clicked
mw.connect(action, SIGNAL("triggered()"), export_todos)
# add to tools menu
mw.form.menuCol.addAction(action)



    # type, {fields} -> fieldstr
    # fieldstr -> RC remove if tag
    # fieldstr -> html format remove

# [cleaned output lines] -> [sorted output lines]
# [cleaned output lines] -> save to file
# wishlist: reset the Todos, flush their history
    # wishlist: given a note, reset it. given a note, flush its history


# reset the scheduler after any DB changes!
mw.reset()
# TODO:   turn off mw.col.startTimebox, mw.col.timeboxReached for todos
# TODO: make new buttons for Todos

# make a randomizer card
# go find some multi-cards and think about data structures
