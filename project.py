from timeobject import TimeObject
from weeklytimehistory import DayOfWeekType, WeeklyTimeHistory

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
   
    def __init__(self,orderNumber:str, projectType  =  ProjectType.USER_DEFINED_PROJECT):
        if(type(orderNumber) != str):
            raise TypeError("@Project: expecting a order number to be string")
        self.RSRCE               = ""
        self.__WorkOrderNumber   = orderNumber
        self.__ContractNumber    = orderNumber
        self.__TimeHistory       = WeeklyTimeHistory();
        self.__projectType       = projectType
        self.__Description       = ""
        self.__WeeklyHours       = TimeObject(0)


    @property
    def WeeklyElapseHours(self):
        return self.TimeHistory.Total

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
    def TimeHistory(self):
        return self.__TimeHistory;

    def __str__(self):
        return "Project(contract = {0})".format(self.ContractNumber)


if __name__ =="__main__":
    project = Project("BBK")
    project.TimeHistory.Update(DayOfWeekType.MONDAY, 1000 * 3 * 60*60)
    project.TimeHistory.Update(DayOfWeekType.FRIDAY, 1000 * 3 * 60*60)
    print(project.TimeHistory.Get(DayOfWeekType.MONDAY));
    print(project.WeeklyElapseHours);
