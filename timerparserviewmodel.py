"""
 Create the timesheet model . to calculated the time sheet as the time is entered.
"""
import os;
import datetime as dt;
import PyPDF2
from PyPDF2 import PdfFileWriter;
from controllerbase    import ControllerBase
from project import Project, ProjectType
from timesheet         import Timesheet, DayOfWeekType
from timesheetreader   import TimesheetReader,  ODSTimesheetReader, XLSTimesheetReader
from timesheetrecorder import TimesheetRecorder
from timesheetmodel    import TimesheetModel, XLSTimesheetLoader
from  PyPDF2.pdf  import PageObject



class TimesheetPDFWriter(object):

    def __init__(self):
        
        pass;


    def Write(self, filename : str ,  timesheet: Timesheet):
        if(isinstance(timesheet, Timesheet)):
            writer  = PdfFileWriter(fname  =  filename);
            print(timesheet)
            print(filename)
    
        

class  TimesheetController(ControllerBase):

    def __init__(self, model : TimesheetModel, **kwargs):
        super().__init__();
        if(isinstance(model, TimesheetModel) is not True):
            raise TypeError("@Timesheet Controller : expecting parameter 1 to TimesheetModel type")

        # configured the timesheet
        self.__TimesheetViewModel  = model
        self.__TimesheetViewModel.ProjectSelected       += self.__OnProjectSelected
        
        #Configure the time sheet pdf writer
        self.__TimesheetPdfWriter  = TimesheetPDFWriter();

        # Configured the timesheet recorder
        self.__TimesheetRecorder   =  TimesheetRecorder(interval = 1);
        self.__TimesheetRecorder.Completed              += self.__RecordCompleted;
        self.__TimesheetRecorder.Progressed             += self.__OnRecordProgressing
        self.__TimesheetRecorder.Failured               += self.__OnRecordingFailured
        self.__TimesheetRecorder.Started                += self.__OnRecordStarted

    @property
    def Model(self):
        return self.__TimesheetViewModel;

    @property
    def Today(self):
        today  = dt.datetime.now();
        return today;
        
    @property
    def WeekDay(self):
        '''
         Return the week day type which can be used to stamp the timesheet.
        '''
        result  =  None
        today  = self.Today;
        if(isinstance(today, dt.datetime)):
            weekday  = today.weekday() # 0 - 6 starting from monday
            
            if(weekday == 0):
                result  =  DayOfWeekType.MONDAY
            elif(weekday == 1):
                result  = DayOfWeekType.TUESDAY
            elif(weekday == 2):
                result  = DayOfWeekType.WEDNESDAY
            elif(weekday == 3):
                result  =  DayOfWeekType.THURSDAY
            elif(weekday == 4):
                result  = DayOfWeekType.FRIDAY
            elif(weekday == 5):
                result  =  DayOfWeekType.SATURDAY
            else:
                result  =  DayOfWeekType.SUNDAY
                
        return result;

 
    @property
    def Recorder(self):
        return  self.__TimesheetRecorder

    @property
    def PdfWriter(self):
        return self.__TimesheetPdfWriter;

    def __OnRecordStarted(self, event):
        print("Timesheet recording started");
        if(self.__TimesheetViewModel != None):
            if(self.__TimesheetViewModel.Project == None):
                print("No Project selected")
                self.Recorder.Stop();

    def __OnRecordingFailured(self, event):
        print(event.Error)

    def __OnProjectSelected(self, evet):
        print("Project selected")


    def __OnRecordProgressing(self, event):
        print("Recording In Progress = {0}:{1}:{2}.{3}".format(event.Elapsed.Hours, event.Elapsed.Minutes, event.Elapsed.Seconds, event.Elapsed.Milliseconds))
        if(self.Model != None):
            project      =  self.Model.Project
            project.TimeHistory.Update(self.WeekDay,  event.Elapsed.Timestamp)
            print(project.TimeHistory.Get(self.WeekDay))


    def __RecordCompleted(self, event):
        if(evt != None):
            print("Recording Completed = {0}:{1}:{2}.{3}".format(event.Elapsed.Hours, event.Elapsed.Minutes, eevent.Elapsed.Seconds, event.Elapsed.Milliseconds));
            
        


if __name__ =="__main__":
    ODS_TIME_SHEET_FILE   = "./data/timesheet.ods"
    XLS_TIME_SHEET_FILE   = "./data/timesheet.xlsx"
    WRITE_TEST_FILE       = "./data/pdftest2.pdf";
    
    loader      =  XLSTimesheetLoader(filename=XLS_TIME_SHEET_FILE);    
    model       =  TimesheetModel(loader.Reader.Parse());
    controller  =  TimesheetController(model  = model);

    controller.Recorder.Start();
    model.Project  =  model.Projects[0];
    print(controller.Today.weekday())
    pdf =  PdfFileWriter();
    print(PyPDF2.pdf)
    with open(WRITE_TEST_FILE , mode='wb+') as stream:
     
        pdf.addBlankPage(594 , 841);
        pdf.setPageLayout("/SinglePage")

        # Create a stream object
        # according to the pdf standard this contain the stream of pdf objects
        #streamObject =  StreamObject();
        page  = pdf.getPage(0);
        content  =  page.getContents();
        print(content)
        
       
       
        
            
        pdf.write(stream)


   
    
    
   
   
    
    
    
    
              
           
 

   
