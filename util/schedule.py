from datetime import datetime, timedelta
bell_schedule = "" # can be REGULAR, CONFERENCE, HOMEROOM
type_of_day = "" # can be A, B
day_of_week = "" #can be MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
days = ["MONDAY","TUESDAY","WEDNESDAY","THURSDAY","FRIDAY","SATURDAY","SUNDAY"]
REGULAR = []
CONFERENCE = []
HOMEROOM = []

def return_day(num):
    '''Given a num from 0-6 returns Monday-Sunday respectively'''
    return days[num]

def num_periods(num):
    '''Sets globals REGULAR, CONFERENCE, HOMEROOM to be of length num'''
    global REGULAR, CONFERENCE, HOMEROOM
    REGULAR = [None for i in range(num)]
    CONFERENCE = [None for i in range(num)]
    HOMEROOM = [None for i in range(num)]

def set_period(period, start_time, end_time, type):
    '''Sets period in globals REGULAR, CONFERENCE, HOMEROOM (based on type) based on start_time, end_time, walking_time'''
    global REGULAR, CONFERENCE, HOMEROOM

    type = type.upper()
    if type == "REGULAR":
        REGULAR[period] = (start_time, end_time)
    elif type == "CONFERENCE":
        CONFERENCE[period] = (start_time, end_time)
    elif type == 'HOMEROOM':
        HOMEROOM[period] = (start_time, end_time)

def set_periods(num_period, start_time, period_length, walking_time):
    '''Sets all the periods given start_time of day (HH:MM), period length (minutes), and walking time (minutes) between periods'''
    time_format = "%H:%M"
    start_time = datetime.strptime(start_time, time_format)
    time_delta_period = timedelta(minutes = period_length)
    time_delta_walk = timedelta(minutes = walking_time)
    num_periods(num_period)
    if period_length == 41:
        type = "REGULAR"
        for i in range(num_period):
            set_period(i, start_time, start_time + time_delta_period, type)
            start_time += time_delta_period + time_delta_walk

    if period_length == 40:
        num_periods(num_period+1)
        type = "HOMEROOM"
        for i in range(num_period+1):
            if i == 3:
                homeroom_time_delta = timedelta(minutes = 12) # Homeroom is 12 minutes long
                set_period(i, start_time, start_time + homeroom_time_delta, type)
                start_time += homeroom_time_delta + time_delta_walk
                continue
            set_period(i, start_time, start_time + time_delta_period, type)
            start_time += time_delta_period + time_delta_walk

set_periods(10, "8:00", 41, 5) # Sets Stuy Regular Schedule
set_periods(10, "8:00", 40, 5) # Sets Stuy Regular Schedule
print(HOMEROOM)
