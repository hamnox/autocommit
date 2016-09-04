from datetime import datetime, timedelta
import random
import math

# TODO: redo with a right-tailed DISTRIBUTION
# http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
# def random_date(startmonth, startday, endmonth, endday=28):
#     """This function will return a random datetime. It has pants safety."""
#     startyear = datetime.now().year()
#     endyear = datetime.now().year()
#     if endmonth < startmonth:
#         endyear = endyear + 1
#     d1 = datetime(startyear, startmonth, startday)
#     d2 = datetime(endyear, endmonth, endday)
#     delta = d2 - d1
#     int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
#     random_second = randrange(int_delta)
#     return d1 + timedelta(seconds=random_second)


# TODO: get cmdline args for # of dates to output and stuff

count = 20
shortdays = 14 * (24 * 60 * 60)
longmonths = 5 * (30 * 24 * 60 * 60)

collection = []
for i in range(count/2):
    delta_int = random.randint(1,shortdays)
    rdate = (datetime.now() + timedelta(seconds=delta_int))
    collection.append(rdate.strftime("%a %b %d"))

    delta_int = random.randint(1,longmonths)
    rdate = (datetime.now() + timedelta(seconds=delta_int))
    collection.append(rdate.strftime("%a %b %d"))

random.shuffle(collection)
for rdate in collection:
    print rdate, random.choice(["8am","1pm","6pm"])
