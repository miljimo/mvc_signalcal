import os;
from modelbase  import ModelBase
from timeobject import TimeObject
from project    import Project, DayOfWeekType

    

'''
    The Project collection data structure.
    
'''
class ProjectCollection(object):

    def __init__(self):
        self.__Headers      =  list();
        self.__Records      =  list();
        self.__FixedRecords =  list();
        self.__FixedElapseHours     = TimeObject(0.0)
        self.__ElapseHours          = TimeObject(0.0);

    @property
    def Total(self):
        return self.ElapseWeeklyHours + self.FixedElapseWeeklyHours

    @property
    def ElapseWeeklyHours(self):
        total =  TimeObject(0.0);
        for project in self.Records:
            total += project.WeeklyElapseHours
        return total;


    @property
    def FixedElapseWeeklyHours(self):
        total =  TimeObject(0.0);
        for project in self.FixedRecords:
            total += project.WeeklyElapseHours
        return total;
        
    @property
    def Header(self):
        return self.__Headers

    @property
    def Records(self):
        return self.__Records;

    @property
    def FixedRecords(self):
        return self.__FixedRecords;

    def __str__(self):
        return self.Records + self.FixedRecords


'''
    The data structure for the timesheet
    a complete data timesheet for every week for the correct employee.
'''
class Timesheet(ModelBase): 

    def __init__(self, uid:str):
        super().__init__();
        self.__TitleHeader          = ""
        self.__Title                = ""
        self.__UID                  = uid
        self.__WeekEndingSunday     = ""
        self.__EmployeeName         = self.__UID
        self.__Department           = ""
        self.__ProjectHeaders       = list()
        self.__Projects             = ProjectCollection()
        self.__Description          = ""
        self.__ElapseHours          = TimeObject(0.0);
        self.__OverTimeHours        = TimeObject(0.0);
        self.__TotalLegalHours      = TimeObject(0.0);
        self.__Template             = ""
        
    @property
    def Description(self):
        return self.__Description

    @Description.setter
    def Description(self, desc:str):
        if(type(desc) != str):
            raise TypeError("@Description: expecting a string value")
        self.__Description =  desc;
        
    @property
    def Department(self):
        return self.__Department

    @Department.setter
    def Department(self, dept:str):
        if(type(dept) != str):
            raise TypeError("Department: expecting a string object")
        self.__Department  =  dept
    @property
    def WeekEndingSunday(self):
        return self.__WeekEndingSunday

    @WeekEndingSunday.setter
    def WeekEndingSunday(self, datestr: str):
        if(type(datestr) != str):
            raise TypeError("@WeekEndingSunday: expecting a string day")
        self.__WeekEndingSunday  =  datestr;
        
    @property
    def EmployeeName(self):
        return self.__EmployeeName

    @EmployeeName.setter
    def EmployeeName(self, employeeName:str):
        if(type(employeeName) != str):
            raise TypeError("@EmployeeName : expecting a string object")
        self.__EmployeeName = employeeName.strip()

    @property
    def TotalLegalWeeklyHours(self):
        return self.__TotalLegalHours

    @TotalLegalWeeklyHours.setter
    def TotalLegalWeeklyHours(self, hours:float):
        if(isinstance(hours, TimeObject) is not True):
            raise TypeError("@TotalLegalHours: expecting a TimeObject object")
        self.__TotalLegalHours =  hours

    @property
    def OverTimeWeeklyHours(self):
        return self.__OverTimeHours

    @OverTimeWeeklyHours.setter
    def OverTimeWeeklyHours(self, value:float):
        if(isinstance(value, TimeObject) is not True):
            raise TypeError("@OverTimeHours property expecting a TimeObject object")
        self.__OverTimeHours  =  value        

    @property
    def Template(self):
        return self.__Template;

    @Template.setter
    def Template(self, template:str):
        if(type(template) != str):
            raise TypeError("@Template: expecting a string object")
        self.__Template  = template.strip()
    
    @property
    def UID(self):
        return self.__UID;

  
    @property
    def Title(self):
        return self.__Title

    @Title.setter
    def Title(self, title:str):
        if(type(title) != str):
            raise TypeError("@Title: expecting a string object")
        self.__Title =  title            

    @property
    def Header(self):
        return self.__TitleHeader

    @Header.setter
    def Header(self, header:str):
        if(type(header) != str):
            raise TypeError("@Header: expecting a string object")
        self.__TitleHeader = header        
   
    @property
    def Projects(self):
        return self.__Projects

    def __str__(self):
        return "Timesheet(employee = {0})".format(self.EmployeeName)


if __name__ =="__main__":
    timesheet =  Timesheet("Obaro I. Johnson");
    timesheet.Projects.Records.append(Project("CRRC080"))
    timesheet.Projects.Records[0].TimeHistory.Update(DayOfWeekType.MONDAY, 1000 * 3 * 60 * 60)
    print(timesheet.Projects.Total)
