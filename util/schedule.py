from datetime import datetime
bell_schedule = "" # can be REGULAR, CONFERENCE, HOMEROOM
type_of_day = "" # can be A, B
day_of_week = "" #can be MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
days = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]

def return_day(num):
    '''Given a num from 0-6 returns Monday-Sunday respectively'''
    return days[num]

for i in range(7):
    print(return_day(i))
