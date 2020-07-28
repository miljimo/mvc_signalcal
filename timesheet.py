import os;
from modelbase import ModelBase


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



'''
    Enum type for project types;
    servotest timesheet have two project types
    fixed and user defined.
'''
class ProjectType(int):
    USER_DEFINED_PROJECT  =  0x01
    FIXED_PROJECT         =  0x02


'''
    The project record data structure
    This included the time spend on the project
    base on the variables weeks days.
    
'''

class Project(object):

    def __init__(self,workOrderNumber:str, projectType  =  ProjectType.USER_DEFINED_PROJECT):
        if(type(workOrderNumber) != str):
            raise TypeError("@Project: expecting a work order number")
        self.RSRCE               = ""
        self.__WorkOrderNumber   = workOrderNumber
        self.__ContractNumber    = ""
        self.__ElapseHours           =  dict();
        self.__ElapseHours[DayOfWeekType.MONDAY]    = 0.0
        self.__ElapseHours[DayOfWeekType.TUESDAY]   = 0.0
        self.__ElapseHours[DayOfWeekType.WEDNESDAY] = 0.0
        self.__ElapseHours[DayOfWeekType.THURSDAY]  = 0.0
        self.__ElapseHours[DayOfWeekType.FRIDAY]    = 0.0
        self.__ElapseHours[DayOfWeekType.SATURDAY]  = 0.0
        self.__ElapseHours[DayOfWeekType.SUNDAY]    = 0.0
        self.__projectType                          = projectType
        self.__Description                            = ""
        
    @property
    def Description(self):
        return self.__Description;

    @Description.setter
    def Description(self, description:str):
        if(type(description) != str):
            raise TypeError("@Description: expecting string object")
        self.__Description =  description;
            
    @property
    def ContractNumber(self):
        return self.__ContractNumber;

    @ContractNumber.setter
    def ContractNumber(self, contractNumber:str):
        if(type(contractNumber) != str):
            if(type(contractNumber) != int):
                raise TypeError("@ContractNumber: expecting a string object but {0} given.".format(type(contractNumber)))
        self.__ContractNumber = contractNumber;
        
    @property
    def Type(self):
        return self.__projectType
    
    @property
    def WorkOrderNumber(self):
        return self.__WorkOrderNumber
    
    @WorkOrderNumber.setter
    def WorkOrderNumber(self, orderNumber:str):
        if(type(orderNumber) != str):
            raise TypeError("@WorkOrderNumber: expecting a string  object")
        self.__WorkOrderNumber = orderNumber;

    @property
    def ElapseHours(self):
        return self.__ElapseHours;

    def __str__(self):
        return "Project(work_order = {0})".format(self.WorkOrderNumber)


'''
    The Project collection data structure.
    
'''
class ProjectCollection(object):

    def __init__(self):
        self.__Headers      =  list();
        self.__Records      =  list();
        self.__FixedRecords =  list();
        
    @property
    def Header(self):
        return self.__Headers

    @property
    def Records(self):
        return self.__Records;

    @property
    def FixedRecords(self):
        return self.__FixedRecords;


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
        self.__OverTimeHours        = 0
        self.__TotalLegalHours      = 0
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
    def TotalLegalHours(self):
        return self.__TotalLegalHours

    @TotalLegalHours.setter
    def TotalLegalHours(self, hours:float):
        if(type(hours) != float) and (type(hours) != int):
            raise TypeError("@TotalLegalHours: expecting a number")
        self.__TotalLegalHours =  hours

    @property
    def OverTimeHours(self):
        return self.__OverTimeHours

    @OverTimeHours.setter
    def OverTimeHours(self, value:float):
        if(type(value) != int) and (type(value) != float):
            raise TypeError("@OverTimeHours property expecting a number")
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
    print(timesheet)
