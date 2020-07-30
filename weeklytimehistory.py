from  timeobject import TimeObject


'''
    Enum type of the day of the week
'''
class DayOfWeekType(int):
    MONDAY      =   0x00,
    TUESDAY     =   0x01,
    WEDNESDAY   =   0x02,
    THURSDAY    =   0x03,
    FRIDAY      =   0x04,
    SATURDAY    =   0x05,
    SUNDAY      =   0x06

class WeeklyTimeHistory(object):
     
    def __init__(self):
        self.__Timesheets           =  dict();
        self.__Timesheets[DayOfWeekType.MONDAY]    = TimeObject(0)
        self.__Timesheets[DayOfWeekType.TUESDAY]   = TimeObject(0)
        self.__Timesheets[DayOfWeekType.WEDNESDAY] = TimeObject(0)
        self.__Timesheets[DayOfWeekType.THURSDAY]  = TimeObject(0)
        self.__Timesheets[DayOfWeekType.FRIDAY]    = TimeObject(0)
        self.__Timesheets[DayOfWeekType.SATURDAY]  = TimeObject(0)
        self.__Timesheets[DayOfWeekType.SUNDAY]    = TimeObject(0)

        self.__TotalTimeObject  = TimeObject(0)

    @property
    def Total(self):
        result  =  TimeObject(0)
        for key in self.__Timesheets:
            timeobject = self.__Timesheets[key]
            result += timeobject;
        return result
            

    def Get(self, weekDay: DayOfWeekType):
        '''
            weekday : DayOfWeekType an integer value for the week 
        '''
        timeobject = None
        if (self.ValidWeekday(weekDay)):
            timeobject  = self.__Timesheets[weekDay];
        return timeobject


    def Update(self, weekday:DayOfWeekType , millseconds:float):
        status  = False;
        if(self.ValidWeekday(weekday)):
            self.__Timesheets[weekday] += TimeObject(millseconds);
            status = True
        return status;

    def Insert(self, weekday:DayOfWeekType, miliseconds:float):
        if(self.ValidWeekday(weekday)):
            self.__Timesheets[weekday]  = TimeObject(miliseconds);
            
    @staticmethod
    def ValidWeekday(weekday:int):
        if(weekday != DayOfWeekType.MONDAY) and \
            (weekday != DayOfWeekType.TUESDAY) and \
            (weekday != DayOfWeekType.WEDNESDAY) and \
            (weekday != DayOfWeekType.THURSDAY) and \
            (weekday != DayOfWeekType.FRIDAY) and \
            (weekday != DayOfWeekType.SATURDAY) and \
            (weekday != DayOfWeekType.SUNDAY):
                return False;
        return True;

    def __str__(self):
        return "WeeklyTimeHistory(hours  = {0} , minutes = {1} , seconds = {2} , milliseconds  = {3})".format(self.Total.Hours, self.Total.Minutes,self.Total.Seconds, self.Total.MiliSeconds)
        

if __name__ =="__main__":
    
  weekly = WeeklyTimeHistory();
  weekly.Insert(DayOfWeekType.MONDAY, (1000  * ( (6 * 60 * 60) + (34 * 60) + 60)) + 987)
  print(weekly.Get(DayOfWeekType.MONDAY))
  print(weekly)
  weekly.Update(DayOfWeekType.MONDAY, 2* 60*60 * 1000)
  print(weekly.Get(DayOfWeekType.MONDAY))
  print(weekly)
