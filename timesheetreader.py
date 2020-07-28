import os;
import xlrd
import pyexcel_ods;
from timesheet import Timesheet,DayOfWeekType
from timesheet import Project,ProjectType;
from collections import OrderedDict


'''
 Base timesheet reader class 
'''
class TimesheetReader(object):

    def __init__(self, filename : str):
        if(os.path.exists(filename) is not True):
            raise TypeError("@Timesheet Controller : {0} name does not exists")
        self.__Filename  =  filename

    def Parse(self):
        raise NotImplementedError("@Parse: method must be implemented.")

    @property
    def Filename(self):
        return self.__Filename


    def __ParseProject(self, project_rec:list,  project_type:int):
        project  = None
        
        if(len(project_rec) > 4):
            #Filter out unfilled timesheet projects
            #get the  project details'
            details    =  project_rec[0:5]
            hours_recs =  project_rec[5:]
                                  
            if(len(hours_recs) >= 0) and (len(details) == 5):
                orderno =  str(details[1]).strip();
                #Only allow if order number is not empty or the project type is a fixed project.
                if(orderno != "") or (project_type  ==  ProjectType.FIXED_PROJECT):
                    #Create the project objects.
                    project                 =  Project(orderno,project_type)
                    project.RSRCE           =  str(details[0]).strip()
                    contractNumber  = details[2];
                    if(type(contractNumber) != str):
                        contractNumber = str(int(contractNumber));
                    project.ContractNumber  =  contractNumber.strip()
                    project.Description     =  str(details[4]).strip()

                    #Load the project hours
                    ndays  =  len(hours_recs)
                    if(ndays > 0):
                        project.ElapseHours[DayOfWeekType.MONDAY]    = self.toNumber(hours_recs[0])                                            
                    if(ndays > 1):
                        project.ElapseHours[DayOfWeekType.TUESDAY]   = self.toNumber(hours_recs[1])
                            
                    if(ndays > 2):
                        project.ElapseHours[DayOfWeekType.WEDNESDAY] = self.toNumber(hours_recs[2])

                    if(ndays > 3):
                        project.ElapseHours[DayOfWeekType.THURSDAY]  = self.toNumber(hours_recs[3])

                    if(ndays > 4):
                        project.ElapseHours[DayOfWeekType.FRIDAY]    = self.toNumber(hours_recs[4])
                                                
                    if(ndays > 5):
                        project.ElapseHours[DayOfWeekType.SATURDAY]  = self.toNumber(hours_recs[5])

                    if(ndays > 6):
                        project.ElapseHours[DayOfWeekType.SUNDAY]    = self.toNumber(hours_recs[6])
        return project


    def toNumber(self, value:str):
        value  =  str(value)
        result  =  0.0
        if(value.strip() != ''):
            try:
                result  =  float(value)
            except Exception as err:
                print("@toNumber Error  = {0}".format(err))
        return result;            


    def _ParseProjects(self, timesheet, projects_recs, projectType):
               
        for project_rec in  projects_recs:
            project  = self.__ParseProject( project_rec, projectType)
            if(project != None):
                #Project defined
                if(project.Type == ProjectType.USER_DEFINED_PROJECT):
                    timesheet.Projects.Records.append(project);
                elif(project.Type == ProjectType.FIXED_PROJECT):
                    timesheet.Projects.FixedRecords.append(project)
                else:
                    raise TypeError("@Project type is invalid")



'''
  A timesheet reader for a ODS file format
  
'''
class ODSTimesheetReader(TimesheetReader):

    def __init__(self, filename:str):
        super().__init__(filename);
                                
    def Parse(self):
        timesheet  =  None;
        workbook  =  pyexcel_ods.get_data(self.Filename)
        keys =  list(workbook.keys())
        
        if(len(keys) > 0):
            sheets  =  list(workbook.items())
            
            if(len(sheets) > 0):
                # Interested in the first sheet
                sheet  =  sheets[0]
                if(sheet is not None):
                    timesheet =  Timesheet(sheet[0])
                    timesheet.OverTimeHours   = 0.0
                    timesheet.TotalLegalHours = 0.0
                    records  =  sheet[1]
                    """
                      Records are list of records.
                      record are python list object of cell values that are not empty.
                    """
                    if(len(records) > 0):
                        header_record       =  records[0]
                        timesheet.Header    =  header_record[-1]

                        #3record is weekly timesheet line
                        
                        weekly_record                  =  records[2]
                        timesheet.EmployeeName         = weekly_record[1]
                        timesheet.Title                = weekly_record[2]
                        timesheet.WeekEndingSunday     = weekly_record[4]

                        #department record line
                        department_record = records[3];
                        timesheet.Department    = department_record[1]

                        #timesheet description
                        timesheet.Description   =  records[4][0]

                        #project records
                        project_column_headers  =  records[5]
                        if(len(project_column_headers) > 5):
                            timesheet.Projects.Header.append(project_column_headers[0]) # RSRCE
                            timesheet.Projects.Header.append(project_column_headers[1]) # Work Order No
                            timesheet.Projects.Header.append(project_column_headers[2]) # Contract Number
                            timesheet.Projects.Header.append(project_column_headers[3]) # Total Hours
                            timesheet.Projects.Header.append(project_column_headers[4]) # Description
                    
                            # Load the projects that are filled by default its fixed to 24 records
                            user_defineds_recs = records[6:30]
                            self._ParseProjects(timesheet, user_defineds_recs, ProjectType.USER_DEFINED_PROJECT)

                            # Load the fixed projects or tasks projects.
                            # this involves holidays , pay leaves e.t.c
                            # there are 15 of does at the moment.
                            fixed_project_recs =  records[31:45]
                            self._ParseProjects(timesheet, fixed_project_recs, ProjectType.FIXED_PROJECT)

                            # The year stamp time for the timesheet.
                            template_records  = records[50:52];
                            if(len(template_records) > 0):
                                template_rec =  template_records[0]
                                if(len(template_rec) > 0):
                                   timesheet.Template =  template_rec[0]
                            
        return timesheet



'''
 Timesheet reader for xls and xlsx files
 
'''
class XLSTimesheetReader(TimesheetReader):

    def __init__(self, filename :str):
        super().__init__(filename)
        
    def Parse(self):
        timesheet  =  None;
        workbook  =  xlrd.open_workbook(self.Filename)
        
        if(len(workbook.sheets()) > 0):
            #interested on the first sheet
            sheet      =  workbook.sheets()[0];
            timesheet  = Timesheet(sheet.name);
            timesheet.OverTimeHours   = 0.0
            timesheet.TotalLegalHours = 0.0
            cell = sheet.cell(0,4) # the timesheet header text
            if(cell is not None):            
                timesheet.Header            = cell.value;
            timesheet.EmployeeName          = sheet.cell(2, 2).value
            timesheet.Title                 = sheet.cell(2, 4).value
            timesheet.WeekEndingSunday      = sheet.cell(2, 10).value
            timesheet.Department            = sheet.cell(3, 2).value
            timesheet.Description           = sheet.cell(4,0).value

            #Timesheet column titles
            timesheet.Projects.Header.append(sheet.cell(5,0).value) # RSRCE
            timesheet.Projects.Header.append(sheet.cell(5,1).value) # Work Order No
            timesheet.Projects.Header.append(sheet.cell(5,2).value) # Contract Number
            timesheet.Projects.Header.append(sheet.cell(5,3).value) # Total Hours
            timesheet.Projects.Header.append(sheet.cell(5,4).value) # Description

            # Load the projects that are filled by default its fixed to 24 records
            user_defineds_recs = self.__FromRowAtToList(sheet, 6,30);                
            self._ParseProjects(timesheet, user_defineds_recs, ProjectType.USER_DEFINED_PROJECT)

            #Fixed records
            fixed_project_recs =  self.__FromRowAtToList(sheet,31,45)
          
            self._ParseProjects(timesheet, fixed_project_recs, ProjectType.FIXED_PROJECT)
            
            # The year stamp time for the timesheet.
            timesheet.Template  = sheet.cell(50,0).value
        
        return timesheet

    def __FromRowAtToList(self, sheet : xlrd.sheet, start:int , end:int):
        records =  list();
        for i in range(start, end):
            row = sheet.row(i)
            table =  list()
            
            for cell in row:
                table.append(cell.value)
            records.append(table)
        return records

        
    
if __name__ =="__main__":
    ODS_TIME_SHEET_FILE   = "./data/timesheet.ods"
    XLS_TIME_SHEET_FILE   = "./data/timesheet.xlsx"
    WRITE_TEST_FILE   = "./data/timesheet_test.ods";

    treader   =  ODSTimesheetReader(filename= ODS_TIME_SHEET_FILE);
    timesheet =  treader.Parse();
    print(timesheet)
    print(timesheet.Template);
    print(timesheet.OverTimeHours);
    print(timesheet.Description);

    #Write back the timesheet file

    print("\n**************************TIMESHEET XLSX*****************************\n");
    xslreader  = XLSTimesheetReader(filename = XLS_TIME_SHEET_FILE);
    timesheet2 = xslreader.Parse();
    print(timesheet2)
    print(timesheet2.Template);
    print(timesheet2.OverTimeHours);
    print(timesheet2.Description);
