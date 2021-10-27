import re
from robobrowser import RoboBrowser
import datetime
import schedule
from datetime import datetime as dt
import time

# I'm lazy I only workout Mon-Tue-Thur 17:00 and Wed 19:00 (meetings up to 18)
def GetTime(date_time):
    week_day = date_time.weekday()
    # Wednesday
    if week_day == 2:
        return 19
    elif week_day > 4:
        return -1
    else:
        return 17

class CrossfitAutoSign:
    def __init__(self, start_date):
        f = open("config.txt", "r")
        self.credentials=dict(
            username=f.readline().split("\n")[0],
            password=f.readline().split("\n")[0]
        )
        self.crossfit = f.readline().split("\n")[0]
        self.current_date = start_date
        self.br = RoboBrowser(history=True, parser="html.parser")
        schedule.every().day.at("01:00").do(self.Run)
        while True:
            schedule.run_pending()
            time.sleep(30)

    def Login(self):
        self.br.open(url='https://'+ self.crossfit+'.sportbitapp.nl/cbm/account/inloggen/?post=1', method='post', data=self.credentials)

    def ScheduleClass(self,date_time):
        year_number = str(date_time.isocalendar().year)
        week_number = str(date_time.isocalendar().week)
        self.br.open('https://'+ self.crossfit+'.sportbitapp.nl/cbm/account/lesmomenten/'+year_number+'/'+week_number+'/?locatie=2')
        date_str = date_time.strftime("%d-%m-%Y")
        time_str = date_time.strftime("%H:%M")
        print (date_str)
        print (time_str)
        class_url = 'https://'+ self.crossfit+'.sportbitapp.nl/cbm/'
        course_id = 0
        for line in str(self.br.parsed).splitlines():
            if 'href="training-info/' in line and 'data-time-start="'+time_str+'"' in line:
                regex = re.search('training-info/'+date_str+'/'+time_str+'/(.+?)/', line)
                if regex:
                    course_id = regex.group(0)
                    break
        class_url += course_id
        self.br.open(class_url + "/aanmelden")
        print ("Sair da jaula o Monstro " + date_str + " " + time_str)

    def Run(self):
        # We prolly want to login every day
        self.Login()
        time = GetTime(self.current_date)
        # Time to rest - get the gains - drink whey protein
        if time != -1:
            schedule_date = dt(self.current_date.year, self.current_date.month, self.current_date.day,time)
            self.ScheduleClass(schedule_date)
        self.current_date += datetime.timedelta(days=1)


start_date = datetime.date(2021,11,9)
CrossfitAutoSign(start_date)