
'''
 The timesheet date time object class.
'''

class TimeObjectFormat(int):
    SERVOTEST_EXCEL = 0x00

    
class TimeObject(object):

    def __init__(self, miliseconds: float):
        if(type(miliseconds) != float):
            if(type(miliseconds) != int):
                raise TypeError("@TimeObject: require a floating point parameter 1")
        self.__Hours        = 0
        self.__Minutes      = 0
        self.__Seconds      = 0
        self.__Milliseconds = 0;
        self.__Timestamp    = miliseconds;
        self.__ParseMiliSeconds(self.__Timestamp);

    @property
    def Timestamp(self):
        return self.__Timestamp

    @property
    def Hours(self):
        return self.__Hours

    @property
    def Minutes(self):
        return self.__Minutes
  
    @property
    def Seconds(self):
        return self.__Seconds

    @property
    def Milliseconds(self):
        return self.__Milliseconds

    def __eq__(self, other):
        status  =  False;
        if(isinstance(other, TimeObject)):
            status =  other.Timestamp == self.Timestamp
        return status

    def __gt__(self, other):
        status  = False;
        if(isinstance(other, TimeObject)):
            status  = (self.Timestamp > other.Timestamp)
        return status
    
    def __lt__(self, other):
        status  = False;
        if(isinstance(other, TimeObject)):
            status  = (self.Timestamp < other.Timestamp)
        return status

    def __le__(self , other):
        status  =  False;
        if(isinstance(other, TimeObject)):
            status  =  (self < other) or (self == other)
        return status;

    def __ge__(self , other):
        status  =  False;
        if(isinstance(other, TimeObject)):
            status  =  (self > other) or (self == other)

        return status;
            

    def __add__(self, other):
        result  =  None
        if(isinstance(other, TimeObject) is not True):
            raise TypeError("@Expecting a TimeObject object but {0} given".format(type(other)))
        return  TimeObject(self.Timestamp + other.Timestamp);

    def __iadd__(self, other ):
         result  =  self + other
         self.__Seconds     = result.Seconds
         self.__Minutes     = result.Minutes
         self.__Hours        = result.Hours
         self.__Milliseconds = result.Milliseconds
         self.__Timestamp    = result.Timestamp
         return self;

    def __sub__(self, other):
        result  =  None
        if(isinstance(other, TimeObject) is not True):
            raise TypeError("@Expecting a TimeObject object but {0} given".format(type(other)))
        return  TimeObject(self.Timestamp - other.Timestamp);

    def __isub__(self, other ):
        result  =  self - other
        self.__Seconds     = result.Seconds
        self.__Minutes     = result.Minutes
        self.__Hours       = result.Hours
        self.__MiliSeconds = result.MiliSeconds
        self.__Timestamp   = result.Timestamp
        return self;

    def __ParseMiliSeconds(self, milliseconds: float):
        total_seconds            = milliseconds / 1000;
        self.__Milliseconds      = int(milliseconds % 1000);
        self.__Hours    =  int(total_seconds / (60*60)) 
        self.__Minutes  =  int(total_seconds / 60) % 60
        self.__Seconds  =  int(total_seconds) % 60

    def __str__(self):
        return "TimeObject(timestamp = {0})".format(self.Timestamp)
            

    @staticmethod
    def Parse(value:float , formatType  = TimeObjectFormat.SERVOTEST_EXCEL):
        '''
         TimeObjectFormat.SERVOTEST_EXCEL  is HH:percentage of minutes used.
        '''
        result =  None
        if(formatType  == TimeObjectFormat.SERVOTEST_EXCEL):
            MINUTES  = 60.0
            if(type(value) != float):
                if(type(value) != int):
                    raise TypeError("@Parse: expecting a floating type number");
            hours       =  int(value)
            percent     =  (value - hours) * 100
            minutes     =  int((MINUTES * percent) / 100)
            seconds     = (hours * 60 * 60) + (minutes * 60);
            result      = TimeObject(seconds)
        if(result  == None):
            result  =  TimeObject(0);
        return result;

if(__name__=="__main__"):
    
    def PrintTimeObject(timeobject: TimeObject):
        print("Timestamp = {0}".format(timeobject.Timestamp))
        print("Hours = {0}".format(timeobject.Hours))
        print("Minutes = {0}".format(timeobject.Minutes))
        print("Seconds = {0}".format(timeobject.Seconds))
        print("Milliseconds = {0}".format(timeobject.Milliseconds))
        return timeobject
        
    seconds  =  (6* 60 * 60) + (30 *60) + 30;
    miliseconds  =  (seconds * 1000) + 999
    timeobject  = TimeObject( miliseconds )
    timeobject =PrintTimeObject(timeobject);
    print("Add it again")
    timeobject = PrintTimeObject(timeobject + timeobject);
    print("Add it again")
    timeobject+=timeobject
    timeobject =PrintTimeObject(timeobject);
    timeobject +=timeobject  + timeobject
    PrintTimeObject(timeobject);
    print(timeobject == timeobject)
    print(timeobject > timeobject)
    print(timeobject < timeobject)
    print(timeobject <= timeobject)
    print(timeobject >= timeobject)
            
