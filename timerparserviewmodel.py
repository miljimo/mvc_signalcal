"""
 Create the timesheet model . to calculated the time sheet as the time is entered.
"""
import os;
from PyPDF2 import PdfFileWriter;
from controllerbase import ControllerBase
from modelbase import ModelBase;
from timesheet import Timesheet, Project, ProjectType , DayOfWeekType
from timesheetreader import TimesheetReader,  ODSTimesheetReader, XLSTimesheetReader
from timesheetrecorder import TimesheetRecorder
import datetime as dt;
from threading import Thread, Lock

    
DAILY_EXPECTED_HOURS  = 35.00 # this is for servotest
WEEKLY_UNPAY_OVERTIME_HOURS  = 2.0   #  Servotest




    

class TimesheetModel(ModelBase):

    def __init__(self, filename:str = None, daily_expected_hours =  DAILY_EXPECTED_HOURS , benefit_hours  = WEEKLY_UNPAY_OVERTIME_HOURS ):
        super().__init__();
        if(os.path.exists(filename) is not True):
            raise TypeError("{0} does not exists".format(filename));
        details  = os.path.splitext(filename)
        if(len(details) <= 1):
            raise TypeError("@Invalid file extension provided");
        extension = details[1][1:].lower();
        if(extension =='xls') or (extension  == 'xlsx'):
            self.__Reader  =  XLSTimesheetReader(filename  =  filename);
        elif(extension=='ods'):
            self.__Reader  = ODSTimesheetReader(filename  =  filename);
        self.__IsAlreadyLoaded = False;
        self.__Timesheet = None;
        self.__DailyExpectedHours  = daily_expected_hours if((type(daily_expected_hours) == float) or (type(daily_expected_hours) == int)) else 0.0
        self.__WeeklyUnPayOvertimeHours  = benefit_hours if((type(benefit_hours) == float) or (type(benefit_hours) == int)) else 0.0
        #Load the timesheet
        if(self.__Reader != None):
            if(self.__IsAlreadyLoaded != True):
                self.__Timesheet  =  self.__Reader.Parse()
                self.__IsAlreadyLoaded = True
        self.__TimeRecorder  = TimesheetRecorder(interval = 1);
        self.__CurrentProject  = None;


    @property
    def Recorder(self):
        return self.__TimeRecorder;
                
    @property
    def WeeklyUnPayOvertimeHours(self):
        return self.__WeeklyUnPayOvertimeHours;


    @property
    def DailyExpectedHours(self) -> float:
        return self.__DailyExpectedHours

    @DailyExpectedHours.setter
    def DailyExpectedHours(self, hours:float):
        if(type(hours) != float):
            if(type(hours) != int):
                raise TypeError("@DailyExpectedHours: expecting a floating point value")
        self.__DailyExpectedHours =  hours        

        
    @property
    def Timesheet(self):
        return self.__Timesheet

    @property
    def Project(self):
        return self.__CurrentProject;

    @Project.setter
    def Project(self, project: Project):
        if(isinstance(project, Project) is not True):
            raise  TypeError("@Project: expecting a Timesheet.Project object type");
        self.__CurrentProject  =  project


    def Compute(self)-> Timesheet:                
        if( self.Timesheet is not None):
            self.Timesheet.Compute();
            # computer  total legal hours and overtimehours
            if(self.Timesheet.ElapseHours > self.DailyExpectedHours):

                overtimeDiff  =  (self.Timesheet.ElapseHours   - self.DailyExpectedHours)
                if(overtimeDiff  > self.WeeklyUnPayOvertimeHours):
                    self.Timesheet.OverTimeHours   = overtimeDiff - self.WeeklyUnPayOvertimeHours;
            self.Timesheet.TotalLegalHours =  self.Timesheet.ElapseHours   - self.Timesheet.OverTimeHours

    @property
    def Projects(self):
        projects  =  list();
        if(self.Timesheet.Projects is not None):
            projects  =  self.Timesheet.Projects.Records + self.Timesheet.Projects.FixedRecords;
        return projects;

    def CreateProject(self , **kwargs):
      
        contract             =  kwargs['contract'] if('contract' in kwargs) else None;
        workOrderNumber      =  kwargs['work_order_number'] if('work_order_number' in kwargs) else "";
        project_type         =  kwargs['project_type'] if('project_type' in kwargs) else ProjectType.USER_DEFINED_PROJECT;
        
        if(contract is None):
            raise TypeError("@CreateProject: expect the contract number of the project");
        project  = Project(workOrderNumber,project_type);
        project.ContractNumber  = contract ;

        if(project.Type  == ProjectType.USER_DEFINED_PROJECT):
            self.Timesheet.Projects.Records.append(project)
        else:
            self.Timesheet.Projects.FixedRecords.append(project)

        return project;
        
        

    def Find(self, **kwargs):
        result   =  None;
        contract  =  kwargs['contract'] if('contract' in kwargs) else '';

        for project in self.Projects:
            if(project.ContractNumber  == contract):
                result  =  project;
                break;
        return result;


    

    
        

class  TimesheetController(ControllerBase):

    def __init__(self):
        super().__init__(self);
                
                                



if __name__ =="__main__":
    ODS_TIME_SHEET_FILE   = "./data/timesheet.ods"
    XLS_TIME_SHEET_FILE   = "./data/timesheet.xlsx"
    WRITE_TEST_FILE       = "./data/pdftest.pdf";
    model       =  TimesheetModel(XLS_TIME_SHEET_FILE);
    pdf_writer  =  PdfFileWriter();

    print("Creating a new Project");
    project  =  model.CreateProject(contract  =  "OB890");
    print(project)
    print(project.WeeklyHours);
    project.AddHour(DayOfWeekType.MONDAY, 2.0);
    

    print("Computing test");
    model.Compute();
    print(model.Timesheet.TotalLegalHours);
    print(model.Timesheet.OverTimeHours);
    print("\nPrint all project test");
    for project in model.Projects:
        print(project.ContractNumber);
    print("\nFind existing contract");
    project  =  model.Find(contract  = '61534');
    if(project is not None):
        print(project.ContractNumber);
        print(project.WeeklyHours)
    
    
   
   
    
    
    
    
              
           
 

   
