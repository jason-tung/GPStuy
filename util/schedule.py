from datetime import datetime
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

def set_period(period, start_time, end_time, walking_time, type):
    '''Sets period in globals REGULAR, CONFERENCE, HOMEROOM (based on type) based on start_time, end_time, walking_time'''
    global REGULAR, CONFERENCE, HOMEROOM
    time_format = "%H:%M"
    type = type.upper()
    if type == "REGULAR":
        REGULAR[period] = (datetime.strptime(start_time, time_format), datetime.strptime(end_time, time_format))
    elif type == "CONFERENCE":
        CONFERENCE[period] = (datetime.strptime(start_time, time_format), datetime.strptime(end_time, time_format))
    elif type == 'HOMEROOM':
        HOMEROOM[period] = (datetime.strptime(start_time, time_format), datetime.strptime(end_time, time_format))
