import json
import sys
import time

import requests


#this functions returns arguments
#separated by spaces provided by user
#when opened from command line
#or when using the interactive console
'''
def sysargs(sysargv, argsdictionary):
    sysarg = [sys.upper() for sys in sysargv]
    if sysarg[0] == '/?' or sysarg[0] == '/help':
        help()
        exit()
    else:
        print(sysarg)
        argsdict = {}
        for b in range(len(argsdictionary[0])):
            if (argsdictionary[0][b] in sysarg):
                argsdict[str(argsdictionary[1][b])] = sysarg[sysarg.index(argsdictionary[0][b])+1]
    return argsdict

def argsdictionary():
   return list([["/IN","/MOD","/LEC","/DAY","/DATE","/ST","/ET","/LOC","/GRP"],["INTAKE","MODID","NAME","DAY","DATESTAMP","TIME_FROM","TIME_TO","LOCATION","GROUPING"]])

'''
def sysargs(sysargv, argsdictionary):
    sysarg = [sys.upper() for sys in sysargv]
    if sysarg[0] == '/?' or sysarg[0] == '/help':
        help()
        exit()
    else:
        print(sysarg)
        argsdict = {}
        for b in range(len(argsdictionary[0])):
            if (argsdictionary[0][b] in sysarg):
                argsdict[str(argsdictionary[1][b])] = sysarg[sysarg.index(argsdictionary[0][b])+1]
    return argsdict

def argsdictionary():
    return list()#[["/DAY","/DATE","/SHIFT","/ST","/ET","/LOC"],["DAY","DATESTAMP_ISO","SHIFT","TIME_FROM","TIME_TO","LOCATION"]])

def list_ta_intake(tadict):
    unique_intake_list = list()
    for ta in tadict:
        intake = str(ta.get("intake")+"-"+ta.get("class"))
        if (intake not in unique_intake_list):
            unique_intake_list.append(intake)
    return unique_intake_list

def tadicts():
    with open('taintake.json') as f:
        data = json.load(f)
    return data

def to_sec(hours,minutes):
    return hours*3600+minutes*60

def get_shift_time(shift):
    if shift == 'S1':
        return dict(to_sec(8,30) = to_sec(10,30))
    elif shift == 'S2':
        return dict(to_sec(10,30) = to_sec(12,30))
    elif shift == 'S3':
        return dict(to_sec(12,30) = to_sec(14,30))
    elif shift == 'S4':
        return dict(to_sec(14,30) = to_sec(16,30))
    elif shift == 'S5':
        return dict(to_sec(16,30) = to_sec(18,30))
    elif shift == 'S6':
        return dict(to_sec(18,30) = to_sec(21,30))
    else:
        print("No shift specified. Exiting...")
        exit(1)
#main function

def main():
    if (len(sys.argv)) < 2:
        try:
            help()
            print("Enter commands without 'timetable.py'.")
            print("Press Ctrl+C to exit.")
            while(True):
                arguments = input(">>>\t")
                arguments = arguments.split(" ")
                print(arguments)
                parsing(sysargs(arguments,argsdictionary()))
        except:
            print("Error, Program exiting...")
            exit(1)
    else:
        parsing(sysargs(sys.argv[1:], argsdictionary()))
        exit(0)

#API Parser function
def parsing(argsdict):
    #api URL
    URL = "https://s3-ap-southeast-1.amazonaws.com/open-ws/weektimetable"
    #open URL
    start_time = time.time()
    data = requests.get(URL).json()
    print("API retrieved in: %s seconds" % (time.time() - start_time))
    return search(data, argsdict, list_ta_intake()) #continues to search phase which takes API data and system arguments

#Search function based on flags,
#it will only take schedules
#that perfectly matches
#the arguments and value given
def search(schedules, argsdict, listtaintake):
    #intake & grouping first priority, then date time
    #search_time=time.time()
    #listtaintake = list_ta_intake(tadicts())
    shift_time = get_shift_time(argsdict.get('/SHIFT'))
    listofschedule = []
    for scheduledict in schedules:
        #intake = scheduledict.get("INTAKE")
        #grouping = scheduledict.get("GROUPING")
        intake_grouping = str(scheduledict.get("INTAKE")+"-"+scheduledict.get("GROUPING"))
        datestamp_iso_parsed = scheduledict.get("DATESTAMP_ISO").split('-')
        datestamp_iso_parsed = ''.join(datestamp_iso_parsed)
        if scheduledict.get("TIME_FROM")[-2:] == 'PM':
            time_from = str(int(scheduledict.get("TIME_TO")[:2])+12)*3600+int(scheduledict.get("TIME_TO")[3:5]*60)
        else:
            time_from = int(scheduledict.get("TIME_FROM")[:2])*3600+int(scheduledict.get("TIME_FROM")[3:5]*60)
        if  scheduledict.get("TIME_TO")[-2:] == 'PM':
            time_to = int(int(scheduledict.get("TIME_TO")[:2])+12)*3600+int(scheduledict.get("TIME_TO")[3:5]*60)
        else:
            time_to = int(scheduledict.get("TIME_TO")[:2])*3600+int(scheduledict.get("TIME_TO")[3:5]*60)

        #time_from_to = dict(time_from = time_to)

        '''
        if (intake_grouping in listtaintake):
            if(intake_grouping in listofschedule):
                if(datestamp_iso_parsed in listofschedule.get(intake_grouping)):
                    if(time_from in listofschedule.get(intake_grouping).get(datestamp_iso_parsed)):
                        pass
                    else:
                        listofschedule.get(intake_grouping).get(datestamp_iso_parsed)[time_from] = time_to
                else:
                    listofschedule.get(intake_grouping)[datestamp_iso_parsed] = time_from_to
            else:
                listofschedule[intake_grouping] = dict(datestamp_iso_parsed = time_from_to)
        else:
            pass
        '''
    return filter(listofschedule,argsdict) #continues to format the values phase

#find empty slots for all intake schedules
def filter_schedules(listofschedule,argsdict):
    return

#find people who is available for the targeted shifts
def findpeople(listofschedule,argsdict):
    listtanames=list_ta_names()
    argsdict

#format and print function
def formatter(list):
    form_time = time.time()
    for v in list:
        print('''~~~\t {modid} \t~~~
Intake: {intake}
Lecture Name: {lec}
Module Code: {modid}
Day and Date: {day} {date}
Time Start and Finish: {tf}-{tt}
Location: {loc}
Grouping: {group}'''
        .format(modid = v["MODID"]
            ,intake = v["INTAKE"]
            ,lec = v["NAME"]
            ,day = v["DAY"]
            ,date = v["DATESTAMP"]
            ,tf = v["TIME_FROM"], tt =v["TIME_TO"]
            ,loc= v["LOCATION"]
            ,group = v["GROUPING"])
            )
    print("Data printed in: %s seconds" % (time.time() - form_time))

#help page function
#will be called upon
#no arguments provided or
#arguments such as /? or /help provided
#then exits the application
def help():
    print('''
Asia Pacific University Timetable Command Line Interface v1.0
Usage: .\\timetable.py /arg value /arg value /arg value

        /? or /help: Show help page and exits.
        /in: Used to search a schedule based on the intake.
        /loc:                    ...                location.
        /lec:                    ...                lecturer name.
        /mod:                    ...                module code.
        /day:                    ...                day.
        /date:                   ...                date.
        /start:                  ...                start time.
        /end:                    ...                end time.
        /grp:                    ...                grouping.
Example: timetable.py /in UC2F1908SE /mod dmtd /date 01
Output:  ~~~      CT015-3-2-DMTD-T-2     ~~~
        Intake: UC2F1908SE
        Lecture Name: CENSORED
        Module Code: CT015-3-2-DMTD-T-2
        Day and Date: FRI 01-MAY-20
        Time Start and Finish: 09:30 AM-10:30 AM
        Location: NEW CAMPUS
        Grouping: T2
        ''')

if __name__ == '__main__':
    main()
