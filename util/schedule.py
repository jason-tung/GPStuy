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

def num_periods(num, type):
    '''Sets globals REGULAR, CONFERENCE, HOMEROOM to be of length num'''
    global REGULAR, CONFERENCE, HOMEROOM
    if type == "REGULAR":
        REGULAR = [None for i in range(num)]
    elif type == "CONFERENCE":
        CONFERENCE = [None for i in range(num)]
    elif type == "HOMEROOM":
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

    if period_length == 40:
        num_period += 1 # Accounts for addition 1 homeroom period
        type = "HOMEROOM"
        num_periods(num_period, type)

        for i in range(num_period):
            if i == 3:
                homeroom_time_delta = timedelta(minutes = 12) # Homeroom is 12 minutes long
                set_period(i, start_time, start_time + homeroom_time_delta, type)
                start_time += homeroom_time_delta + time_delta_walk
                continue
            set_period(i, start_time, start_time + time_delta_period, type)
            start_time += time_delta_period + time_delta_walk

    elif period_length == 37:
        type = "CONFERENCE"
        num_periods(num_period, type)
        time_delta_walk = timedelta(minutes = 4)

        for i in range(num_period):
            set_period(i, start_time, start_time + time_delta_period, type)
            start_time += time_delta_period + time_delta_walk

    else:
        type = "REGULAR"
        num_periods(num_period, type)

        for i in range(num_period):
            set_period(i, start_time, start_time + time_delta_period, type)
            start_time += time_delta_period + time_delta_walk


set_periods(10, "8:00", 41, 5) # Sets Stuy Regular Schedule
set_periods(10, "8:00", 40, 5) # Sets Stuy Regular Schedule
set_periods(10, "8:00", 37, 5) # Sets Stuy Regular Schedule
