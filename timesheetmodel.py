import os;
from events     import Event, EventHandler
from modelbase  import ModelBase;
from timeobject import TimeObject
from project    import Project,  ProjectType 
from timesheet  import Timesheet, DayOfWeekType
from timesheetreader import TimesheetReader,  ODSTimesheetReader, XLSTimesheetReader


DAILY_EXPECTED_HOURS         = 35.00 # this is for servotest
WEEKLY_UNPAY_OVERTIME_HOURS  = 2.0   #  Sthreshold overtime hours before pay.
ODS_TIME_SHEET_FILE   = "./data/timesheet.ods"
XLS_TIME_SHEET_FILE   = "./data/timesheet.xlsx"

"""
 A class that will load the time sheet
 from the an excel files.
"""
class XLSTimesheetLoader(ModelBase):
    def __init__(self, filename):
        super().__init__();
        self.__Reader = None
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

    @property
    def Reader(self):
        return self.__Reader;


class ArgValidator(object):

    def __init__(self,name,  expected_args:list):
        if(type(expected_args) != list):
            raise TypeError("@ArgValidator: expecting a first object of the variable names expected.");
        self.__expected_args  = expected_args
        self.__Name  =  name;

    @property
    def Name(self):
        return self.__Name;

    @property
    def Args(self):
        return self.__expected_args;

    def Valid(self, **kwargs):
        for key in kwargs:
            if( key in self.__expected_args) is not True:
                raise ValueError("{1} : Unknown '{0}' argument provided".format(key, self.Name))
        return True;
        
        
class ProjectSelectionEvent(Event):
    
    def __init__(self, project: Project):
        super().__init__("Project.changed.event")
        self.__Project  =  project;
        
    @property
    def Project(self):
        return self.__Project

"""
  A class for the main servotest timesheet format model class implementation
  
"""
class TimesheetModel(ModelBase):
    '''
      timesheet                       : a timesheet object of type Timesheet , default is None
      contracted_weekly_hours         : this is the normal ours expected by the employee every week.
      threshold_hours_before_overtime : this is the hour employee have to be done before considering paying for over time.
    '''

    def __init__(self, timesheet:Timesheet  = None, **kwargs):
        super().__init__()
        self.__ArgsValidator =  ArgValidator(self.__class__, ['contracted_weekly_hours',
                                              'threshold_hours_before_overtime',
                                              ]);
        if(timesheet is not None):
            if(isinstance(timesheet, Timesheet) is not True):
                raise TypeError("@TimesheetModel: expecting a timesheet object but {0} given".format(type(timesheet)));
        self.__ArgsValidator.Valid(**kwargs);
        
        expected_hours                   = kwargs['contracted_weekly_hours'] if('contracted_weekly_hours' in kwargs)   else DAILY_EXPECTED_HOURS;
        threshold_hours                  = kwargs['threshold_hours_before_overtime'] if('threshold_hours_before_overtime' in kwargs) else WEEKLY_UNPAY_OVERTIME_HOURS;
        self.__Timesheet                 = timesheet;
        self.__DailyExpectedHours        = expected_hours  if((type(expected_hours) == float) or  (type(expected_hours) == int))  else 0.0
        self.__WeeklyUnPayOvertimeHours  = threshold_hours if((type(threshold_hours) == float) or (type(threshold_hours) == int)) else 0.0
        self.__Project                   = None;

        #Events Handler
        self.__ProjectSelected  = EventHandler();
        


    @property
    def ProjectSelected(self):
        return self.__ProjectSelected

    @ProjectSelected.setter
    def ProjectSelected(self, handler: EventHandler):
        if(handler != self.__ProjectSelected):
            raise ValueError("@ProjectSelected: event handler can not be changed");
        self.__ProjectSelected  =  handler;
                    
    @property
    def WeeklyUnPayOvertimeHours(self):
        return self.__WeeklyUnPayOvertimeHours

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
        return self.__Project;

    @Project.setter
    def Project(self, project: Project):
        if(project is not None):
            if(isinstance(project, Project) is not True):
                raise  TypeError("@Project: expecting a Timesheet.Project object type");
        if(self.__Project != project):
            allowChanged  =  False;
            if(project is None):
                 allowChanged  = True                
            else:
                # can only select a project that already exists
                for tempro in self.Projects:
                    if(project == tempro):
                        allowChanged  = True 
                        break
            if(allowChanged is True):
                self.__Project  =  project
                self.ProjectSelected(ProjectSelectionEvent(project));
                    

    def Compute(self)-> Timesheet:                
        if( self.Timesheet is not None):
            # computer  total legal hours and overtimehours
            dailyTimeObject =  TimeObject(self.DailyExpectedHours * 60 * 60 * 1000);
            unpayThreshold  =  TimeObject(self.WeeklyUnPayOvertimeHours * 60 * 60 * 1000);
            if(self.Timesheet.Projects.Total.Hours > dailyTimeObject):

                overtimeDiff  =  (self.Timesheet.Project.Total   - dailyTimeObject)
                if(overtimeDiff  > unpayThreshold):
                    self.Timesheet.OverTimeWeeklyHours   = overtimeDiff - unpayThreshold;
            self.Timesheet.TotalLegalWeeklyHours =  self.Timesheet.Projects.Total   - self.Timesheet.OverTimeWeeklyHours

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



if __name__ =="__main__":

    def OnProjectSelected(event):
        print("Project have be selected")
        print("Selected Project Contract = {0}".format(event.Project.ContractNumber))
        
    loader  =  XLSTimesheetLoader(filename = XLS_TIME_SHEET_FILE);
    timesheet  = loader.Reader.Parse();
    model = TimesheetModel(timesheet);
    model.ProjectSelected +=OnProjectSelected
    print("Creating a new Project");
    project  =  model.CreateProject(contract  =  "OB890");
    print(project)
    print(project.WeeklyElapseHours);
    project.TimeHistory.Insert(DayOfWeekType.MONDAY, 2.0 * 60*60*1000);
    model.Project  = project

    print("Computing test");
    model.Compute();
    print(model.Timesheet.TotalLegalWeeklyHours);
    print(model.Timesheet.OverTimeWeeklyHours);
    print("\nPrint all project test");
    for project in model.Projects:
        print(project.ContractNumber);
    print("\nFind existing contract");
    project  =  model.Find(contract  = '61534');
    if(project is not None):
        print(project.ContractNumber);
        print(project.WeeklyElapseHours)
    
    print(timesheet);
